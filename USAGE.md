## Usage
### I. Decensoring bar censors

For each image you want to decensor, using image editing software like Photoshop or GIMP to color the areas you want to decensor the green color (0,255,0), which is a very bright green color.

*I strongly recommend you use the pencil tool and NOT the brush tool.*

*If you aren't using the pencil tool, BE SURE TO TURN OFF ANTI-ALIASING on the tool you are using.*

I personally use the wand selection tool with anti-aliasing turned off to select the censored regions. I then expand the selections slightly, pick the color (0,255,0), and use the paint bucket tool on the selected regions.

To expand selections in Photoshop, do Selection > Modify > Expand or Contract.
To expand selections in GIMP, do Select > Grow.

Save these images in the PNG format to the "decensor_input" folder.

#### A. Using the binary

Decensor the images by double-clicking on the decensor file.

#### B. Running from scratch

Decensor the images by running

```
$ python decensor.py
```

Decensored images will be saved to the "decensor_output" folder. Decensoring takes a few minutes per image.

### II. Decensoring mosaic censors

As with decensoring bar censors, perform the same steps of coloring the censored regions green and putting the colored image into the "decensor_input" folder.

In addition, move the original, uncolored images into the "decensor_input_original" folder. Ensure each original image has the same names as their corresponding colored version in the "decensor_input" folder.

For example, if the original image is called "mermaid.jpg," then you want to put this image in the "decensor_input_original" folder and, after you colored the censored regions, name the colored image "mermaid.png" and move it to the "decensor_input" folder.

#### A. Using the binary

Decensor the images by double-clicking on the decensor_mosaic file.

#### B. Running from scratch

Decensor the images by running

```
$ python decensor.py --is_mosaic=True
```

Decensored images will be saved to the "decensor_output" folder. Decensoring takes a few minutes per image.

### III. Decensoring with the user interface

To be implemented.