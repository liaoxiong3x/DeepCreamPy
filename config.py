import argparse

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1', True):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0', False):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')



parser = argparse.ArgumentParser(description='')

#Image setting
parser.add_argument('--input_size', dest='input_size', default=128, help='input image size')
parser.add_argument('--local_input_size', dest='local_input_size', default=64, help='local input image size')
parser.add_argument('--input_channel_size', dest='input_channel_size', default=3, help='input image channel')
parser.add_argument('--min_mask_size', dest='min_mask_size', default=24, help='minimum mask size')
parser.add_argument('--max_mask_size', dest='max_mask_size', default=48, help='maximum mask size')
parser.add_argument('--rotate_chance', dest='rotate_chance', default=0.5, help='chance the mask will be randomly rotated')
parser.add_argument('--train_mosaic', dest ='train_mosaic', default=False, help='train neural network to decensor mosaics')

# parser.add_argument('--input_dim', dest='input_dim', default=100, help='input z size')

# #Training Settings
parser.add_argument('--continue_training', dest='continue_training', default=False, type=str2bool, help='flag to continue training')

# parser.add_argument('--data', dest='data', default='../ambientGAN_TF/data', help='cats image train path')

parser.add_argument('--batch_size', dest='batch_size', default=16, help='batch size')
# parser.add_argument('--train_step', dest='train_step', default=400, help='total number of train_step')
# parser.add_argument('--Tc', dest='Tc', default=100, help='Tc to train Completion Network')
# parser.add_argument('--Td', dest='Td', default=1, help='Td to train Discriminator Network')


parser.add_argument('--learning_rate', dest='learning_rate', default=0.001, help='learning rate of the optimizer')
# parser.add_argument('--momentum', dest='momentum', default=0.5, help='momentum of the optimizer')

# #I set alpha to 1 to give more weights to the discriminator loss
# parser.add_argument('--alpha', dest='alpha', default=1.0, help='alpha')

# parser.add_argument('--margin', dest='margin', default=5, help='margin')

# #Test image
# parser.add_argument('--img_path', dest='img_path', default='', help='test image path')

# #Extra folders setting
# parser.add_argument('--checkpoints_path', dest='checkpoints_path', default='./checkpoints/', help='saved model checkpoint path')
# parser.add_argument('--graph_path', dest='graph_path', default='./graphs/', help='tensorboard graph')
# parser.add_argument('--images_path', dest='images_path', default='./images/', help='result images path')
parser.add_argument('--training_samples_path', dest='training_samples_path', default='./training_samples/', help='samples images generated during training path')


args = parser.parse_args()