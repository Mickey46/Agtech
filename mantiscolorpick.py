import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize
import torch
from matplotlib.widgets import Button
import tkinter as tk
from tkinter import colorchooser

def get_available_camera_indices(max_check=10):
    available_indices = []
    for index in range(max_check):
        cap = cv2.VideoCapture(index)
        ret, _ = cap.read()
        if ret:
            available_indices.append(index)
        cap.release()
    return available_indices

def smooth_filter(img_tensor_batch, target_colors, tolerance):
    distances = torch.norm(img_tensor_batch * 255 - target_colors[:, None, None, :], dim=-1)
    weights = (1 - torch.clamp(distances / tolerance, 0, 1)).unsqueeze(-1)
    return img_tensor_batch * weights 

camera_indices = get_available_camera_indices()
camera_indices = camera_indices[:5]
caps = [cv2.VideoCapture(index) for index in camera_indices]
color = [(255, 255, 255)]  # Default white color

fig, axs = plt.subplots(1, len(camera_indices), figsize=(5 * len(camera_indices), 10))

# Callback functions
def pick_color(event):
    root = tk.Tk()
    root.withdraw()
    color_tuple = colorchooser.askcolor(title ="Choose Filter Color")
    color[0] = tuple(int(val) for val in color_tuple[0])
    update_display()

def update_display():
    for ax, cap in zip(axs, caps):
        ax.cla()
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = resize(frame_rgb, (512, 512))
            
            image_batch = np.repeat(frame_resized[np.newaxis, ...], 1, axis=0)
            img_tensor_batch = torch.tensor(image_batch)
            target_color_tensor_batch = torch.tensor(np.array([color[0]])).float()
            
            filtered = smooth_filter(img_tensor_batch, target_color_tensor_batch, 100.0).cpu().numpy()[0]
            
            stacked_image = np.vstack([frame_resized, filtered])
            ax.imshow(stacked_image)
            ax.axis('off')

    plt.draw()

# Pick Color button
pick_color_button_ax = fig.add_axes([0.45, 0.01, 0.1, 0.05])
pick_color_button = Button(pick_color_button_ax, 'Pick Color')
pick_color_button.on_clicked(pick_color)

update_display()
plt.show()

