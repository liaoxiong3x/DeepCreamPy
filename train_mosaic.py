import numpy as np
import tensorflow as tf
from PIL import Image, ImageFilter
import tqdm
from model_mosaic import Model
import load

IMAGE_SIZE = 128
LOCAL_SIZE = 64
HOLE_MIN = 24
HOLE_MAX = 48
MOSAIC_MIN = 8 #Minimum number of mosaic squares across image
MOSAIC_MAX = 32 #Maximum number of mosaic squares across image
MOSAIC_GAUSSIAN_P = 0.5 #represent images that have been compressed post-mosaic
MOSAIC_GAUSSIAN_MIN = 0.2
MOSAIC_GAUSSIAN_MAX = 1.2
LEARNING_RATE = 1e-3
BATCH_SIZE = 16
PRETRAIN_EPOCH = 100

def train():
    x = tf.placeholder(tf.float32, [BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, 3])
    mosaic = tf.placeholder(tf.float32, [BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, 3])
    mask = tf.placeholder(tf.float32, [BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, 1])
    local_x = tf.placeholder(tf.float32, [BATCH_SIZE, LOCAL_SIZE, LOCAL_SIZE, 3])
    global_completion = tf.placeholder(tf.float32, [BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, 3])
    local_completion = tf.placeholder(tf.float32, [BATCH_SIZE, LOCAL_SIZE, LOCAL_SIZE, 3])
    is_training = tf.placeholder(tf.bool, [])

    model = Model(x, mosaic, mask, local_x, global_completion, local_completion, is_training, batch_size=BATCH_SIZE)
    sess = tf.Session()
    global_step = tf.Variable(0, name='global_step', trainable=False)
    epoch = tf.Variable(0, name='epoch', trainable=False)

    opt = tf.train.AdamOptimizer(learning_rate=LEARNING_RATE)
    g_train_op = opt.minimize(model.g_loss, global_step=global_step, var_list=model.g_variables)
    d_train_op = opt.minimize(model.d_loss, global_step=global_step, var_list=model.d_variables)

    init_op = tf.global_variables_initializer()
    sess.run(init_op)

    if tf.train.get_checkpoint_state('./models'):
        saver = tf.train.Saver()
        saver.restore(sess, './models/latest')

    x_train, x_test = load.load()
    x_train = np.array([a / 127.5 - 1 for a in x_train])
    x_test = np.array([a / 127.5 - 1 for a in x_test])

    step_num = int(len(x_train) / BATCH_SIZE)

    while True:
        sess.run(tf.assign(epoch, tf.add(epoch, 1)))
        print('epoch: {}'.format(sess.run(epoch)))

        np.random.shuffle(x_train)

        # Completion 
        if sess.run(epoch) <= PRETRAIN_EPOCH:
            g_loss_value = 0
            for i in tqdm.tqdm(range(step_num)):
                x_batch = x_train[i * BATCH_SIZE:(i + 1) * BATCH_SIZE]
                points_batch, mask_batch = get_points()
                mosaic_batch = get_mosaic(x_batch)

                _, g_loss = sess.run([g_train_op, model.g_loss], feed_dict={x: x_batch, mask: mask_batch, mosaic: mosaic_batch, is_training: True})
                g_loss_value += g_loss

            print('Completion loss: {}'.format(g_loss_value))

            f = open("loss.csv","a+")
            f.write(str(sess.run(epoch)) + "," + str(g_loss_value) + "," + "0" + "\n")
            f.close()

            np.random.shuffle(x_test) 
            x_batch = x_test[:BATCH_SIZE]
            mosaic_batch = get_mosaic(x_batch)
            merged, completion = sess.run([model.merged, model.completion], feed_dict={x: x_batch, mask: mask_batch, mosaic: mosaic_batch, is_training: False})
            sample = np.array((merged[0] + 1) * 127.5, dtype=np.uint8)
            result = Image.fromarray(sample)
            result.save('./training_output_images/{}_0.png'.format("{0:06d}".format(sess.run(epoch))))
            sample = np.array((completion[0] + 1) * 127.5, dtype=np.uint8)
            result = Image.fromarray(sample)
            result.save('./training_output_images/{}_1.png'.format("{0:06d}".format(sess.run(epoch))))
            
            saver = tf.train.Saver()
            saver.save(sess, './models/latest', write_meta_graph=False)
            if sess.run(epoch) == PRETRAIN_EPOCH:
                saver.save(sess, './models/pretrained', write_meta_graph=False)


        # Discrimitation
        else:
            g_loss_value = 0
            d_loss_value = 0
            for i in tqdm.tqdm(range(step_num)):
                x_batch = x_train[i * BATCH_SIZE:(i + 1) * BATCH_SIZE]
                points_batch, mask_batch = get_points()
                mosaic_batch = get_mosaic(x_batch)

                _, g_loss, completion = sess.run([g_train_op, model.g_loss, model.completion], feed_dict={x: x_batch, mask: mask_batch, mosaic: mosaic_batch, is_training: True})
                g_loss_value += g_loss

                local_x_batch = []
                local_completion_batch = []
                for i in range(BATCH_SIZE):
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
            x_batch = x_test[:BATCH_SIZE]
            mosaic_batch = get_mosaic(x_batch)
            merged, completion = sess.run([model.merged, model.completion], feed_dict={x: x_batch, mask: mask_batch, mosaic: mosaic_batch, is_training: False})
            sample = np.array((merged[0] + 1) * 127.5, dtype=np.uint8)
            result = Image.fromarray(sample)
            result.save('./training_output_images/{}_0.png'.format("{0:06d}".format(sess.run(epoch))))
            sample = np.array((completion[0] + 1) * 127.5, dtype=np.uint8)
            result = Image.fromarray(sample)
            result.save('./training_output_images/{}_1.png'.format("{0:06d}".format(sess.run(epoch))))
            
            saver = tf.train.Saver()
            saver.save(sess, './models/latest', write_meta_graph=False)


def get_points():
    points = []
    mask = []
    for i in range(BATCH_SIZE):
        x1, y1 = np.random.randint(0, IMAGE_SIZE - LOCAL_SIZE + 1, 2)
        x2, y2 = np.array([x1, y1]) + LOCAL_SIZE
        points.append([x1, y1, x2, y2])

        w, h = np.random.randint(HOLE_MIN, HOLE_MAX + 1, 2)
        p1 = x1 + np.random.randint(0, LOCAL_SIZE - w)
        q1 = y1 + np.random.randint(0, LOCAL_SIZE - h)
        p2 = p1 + w
        q2 = q1 + h
        
        m = np.zeros((IMAGE_SIZE, IMAGE_SIZE, 1), dtype=np.uint8)
        m[q1:q2 + 1, p1:p2 + 1] = 1
        mask.append(m)

    return np.array(points), np.array(mask)


def get_mosaic(x_batch):
    mosaic = []
    for i in range(BATCH_SIZE):
        im = np.array((x_batch[i] + 1) * 127.5, dtype=np.uint8)
        im = Image.fromarray(im)
        size = np.random.randint(MOSAIC_MIN, MOSAIC_MAX)
        im = im.resize((size,size),Image.LANCZOS)
        im = im.resize((IMAGE_SIZE,IMAGE_SIZE),Image.NEAREST)
        if np.random.rand() < MOSAIC_GAUSSIAN_P:
            im = im.filter(ImageFilter.GaussianBlur(np.random.uniform(MOSAIC_GAUSSIAN_MIN, MOSAIC_GAUSSIAN_MAX)))

        mosaic.append(np.array(im))
    
    mosaic = np.array([a / 127.5 - 1 for a in mosaic])
    return mosaic


if __name__ == '__main__':
    train()
    
