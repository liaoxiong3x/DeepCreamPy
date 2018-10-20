import numpy as np
from PIL import Image
import os

from copy import deepcopy

import config
from libs.pconv_hybrid_model import PConvUnet
from libs.flood_fill import find_regions, expand_bounding

class Decensor():

    def __init__(self):
        self.args = config.get_args()
        self.decensor_mosaic = self.args.is_mosaic

        self.mask_color = [self.args.mask_color_red/255.0, self.args.mask_color_green/255.0, self.args.mask_color_blue/255.0]

        if not os.path.exists(self.args.decensor_output_path):
            os.makedirs(self.args.decensor_output_path)

        self.load_model()

    def get_mask(self,ori, width, height):
        mask = np.zeros(ori.shape, np.uint8)
        #count = 0
        #TODO: change to iterate over all images in batch when implementing batches
        for row in range(height):
            for col in range(width):
                if np.array_equal(ori[0][row][col], self.mask_color):
                    mask[0, row, col] = 1
        return 1-mask

    def load_model(self):
        self.model = PConvUnet(weight_filepath='data/logs/')
        self.model.load(
            r"./models/model.h5",
            train_bn=False,
            lr=0.00005
        )

    def decensor_all_images_in_folder(self):
        #load model once at beginning and reuse same model
        #self.load_model()

        subdir = self.args.decensor_input_path
        files = os.listdir(subdir)

        #convert all images into np arrays and put them in a list
        for file in files:
            #print(file)
            file_path = os.path.join(subdir, file)
            if os.path.isfile(file_path) and os.path.splitext(file_path)[1] == ".png":
                print("Decensoring the image {file_path}".format(file_path))
                censored_img = Image.open(file_path)
                self.decensor_image(censored_img, file)

    #decensors one image at a time
    #TODO: decensor all cropped parts of the same image in a batch (then i need input for ori an array of those images and make additional changes)
    def decensor_image(self,ori, file_name):
        width, height = ori.size
        #save the alpha channel if the image has an alpha channel
        has_alpha = False
        alpha_channel = None
        if (ori.mode == "RGBA"):
            has_alpha = True
            alpha_channel = np.asarray(ori)[:,:,3]
            alpha_channel = np.expand_dims(alpha_channel, axis =-1)
            ori = ori.convert('RGB')

        ori_array = np.asarray(ori)
        ori_array = np.array(ori_array / 255.0)
        ori_array = np.expand_dims(ori_array, axis = 0)

        mask = self.get_mask(ori_array, width, height)

        regions = find_regions(ori)
        print("Found {region_count} censored regions in this image!".format(region_count = len(regions)))

        if len(regions) == 0 and not self.decensor_mosaic:
            print("No green colored regions detected!")
            return

        output_img_array = ori_array[0].copy()

        for region_counter, region in enumerate(regions, 1):
            bounding_box = expand_bounding(ori, region)
            crop_img = ori.crop(bounding_box)
            #crop_img.show()
            #convert mask back to image
            mask_reshaped = mask[0,:,:,:] * 255.0
            mask_img = Image.fromarray(mask_reshaped.astype('uint8'))
            #resize the cropped images
            crop_img = crop_img.resize((512, 512))
            crop_img_array = np.asarray(crop_img)
            crop_img_array = crop_img_array / 255.0
            crop_img_array = np.expand_dims(crop_img_array, axis = 0)
            #resize the mask images
            mask_img = mask_img.crop(bounding_box)
            mask_img = mask_img.resize((512, 512))
            #mask_img.show()
            #convert mask_img back to array 
            mask_array = np.asarray(mask_img)
            mask_array = np.array(mask_array / 255.0)
            #the mask has been upscaled so there will be values not equal to 0 or 1
            #mask_array[mask_array < 0.01] = 0
            mask_array[mask_array > 0] = 1
            mask_array = np.expand_dims(mask_array, axis = 0)

            # Run predictions for this batch of images
            pred_img_array = self.model.predict([crop_img_array, mask_array, mask_array])
            
            pred_img_array = pred_img_array * 255.0
            pred_img_array = np.squeeze(pred_img_array, axis = 0)

            #scale prediction image back to original size
            bounding_width = bounding_box[2]-bounding_box[0]
            bounding_height = bounding_box[3]-bounding_box[1]
            #convert np array to image

            # print(bounding_width,bounding_height)
            # print(pred_img_array.shape)

            pred_img = Image.fromarray(pred_img_array.astype('uint8'))
            #pred_img.show()
            pred_img = pred_img.resize((bounding_width, bounding_height), resample = Image.BICUBIC)
            pred_img_array = np.asarray(pred_img)
            pred_img_array = pred_img_array / 255.0

            # print(pred_img_array.shape)
            pred_img_array = np.expand_dims(pred_img_array, axis = 0)

            for i in range(len(ori_array)):
                if self.decensor_mosaic:
                    output_img_array = pred_img[i]
                else:
                    for col in range(bounding_width):
                        for row in range(bounding_height):
                            bounding_width = col + bounding_box[0]
                            bounding_height = row + bounding_box[1]
                            if (bounding_width, bounding_height) in region:
                                output_img_array[bounding_height][bounding_width] = pred_img_array[i,:,:,:][row][col]
            print("{region_counter} out of {region_count} regions decensored.".format(region_counter=region_counter, region_count=len(regions)))

        output_img_array = output_img_array * 255.0

        #restore the alpha channel
        if has_alpha:
            print(output_img_array.shape)
            print(alpha_channel.shape)
            output_img_array = np.concatenate((output_img_array, alpha_channel), axis = 2)

        output_img = Image.fromarray(output_img_array.astype('uint8'))

        #save the decensored image
        #file_name, _ = os.path.splitext(file_name)
        save_path = os.path.join(self.args.decensor_output_path, file_name)
        output_img.save(save_path)

        print("Decensored image saved to {save_path}!".format(save_path=save_path))
        return

if __name__ == '__main__':
    decensor = Decensor()
    decensor.decensor_all_images_in_folder()