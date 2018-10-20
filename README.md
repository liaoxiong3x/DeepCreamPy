# DeepCreamPy
*Decensoring Hentai with Deep Neural Networks*

*Formerly named DeepMindBreak*

This project applies an implementation of [Image Inpainting for Irregular Holes Using Partial Convolutions](https://arxiv.org/abs/1804.07723) to the problem of hentai decensorship. Using a deep fully convolutional neural network, DeepCreamPy can replace censored artwork in hentai with plausible reconstructions. The user needs to only specify the censored regions.

![Censored, decensored](/readme_images/mermaid_collage.png)

# What's New?
- Decensoring images of ANY size
- Higher quality decensors
- Support for mosaic decensors (still a WIP)
- User interface (still a WIP and not very usable)

# Limitations

The decensorship is intended to ONLY work on color hentai images that have minor to moderate bar censorship of the penis or vagina.

It does NOT work with:
- Black and white images
- Monochrome images
- Hentai containing screentones (e.g. printed hentai)
- Real life porn
- Censorship of nipples
- Censorship of anus
- Animated gifs/videos

In particular, if a vagina or penis is completely censored out, decensoring will be ineffective.

# Dependencies

- Python 3
- TensorFlow 1.10
- Pillow
- argparse

No GPU required! Tested on Ubuntu 16.04 and Windows. (Tensorflow on Windows is compatible with Python 3 and not Python 2.)

Tensorflow, Pillow, and argparse can all be installed with pip.

# Model
Pretrained models can be downloaded from https://drive.google.com/open?id=1byrmn6wp0r27lSXcT9MC4j-RQ2R04P1Z.

Unzip the file into the /models/ folder.

# Usage

## I. Decensoring bar censors

For each image you want to decensor, using image editing software like Photoshop or GIMP to color the areas you want to decensor the green color (0,255,0), which is a very bright green color.

*I strongly recommend you use the pencil tool and NOT the brush tool.*

*If you aren't using the pencil tool, BE SURE TO TURN OFF ANTI-ALIASING on the tool you are using.*

I personally use the wand selection tool with anti-aliasing turned off to select the censored regions. I then expand the selections slightly, pick the color (0,255,0), and use the paint bucket tool on the selection regions.

To expand selections in Photoshop, do Selection > Modify > Expand or Contract.
To expand selections in GIMP, do Select > Grow.

Save these images in the PNG format to the "decensor_input" folder.

### A. Using the Binary

Decensor the images by double-clicking on the decensor file.

### B. Running from scratch

Decensor the images by running

```
$ python decensor.py
```

Decensored images will be saved to the "decensor_output" folder. Decensoring takes a few minutes per image.

## II. Decensoring mosaic censors

To be implemented.

## II. Decensoring with the user interface

To be implemented.

# Troubleshooting
If your decensor output looks like this:
![Bad decensor](/readme_images/mermaid_face_censored_bad_decensor.png)
then the colored regions were not colored correctly.

Make sure you have antialiasing off.

Here are some examples of bad and good colorings:

|Image|Comment|
|--- | --- |
|![Incomplete coloring](/readme_images/mermaid_face_censored_bad_incomplete.png)|Some censored pixels was left uncolored. Expand your selections to fully cover all censored regions.|
|![Bad edges](/readme_images/mermaid_face_censored_bad_edge.png)|Some pixels around the edges of the green regions are not pure green. This will cause the green to bleed into the decensors. Make sure anti-aliasing is off and to use a pencil tool and not a brush tool if possible.|
|![Perfect coloring!](/readme_images/mermaid_face_censored_good.png)|Perfect coloring!|

# To do
- Finish the user interface

Contributions are welcome! Special thanks to StartleStars for contributing code for mosaic decensorship and SoftArmpit for greatly simplifying decensoring!

# License
**I will likely change the license to be more permissive in the future, but I make no guarantees.**

**This work (the code and the model) is under my exclusive copyright. The only right I grant to users is using this work for personal use to decensor hentai. Copying, distribution, and modification is prohibited. Commercial use is prohibited. (Modification of the 6 values of the arguments in config.py is allowed.)**

Example image by Shurajo & AVALANCHE Game Studio under [CC BY 3.0 License](https://creativecommons.org/licenses/by/3.0/). The example image is modified from the original, which can be found [here](https://opengameart.org/content/mermaid).

Neural network code is modified from MathiasGruber's project [Partial Convolutions for Image Inpainting using Keras](https://github.com/MathiasGruber/PConv-Keras), which is an unofficial implementation of the paper [Image Inpainting for Irregular Holes Using Partial Convolutions](https://arxiv.org/abs/1804.07723).

User interface code is modified from Packt's project [Tkinter GUI Application Development Blueprints - Second Edition](https://github.com/PacktPublishing/Tkinter-GUI-Application-Development-Blueprints-Second-Edition).


```
# Copyright (c) 2018 MathiasGruber, Packt
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
```