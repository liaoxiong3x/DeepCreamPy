import numpy as np
import tensorflow as tf
from PIL import Image
import tqdm
import os
import matplotlib.pyplot as plt
import sys
sys.path.append('..')

from model import Model
from poisson_blend import blend
from config import *

#size of input of local discrimnator. do not change this value.
LOCAL_SIZE = 64
BATCH_SIZE = 1

image_folder = 'decensor_input_images/'
mask_color = [0, 255, 0]
poisson_blending_enabled = False

def decensor():
    x = tf.placeholder(tf.float32, [args.batch_size, args.image_size, args.image_size, args.input_channel_size])
    mask = tf.placeholder(tf.float32, [args.batch_size, args.image_size, args.image_size, 1])
    local_x = tf.placeholder(tf.float32, [args.batch_size, args.local_image_size, args.local_image_size, args.input_channel_size])
    global_completion = tf.placeholder(tf.float32, [args.batch_size, args.image_size, args.image_size, args.input_channel_size])
    local_completion = tf.placeholder(tf.float32, [args.batch_size, args.local_image_size, args.local_image_size, args.input_channel_size])
    is_training = tf.placeholder(tf.bool, [])

    model = Model(x, mask, local_x, global_completion, local_completion, is_training, batch_size=BATCH_SIZE)
    sess = tf.Session()
    init_op = tf.global_variables_initializer()
    sess.run(init_op)

    saver = tf.train.Saver()
    saver.restore(sess, './models/latest')

    x_decensor = []
    mask_decensor = []
    for subdir, dirs, files in sorted(os.walk(image_folder)):
        for file in sorted(files):
            file_path = os.path.join(subdir, file)
            if os.path.isfile(file_path) and os.path.splitext(file_path)[1] == ".png":
                print(file_path)
                image = Image.open(file_path).convert('RGB')
                image = np.array(image)
                image = np.array(image / 127.5 - 1)
                x_decensor.append(image)
    x_decensor = np.array(x_decensor)
    print(x_decensor.shape)
    step_num = int(len(x_decensor) / BATCH_SIZE)

    cnt = 0
    for i in tqdm.tqdm(range(step_num)):
        x_batch = x_decensor[i * BATCH_SIZE:(i + 1) * BATCH_SIZE]
        mask_batch = get_mask(x_batch)
        completion = sess.run(model.completion, feed_dict={x: x_batch, mask: mask_batch, is_training: False})
        for i in range(BATCH_SIZE):
            cnt += 1
            img = completion[i]
            img = np.array((img + 1) * 127.5, dtype=np.uint8)
            original = x_batch[i]
            original = np.array((original + 1) * 127.5, dtype=np.uint8)
            if (poisson_blending_enabled):
                img = blend(original, img, mask_batch[0,:,:,0])
            output = Image.fromarray(img.astype('uint8'), 'RGB')
            dst = './decensor_output_images/{}.png'.format("{0:06d}".format(cnt))
            output.save(dst)

def get_mask(x_batch):
    points = []
    mask = []
    for i in range(BATCH_SIZE):
        raw = x_batch[i]
        raw = np.array((raw + 1) * 127.5, dtype=np.uint8)
        m = np.zeros((args.image_size, args.image_size, 1), dtype=np.uint8)
        for x in range(args.image_size):
            for y in range(args.image_size):
                if np.array_equal(raw[x][y], [0, 255, 0]):
                    m[x, y] = 1
        mask.append(m)
    return np.array(mask)

if __name__ == '__main__':
    decensor()
    
