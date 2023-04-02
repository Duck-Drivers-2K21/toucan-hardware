# toucan-hardware

This repository contains all the necessary hardware interfacing functionality to support our application, _parkn_, which uses Computer Vision and Deep Learning to detect vacant parking spaces in crowded urban areas.

The project includes an embedded application which utilizes a Raspberry Pi along with a servo motor to give your camera a better field of view of the road.

## Get started

Required hardware:
- A camera
- Raspberry Pi (optional)
- Servo Motor (optional)

### Setup
Run `setup.sh` to setup the virtual environment and install the requirements. Please note this project requires `venv` to be installed.

If you wish to use our embedded solution, carry out this process on your Raspberry Pi and add the following argument `setup.sh -rpi`. You will also have to set `RPI=True` in `main.py` to import the correct modules.

### Running Toucan
Run `run.sh` to activate venv and start script
