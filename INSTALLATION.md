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

## Run Code Yourself on CPUs that don't support AVX instructions

CPUs that don't support AVX instructions may experience this error when using the above install instructions:

```
ModuleNotFoundError: No module named '_pywrap_tensorflow_internal'
```

Follow these alternate install instructions:

1. Start from a clean Python 3.6.7 install.
2. Download a version of tensorflow that do support AVX instructions from (https://github.com/fo40225/tensorflow-windows-wheel/tree/master/1.10.0/py36/CPU/sse2). I assume you picked tensorflow-1.10.0-cp36-cp36m-win_amd64.whl for 64-bit and the other for 32-bit computers.
3. Open the command line in the same directory as the file downloaded in step 2. Run

```
pip install tensorflow-1.10.0-cp36-cp36m-win_amd64.whl
```

or

```
pip install tensorflow-1.10.0-cp36-cp36m-win32.whl
```
depending on what you installed in step 2.
4. Open the command line in the directory of "DeepCreamPy-master" and run
```
pip install -r requirements.txt
```

Instructions are from https://github.com/deeppomf/DeepCreamPy/issues/26#issuecomment-434043166.
