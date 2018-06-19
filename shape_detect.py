"""Shape detection.

Detect rectangle shapes in images, cut out 128px
surrounding shape and then pass it to the decensoring
program and replace the censored tile with the
decensored one.
"""

import numpy as np
import cv2
import argparse
from PIL import Image
import os


isExec = __name__ == '__main__'


box_size = 128
def cv_to_pillow(image, i = 0):
    """
    converted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    conv_array = np.array(converted)
    pil_image = Image.fromarray(conv_array)
    print(converted)
    print(conv_array)
    print(pil_image)
    return pil_image
    """

    # TODO(SoftArmpit): This is inefficient, convert directly instead.
    file_path = os.path.join('/tmp/', str(i) + '.png')
    write_to_file(image, file_path)
    pil_box_image = Image.open(file_path).convert('RGB')
    return pil_box_image


def pillow_to_cv(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def insert_box(box, image):
    (box_image, x, y) = box
    image[y:y+box_image.shape[0], x:x+box_image.shape[1]] = box_image
    return image


def detect_shape(c):
    perim = cv2.arcLength(c, True)
    vertices = cv2.approxPolyDP(c, 0.04 * perim, True)

    print('Vertices: ' + str(len(vertices)))
    return len(vertices) == 4


def process_contour(image, c):
    M = cv2.moments(c)
    print(M)

    if M['m00'] == 0:
        return None

    cx = int(M['m10'] / M['m00'] - box_size / 2)
    cy = int(M['m01'] / M['m00'] - box_size / 2)
    # NOTE(SoftArmpit): Limit box to image boundaries
    cx = min(max(cx, 0), image.shape[1] - box_size)
    cy = min(max(cy, 0), image.shape[0] - box_size)
    box = image[cy:cy+box_size, cx:cx+box_size]

    print(str(cx) + ", " + str(cy))
    area = cv2.contourArea(c)

    if area < 148:
        print('Area too small: ' + str(area) + "at " + str(cx) + 'x' + str(cy))
        return None

    return (box, cx, cy)


def process_image(image, mask_color):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    green_mask = cv2.inRange(image, mask_color, mask_color)
    if isExec:
        cv2.imshow("Mask", green_mask)
    (_, cs, _) = cv2.findContours(green_mask,
                                  cv2.RETR_EXTERNAL,
                                  cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
    for c in cs:
        isRect = detect_shape(c)

        if isRect or True:
            print("Rectangle detected")
            pc = process_contour(image, c)
            if pc is not None:
                boxes.append(pc)

    return boxes


def process_image_path(image_path, mask_color):
    image = cv2.imread(image_path)
    return (image, process_image(image, mask_color))


def write_to_file(image, path):
    cv2.imwrite(path, image)


def main():
    """Entry function."""
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--file', required=True, help='Path to image file')
    ap.add_argument('-g', '--green', required=False, default=255)
    ap.add_argument('-r', '--red', required=False, default=0)
    ap.add_argument('-b', '--blue', required=False, default=0)
    args = ap.parse_args()

    (image, boxes) = process_image_path(args.file, (args.red, args.green, args.blue))

    print(len(boxes))
    for (box_image, cx, cy) in boxes:
        cv2.imshow("Box " + str(cx) + 'x' + str(cy), box_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
