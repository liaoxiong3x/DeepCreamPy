# DeepMindBreak
*Decensoring Hentai with Deep Neural Networks*

This project applies an implementation of [Globally and Locally Consistent Image Completion](http://hi.cs.waseda.ac.jp/%7Eiizuka/projects/completion/data/completion_sig2017.pdf) to the problem of hentai decensorship. Using a deep fully convolutional neural network, DeepMindBreak can replace censored artwork in hentai with plausible reconstructions. The user needs to only specify the censored regions.

# **THIS PROJECT IS STILL IN DEVELOPMENT. DO NOT BE DISAPPOINTED IF THE RESULTS AREN'T AS GOOD AS YOU EXPECT.**

![Censored, decensored](/readme_images/collage.png)

# Limitations

This project is LIMITED in capability. It is a proof of concept of ongoing research.

The decensorship is intended to ONLY work on color hentai images that have minor bar censorship of the penis or vagina.

It does NOT work with:
- Black and white images
- Monochrome images
- Hentai containing screentones (e.g. printed hentai)
- Real life porn
- Mosaic censorship
- Censorship of nipples
- Censorship of anus
- Animated gifs/videos

In particular, if a vagina or penis is completely censored out, inpainting will be ineffective.

Embarrassingly, because the neural network was trained to decensor horizontally and vertically oriented rectangles, it has trouble with angled rectangles. This will be fixed soon.

# Dependencies

- Python 2/3
- TensorFlow 1.5
- Pillow
- tqdm
- scipy
- pyamg (only needed if poisson blending is enabled in decensor.py)
- matplotlib (only for running test.py)

No GPU required! Tested on Ubuntu 16.04 and Windows.

Poisson blending is disabled by default since it has little effect on output quality.

Pillow, tqdm, scipy, pyamg, and matplotlib can all be installed using pip.

# Model
The pretrained model can be downloaded from https://drive.google.com/open?id=1mWHYSj0LDSbJQQxjR4hUMykQkVve2U3Q.

Unzip the contents into the /models/ folder.

# Usage

## I. Decensoring hentai

![Guide](/readme_images/guide.png)

The decensorship process is fairly involved. A user interface will eventually be released to streamline the process.

Using image editing software like Photoshop or GIMP, paint the areas you want to decensor the color with RGB values of (0,255,0). For each censored region, crop 128 x 128 size images containing the censored regions from your images and save them as new ".png" images.

Move the cropped images to the "decensor_input_images" directory. Decensor the images by running

```
$ python decensor.py
```

Decensored images will be saved to the "decensor_output_images" directory. Paste the decensored images back into the original image.

## II. Train the pretrained model on custom dataset

Put your custom dataset for training in the "data/images" directory and convert images to npy format.

```
$ cd training_data
$ python to_npy.py
```

Train pretrained model on your custom dataset.

```
$ python train.py
```

# To do
- ~~Add Python 3 compatibility~~
- Add random rotations in cropping rectangles
- Retrain for arbitrary shape censors
- Add a user interface
- Incorporate GAN loss into training
- Update the model to the new version

Contributions are welcome!

# License

Example image by dannychoo under [CC BY-NC-SA 2.0 License](https://creativecommons.org/licenses/by-nc-sa/2.0/). The example image is modified from the original, which can be found [here](https://www.flickr.com/photos/dannychoo/16081096643/in/photostream/).

Model is licensed under CC BY-NC 3.0 License.

Code is licensed under MIT License and is modified from tadax's project [Globally and Locally Consistent Image Completion with TensorFlow ](https://github.com/tadax/glcic), which is an implementation of the paper [Globally and Locally Consistent Image Completion](http://hi.cs.waseda.ac.jp/%7Eiizuka/projects/completion/data/completion_sig2017.pdf). It also has a modified version of parosky's project [poissonblending](https://github.com/parosky/poissonblending).

---

Copyright (c) 2018 tadax, parosky, deeppomf

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
