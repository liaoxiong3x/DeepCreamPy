from PIL import Image, ImageDraw

#find strongly connected components with the mask color
def find_regions(image):
    pixel = image.load()
    neighbors = dict()
    width, height = image.size
    for x in range(width):
        for y in range(height):
            if is_green(pixel[x,y]):
                neighbors[x, y] = {(x,y)}
    for x, y in neighbors:
        candidates = (x + 1, y), (x, y + 1)
        for candidate in candidates:
            if candidate in neighbors:
                neighbors[x, y].add(candidate)
                neighbors[candidate].add((x, y))
    closed_list = set()

    def connected_component(pixel):
        region = set()
        open_list = {pixel}
        while open_list:
            pixel = open_list.pop()
            closed_list.add(pixel)
            open_list |= neighbors[pixel] - closed_list
            region.add(pixel)
        return region

    regions = []
    for pixel in neighbors:
        if pixel not in closed_list:
            regions.append(connected_component(pixel))
    regions.sort(key = len, reverse = True)
    return regions

# risk of box being bigger than the image
def expand_bounding(img, region, expand_factor=1.5, min_size = 256, max_size=512):
    #expand bounding box to capture more context
    x, y = zip(*region)
    min_x, min_y, max_x, max_y = min(x), min(y), max(x), max(y)
    width, height = img.size
    width_center = width//2
    height_center = height//2
    bb_width = max_x - min_x
    bb_height = max_y - min_y
    x_center = (min_x + max_x)//2
    y_center = (min_y + max_y)//2
    current_size = max(bb_width, bb_height)
    current_size  = int(current_size * expand_factor)
    if current_size > max_size:
        current_size = max_size
    elif current_size < min_size:
        current_size = min_size
    x1 = x_center - current_size//2
    x2 = x_center + current_size//2
    y1 = y_center - current_size//2
    y2 = y_center + current_size//2
    x1_square = x1
    y1_square = y1
    x2_square = x2
    y2_square = y2
    #move bounding boxes that are partially outside of the image inside the image
    if (y1_square < 0 or y2_square > (height - 1)) and (x1_square < 0 or x2_square > (width - 1)):
        #conservative square region
        if x1_square < 0 and y1_square < 0:
            x1_square = 0
            y1_square = 0
            x2_square = current_size
            y2_square = current_size
        elif x2_square > (width - 1) and y2_square > (height - 1):
            x1_square = width - current_size - 1
            y1_square = 0
            x2_square = width - 1
            y2_square = current_size
        elif x1_square < 0 and y2_square > (height - 1):
            x1_square = 0
            y1_square = height - current_size - 1
            x2_square = current_size
            y2_square = height - 1
        elif x2_square > (width - 1) and y2_square > (height - 1):
            x1_square = width - current_size - 1
            y1_square = height - current_size - 1
            x2_square = width - 1
            y2_square = height - 1
        else:
            x1_square = x1
            y1_square = y1
            x2_square = x2
            y2_square = y2
    else:
        if x1_square < 0:
            difference = x1_square
            x1_square -= difference
            x2_square -= difference
        if x2_square > (width - 1):
            difference = x2_square - width + 1
            x1_square -= difference
            x2_square -= difference
        if y1_square < 0:
            difference = y1_square
            y1_square -= difference
            y2_square -= difference
        if y2_square > (height - 1):
            difference = y2_square - height + 1
            y1_square -= difference
            y2_square -= difference
    # if y1_square < 0 or y2_square > (height - 1):

    #if bounding box goes outside of the image for some reason, set bounds to original, unexpanded values
    #print(width, height)
    if x2_square > width or y2_square > height:
        print("bounding box out of bounds!")
        print(x1_square, y1_square, x2_square, y2_square)
        x1_square, y1_square, x2_square, y2_square = min_x, min_y, max_x, max_y
    return x1_square, y1_square, x2_square, y2_square

def is_green(pixel):
    r, g, b = pixel
    return r == 0 and g == 255 and b == 0

if __name__ == '__main__':
    image = Image.open('')
    no_alpha_image = image.convert('RGB')
    draw = ImageDraw.Draw(no_alpha_image)
    for region in find_regions(no_alpha_image):
        draw.rectangle(expand_bounding(no_alpha_image, region), outline=(0, 255, 0))
    no_alpha_image.show()