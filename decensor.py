import numpy as np
import tensorflow as tf
from PIL import Image
import tqdm
import os
import matplotlib.pyplot as plt
import stat
import sys
sys.path.append('..')

from model import Model
from poisson_blend import blend
from config import *
import shape_detect as sd

#TODO: allow variable batch sizes when decensoring. changing BATCH_SIZE will likely result in crashing
BATCH_SIZE = 1

mask_color = [args.mask_color_red, args.mask_color_green, args.mask_color_blue]
poisson_blending_enabled = False

def is_file(file):
    try:
        return not stat.S_ISDIR(os.stat(file).st_mode)
    except:
        return False

def get_files(dir):
    all_files = os.listdir(dir)
    filtered_files = list(filter(lambda file: is_file(os.path.join(dir, file)), all_files))
    return filtered_files

def find_censor_boxes(image_path):
    (image, boxes) = sd.process_image_path(image_path, tuple(mask_color))

    i = 0
    for (box_image, cx, cy) in boxes:
        pil_box_image = sd.cv_to_pillow(box_image)
        boxes[i] = (pil_box_image, cx, cy)
        i += 1

    # boxes = map(lambda box: (sd.cv_to_pillow(box[0]), box[1], box[2]), boxes)
    return (image, boxes)

def decensor(args):
    subdir = args.decensor_input_path
    files = sorted(get_files(subdir))

    for file in files:
        file_path = os.path.join(subdir, file)
        if os.path.isfile(file_path) and os.path.splitext(file_path)[1] == ".png":
            print(file_path)
            (image, boxes) = find_censor_boxes(file_path)
            decensored_boxes = decensor_boxes(args, boxes)
            for (box_pillow_image, cx, cy) in decensored_boxes:
                box_image = sd.pillow_to_cv(box_pillow_image)
                image = sd.insert_box((box_image, cx, cy), image)

            sd.write_to_file(image, os.path.join(args.decensor_output_path, file))

def decensor_boxes(args, boxes):
    x = tf.placeholder(tf.float32, [BATCH_SIZE, args.input_size, args.input_size, args.input_channel_size])
    mask = tf.placeholder(tf.float32, [BATCH_SIZE, args.input_size, args.input_size, 1])
    local_x = tf.placeholder(tf.float32, [BATCH_SIZE, args.local_input_size, args.local_input_size, args.input_channel_size])
    global_completion = tf.placeholder(tf.float32, [BATCH_SIZE, args.input_size, args.input_size, args.input_channel_size])
    local_completion = tf.placeholder(tf.float32, [BATCH_SIZE, args.local_input_size, args.local_input_size, args.input_channel_size])
    is_training = tf.placeholder(tf.bool, [])

    model = Model(x, mask, local_x, global_completion, local_completion, is_training, batch_size=BATCH_SIZE)
    sess = tf.Session()
    init_op = tf.global_variables_initializer()
    sess.run(init_op)

    saver = tf.train.Saver()
    saver.restore(sess, './models/latest')

    mask_decensor = []
    x_decensor = []

    for (box_image, cx, cy) in boxes:
        image = np.array(box_image)
        image = np.array(image / 127.5 - 1)
        x_decensor.append(image)

    x_decensor = np.array(x_decensor)
    print(x_decensor.shape)
    step_num = int(len(x_decensor) / BATCH_SIZE)

    results = []

    cnt = 0
    for i in tqdm.tqdm(range(step_num)):
        x_batch = x_decensor[i * BATCH_SIZE:(i + 1) * BATCH_SIZE]
        mask_batch = get_mask(x_batch)
        completion = sess.run(model.completion, feed_dict={x: x_batch, mask: mask_batch, is_training: False})
        for i in range(BATCH_SIZE):
            img = completion[i]
            img = np.array((img + 1) * 127.5, dtype=np.uint8)
            original = x_batch[i]
            original = np.array((original + 1) * 127.5, dtype=np.uint8)
            if (poisson_blending_enabled):
                img = blend(original, img, mask_batch[0,:,:,0])
            output = Image.fromarray(img.astype('uint8'), 'RGB')
            results.append((output, boxes[cnt][1], boxes[cnt][2]))
            cnt += 1

    tf.reset_default_graph()
    return results

def get_mask(x_batch):
    points = []
    mask = []
    for i in range(BATCH_SIZE):
        raw = x_batch[i]
        raw = np.array((raw + 1) * 127.5, dtype=np.uint8)
        m = np.zeros((args.input_size, args.input_size, 1), dtype=np.uint8)
        for x in range(args.input_size):
            for y in range(args.input_size):
                if np.array_equal(raw[x][y], mask_color):
                    m[x, y] = 1
        mask.append(m)
    return np.array(mask)

if __name__ == '__main__':
    if not os.path.exists(args.decensor_output_path):
        os.makedirs(args.decensor_output_path)
    decensor(args)
