# Installation

## Download Prebuilt Binaries
You can download the latest release [here](https://github.com/deeppomf/DeepCreamPy/releases/latest) or find all previous releases [here](https://github.com/deeppomf/DeepCreamPy/releases).
Binary only available for Windows 64-bit.

## Run Code Yourself
If you want to run the code yourself, you can clone this repo and download the model from https://drive.google.com/open?id=1byrmn6wp0r27lSXcT9MC4j-RQ2R04P1Z. Unzip the file into the /models/ folder.

### Dependencies (for running the code yourself)
- Python 3.6.7
- TensorFlow 1.10
- Keras 2.2.4
- Pillow
- h5py

No GPU required! Tested on Ubuntu 16.04 and Windows. Tensorflow on Windows is compatible with Python 3 and not Python 2. Tensorflow is not compatible with Python 3.7.

Tensorflow, Keras, Pillow, and h5py can all be installed by running in the command line

```
$ pip install -r requirements.txt
```

If you experience this error:

```
ModuleNotFoundError: No module named '_pywrap_tensorflow_internal'
```
See https://github.com/deeppomf/DeepCreamPy/issues/26#issuecomment-434043166 for alternative install instructions.
