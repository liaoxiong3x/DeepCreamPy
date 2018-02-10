# DeepMindBreak
Decensoring Hentai with Deep Neural Networks

This project is a proof of concept that hentai can be decensored with deep learning. 

Please note research is ongoing, and the neural network works ONLY with color images and minor bar censorship.

# Dependencies

- Python 2
- TensorFlow 1.5
- Pillow

# Model
Link coming soon

# Usage

## I. Decensoring hentai

The decensorship process is fairly involved. A user interface will eventually be released to streamline the process.

Using image editing software like Photoshop or GIMP, crop 128 x 128 size images containing the censored regions from your images and save them as new ".png" images. For each 128 x 128 cropped image, color the censored regions [tbd].

Move the cropped images to []. Run the command 

```
$ python decensor.py
```

Decensored images will be saved to the "output" directory.

Paste the decensored images back into the original image.

## II. Prepare the training data

Put the images for training the "data/images" directory and convert images to npy format.

```
$ cd data
$ python to_npy.py
```

The dataset will not be released. I do not want to risk trouble for distributing copyrighted pornographic material.

# To do
- Add a user interface
- Incorporate GAN loss into training

Contributions are welcome!

# License

Model is under CC BY-NC 3.0 License

Code is under MIT License

Copyright (c) 2018 tadax

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