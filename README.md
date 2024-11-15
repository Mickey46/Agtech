# Agtech - Real-time Computer Vision and Object Detection

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

## Overview
This repository contains Python scripts for various real-time computer vision tasks, inspired by the complex visual system of the mantis shrimp. The code focuses on detecting and interacting with objects in real-time using advanced image processing techniques.

## Table of Contents
- [Installation](#installation)
- [Scripts Overview](#scripts-overview)
- [Usage](#usage)
- [Example Outputs](#example-outputs)
- [License](#license)

## Installation
To use this repository, ensure you have Python 3.x and the required libraries installed.

### Requirements:
- Python 3.x
- OpenCV for video capture and image processing
- NumPy for numerical operations
- Matplotlib for visualizations
- Scikit-Image for image resizing
- Torch for tensor operations (for smoothing filters and processing)

Install the dependencies using pip:
```bash
pip install opencv-python numpy matplotlib scikit-image torch
Scripts Overview
The repository includes several Python scripts for different aspects of the project:

mantisclickobject.py: Click on a live camera feed to pick colors and detect objects based on the selected color.
autocamera.py: Automatically selects available camera indices and starts capturing video from the first available camera.
motion.py: Detects motion in a video feed, useful for object tracking or surveillance applications.
mantisbutton.py: Adds functionality for button interactions in the GUI to control processes during live video analysis.
mantiscolorpick.py: Provides an interactive GUI to pick specific colors in a camera feed for use in detecting similar colors in the image.
mantisshrimplive.py: Simulates the vision abilities of the mantis shrimp, applying real-time filters to enhance colors or detect specific features in the video stream.
Usage
Running the Scripts:
To run mantisclickobject.py:

python mantisclickobject.py
This opens the camera feed. Click on any point in the displayed image to pick the color at that location.
The system will apply filters to enhance objects that match the picked color.
Color Selection:
Click on any part of the live video feed to pick a color.
The algorithm will use smoothing filters to highlight pixels that match the selected color and suppress others.
Example Outputs
(Add images or screenshots here to show example outputs of your scripts.)

License
This repository is licensed under the MIT License - see the LICENSE file for details.

