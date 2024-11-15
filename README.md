Agtech - Real-time Computer Vision and Object Detection
Overview
This repository contains Python scripts for various real-time computer vision tasks, inspired by the complex visual system of the mantis shrimp. The code focuses on detecting and interacting with objects in live video streams. The project aims to mimic the mantis shrimp's advanced vision capabilities, such as detecting subtle details in images that may be camouflaged or hidden.

The scripts in this repository include:

Real-time camera input handling
Interactive color picking for object detection
Image processing techniques to detect and track objects
Visualization and user interaction with detected objects
Table of Contents
Installation
Scripts Overview
Usage
Example Outputs
License
Installation
To use this repository, make sure you have Python 3.x and the required libraries installed.

Requirements:
Python 3.x
OpenCV for video capture and image processing
NumPy for numerical operations
Matplotlib for visualizations
Scikit-Image for image resizing
Torch for tensor operations (for smoothing filters and processing)
Install the dependencies using pip:
bash
Copy code
pip install opencv-python numpy matplotlib scikit-image torch
Scripts Overview
The repository includes several Python scripts for different aspects of the project:

mantisclickobject.py: This script allows users to click on a live camera feed to pick colors and detect objects based on the selected color. It uses OpenCV to capture the video feed and Matplotlib for visualizing the interaction.

autocamera.py: This script automatically selects available camera indices and starts capturing video from the first available camera.

motion.py: This script detects motion in a video feed, useful for object tracking or surveillance applications.

mantisbutton.py: Adds functionality for button interactions in the GUI (Graphical User Interface) to control processes during live video analysis.

mantiscolorpick.py: Provides an interactive GUI to pick specific colors in a camera feed for use in detecting similar colors in the image.

mantisshrimplive.py: A live feed script that simulates the vision abilities of the mantis shrimp, applying real-time filters to enhance colors or detect specific features in the video stream.

Usage
Running the Scripts:
mantisclickobject.py
Run the script to open the camera feed.
Click on any point in the displayed image to pick the color at that location.
The system will apply filters to enhance objects that match the picked color.
Example for executing the script:
bash
Copy code
python mantisclickobject.py
Color Selection:
Click on any part of the live video feed to pick a color.
The algorithm will use smoothing filters to highlight pixels that match the selected color and suppress others.

License
This repository is licensed under the MIT License - see the LICENSE file for details.

