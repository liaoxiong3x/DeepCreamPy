import glob
import os
#import cv2
from PIL import Image
import numpy as np

ratio = 0.95
image_size = 128

x = []
paths = glob.glob('images/*')
for path in paths:
    #img = cv2.imread(path)
    #img = Image.open(path)
    #img = cv2.resize(img, (image_size, image_size))
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #x.append(img)
    temp = Image.open(path)
    keep = temp.copy()
    keep = np.array(keep)
    x.append(keep)
    temp.close()

x = np.array(x, dtype=np.uint8)
#np.random.shuffle(x)

p = int(ratio * len(x))
x_train = x[:p]
x_test = x[p:]

if not os.path.exists('./npy'):
    os.mkdir('./npy')
np.save('./npy/x_train.npy', x_train)
np.save('./npy/x_test.npy', x_test)