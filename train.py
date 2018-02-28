import numpy as np
import tensorflow as tf
from PIL import Image
import tqdm
import scipy.ndimage
import os

from model import Model
import load
from config import *

PRETRAIN_EPOCH = 100

def train(args):
    x = tf.placeholder(tf.float32, [args.batch_size, args.input_size, args.input_size, args.input_channel_size])
    mask = tf.placeholder(tf.float32, [args.batch_size, args.input_size, args.input_size, 1])
    local_x = tf.placeholder(tf.float32, [args.batch_size, args.local_input_size, args.local_input_size, args.input_channel_size])
    global_completion = tf.placeholder(tf.float32, [args.batch_size, args.input_size, args.input_size, args.input_channel_size])
    local_completion = tf.placeholder(tf.float32, [args.batch_size, args.local_input_size, args.local_input_size, args.input_channel_size])
    is_training = tf.placeholder(tf.bool, [])

    model = Model(x, mask, local_x, global_completion, local_completion, is_training, batch_size=args.batch_size)
    sess = tf.Session()
    global_step = tf.Variable(0, name='global_step', trainable=False)
    epoch = tf.Variable(0, name='epoch', trainable=False)

    opt = tf.train.AdamOptimizer(learning_rate=args.learning_rate)
    g_train_op = opt.minimize(model.g_loss, global_step=global_step, var_list=model.g_variables)
    d_train_op = opt.minimize(model.d_loss, global_step=global_step, var_list=model.d_variables)

    init_op = tf.global_variables_initializer()
    sess.run(init_op)

    if args.continue_training:
        if tf.train.get_checkpoint_state('./models'):
            print("Continuing training from checkpoint.")
            saver = tf.train.Saver()
            saver.restore(sess, './models/latest')
        else:
            print("Checkpoint not found! Training new model from scratch.")

    x_train, x_test = load.load()
    x_train = np.array([a / 127.5 - 1 for a in x_train])
    x_test = np.array([a / 127.5 - 1 for a in x_test])

    step_num = int(len(x_train) / args.batch_size)

    while True:
        sess.run(tf.assign(epoch, tf.add(epoch, 1)))
        print('epoch: {}'.format(sess.run(epoch)))

        np.random.shuffle(x_train)

        # Completion 
        if sess.run(epoch) <= PRETRAIN_EPOCH:
            g_loss_value = 0
            for i in tqdm.tqdm(range(step_num)):
                x_batch = x_train[i * args.batch_size:(i + 1) * args.batch_size]
                points_batch, mask_batch = get_points()

                _, g_loss = sess.run([g_train_op, model.g_loss], feed_dict={x: x_batch, mask: mask_batch, is_training: True})
                g_loss_value += g_loss

            print('Completion loss: {}'.format(g_loss_value))

            np.random.shuffle(x_test) 
            x_batch = x_test[:args.batch_size]
            completion = sess.run(model.completion, feed_dict={x: x_batch, mask: mask_batch, is_training: False})
            sample = np.array((completion[0] + 1) * 127.5, dtype=np.uint8)
            result = Image.fromarray(sample)
            result.save(args.training_samples_path +  '/{}.jpg'.format("{0:06d}".format(sess.run(epoch))))

            saver = tf.train.Saver()
            saver.save(sess, './models/latest', write_meta_graph=False)
            if sess.run(epoch) == PRETRAIN_EPOCH:
                saver.save(sess, './models/pretrained', write_meta_graph=False)


        # Discrimitation
        else:
            g_loss_value = 0
            d_loss_value = 0
            for i in tqdm.tqdm(range(step_num)):
                x_batch = x_train[i * args.batch_size:(i + 1) * args.batch_size]
                points_batch, mask_batch = get_points()

                _, g_loss, completion = sess.run([g_train_op, model.g_loss, model.completion], feed_dict={x: x_batch, mask: mask_batch, is_training: True})
                g_loss_value += g_loss

                local_x_batch = []
                local_completion_batch = []
                for i in range(args.batch_size):
                    x1, y1, x2, y2 = points_batch[i]
                    local_x_batch.append(x_batch[i][y1:y2, x1:x2, :])
                    local_completion_batch.append(completion[i][y1:y2, x1:x2, :])
                local_x_batch = np.array(local_x_batch)
                local_completion_batch = np.array(local_completion_batch)

                _, d_loss = sess.run(
                    [d_train_op, model.d_loss], 
                    feed_dict={x: x_batch, mask: mask_batch, local_x: local_x_batch, global_completion: completion, local_completion: local_completion_batch, is_training: True})
                d_loss_value += d_loss

            print('Completion loss: {}'.format(g_loss_value))
            print('Discriminator loss: {}'.format(d_loss_value))

            np.random.shuffle(x_test) 
            x_batch = x_test[:args.batch_size]
            completion = sess.run(model.completion, feed_dict={x: x_batch, mask: mask_batch, is_training: False})
            sample = np.array((completion[0] + 1) * 127.5, dtype=np.uint8)
            result = Image.fromarray(sample)
            result.save(args.training_samples_path + '{}.jpg'.format("{0:06d}".format(sess.run(epoch))))
            
            saver = tf.train.Saver()
            saver.save(sess, './models/latest', write_meta_graph=False)


def get_points():
    points = []
    mask = []
    for i in range(args.batch_size):
        x1, y1 = np.random.randint(0, args.input_size - args.local_input_size + 1, 2)
        x2, y2 = np.array([x1, y1]) + args.local_input_size
        points.append([x1, y1, x2, y2])

        w, h = np.random.randint(args.min_mask_size, args.max_mask_size + 1, 2)
        p1 = x1 + np.random.randint(0, args.local_input_size - w)
        q1 = y1 + np.random.randint(0, args.local_input_size - h)
        p2 = p1 + w
        q2 = q1 + h
        
        m = np.zeros((args.input_size, args.input_size, 1), dtype=np.uint8)
        m[q1:q2 + 1, p1:p2 + 1] = 1

        if (np.random.random() < args.rotate_chance):
        	#rotate random amount between 0 and 90 degrees
        	m = scipy.ndimage.rotate(m, np.random.random()*90, reshape = False)
        	#set all elements greater than 0 to 1
        	m[m > 0.5] = 1

        mask.append(m)

    return np.array(points), np.array(mask)


if __name__ == '__main__':
    if not os.path.exists(args.training_samples_path):
        os.makedirs(args.training_samples_path)
    train(args)