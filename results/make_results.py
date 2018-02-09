import cv2
import glob

paths = glob.glob('../src/test/a/*')
paths.sort()
for i, path in enumerate(paths):
    x = cv2.imread(path)
    x = x[160:340, 70:585, :]
    dst = './{}.jpg'.format("{0:03d}".format(i + 1))
    cv2.imwrite(dst, x)
