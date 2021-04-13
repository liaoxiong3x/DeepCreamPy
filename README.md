# DeepCreamPy
*Decensoring Images with Deep Neural Networks. Formerly named DeepMindBreak.*


I looked for the DeepCreamPy binary for windows and didn't find it. So I did a fork and decided to compile. Here is the result:

https://drive.google.com/file/d/1cdisrH_QTsfyd9g_PwRzvONChjVwlMrC/view?usp=sharing

![Censored, decensored](/readme_images/mermaid_collage.png)

## Features
- Decensoring images of ANY size
- Decensoring of ANY shaped censor (e.g. black lines, pink hearts, etc.)
- Higher quality decensors
- Support for mosaic decensors (WIP)
- User interface (WIP)

## Limitations
The decensorship is for color hentai images that have minor to moderate censorship of the penis or vagina. If a vagina or penis is completely censored out, decensoring will be ineffective.

It does NOT work with:
- Black and white/Monochrome image
- Hentai with screentones (e.g. printed hentai)
- Real life porn
- Censorship of nipples
- Censorship of anus
- Animated gifs/videos

## Table of Contents
Setup:
* [Running latest Window 64-bit release](INSTALLATION_BINARY.md)
* [Running code yourself](INSTALLATION.md)

Usage:
* [Decensoring tutorial](USAGE.md)
* [Troubleshooting for poor quality decensors](TROUBLESHOOTING.md)

Miscellaneous:
* [FAQ](FAQ.md)

## To do
- Finish the user interface (estimated November)
- Update model with better quality data (estimated November)
- Add support for black and white images
- Add error log

Follow me on Twitter [@deeppomf](https://twitter.com/deeppomf) for project updates.

Contributions are welcome! Special thanks to IAmTheRedSpy, 0xb8, deniszh, Smethan, mrmajik45, harjitmoe, itsVale, StartleStars, and SoftArmpit!

## License
This project is licensed under GNU Affero General Public License v3.0.

See [LICENSE.txt](LICENSE.txt) for more information about the license.

## Acknowledgements
Example mermaid image by Shurajo & AVALANCHE Game Studio under [CC BY 3.0 License](https://creativecommons.org/licenses/by/3.0/). The example image is modified from the original, which can be found [here](https://opengameart.org/content/mermaid).

Neural network code is modified from MathiasGruber's project [Partial Convolutions for Image Inpainting using Keras](https://github.com/MathiasGruber/PConv-Keras), which is an unofficial implementation of the paper [Image Inpainting for Irregular Holes Using Partial Convolutions](https://arxiv.org/abs/1804.07723). [Partial Convolutions for Image Inpainting using Keras](https://github.com/MathiasGruber/PConv-Keras) is licensed under the MIT license.

User interface code is modified from Packt's project [Tkinter GUI Application Development Blueprints - Second Edition](https://github.com/PacktPublishing/Tkinter-GUI-Application-Development-Blueprints-Second-Edition). [Tkinter GUI Application Development Blueprints - Second Edition](https://github.com/PacktPublishing/Tkinter-GUI-Application-Development-Blueprints-Second-Edition) is licensed under the MIT license.

Data is modified from gwern's project [Danbooru2017: A Large-Scale Crowdsourced and Tagged Anime Illustration Dataset](https://www.gwern.net/Danbooru2017).

See [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md) for full license text of these projects.

## Donations
If you like the work I do, you can donate to me via Paypal: [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=SAM6C6DQRDBAE)
