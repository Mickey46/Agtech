import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize
import torch
from matplotlib.widgets import Button, Slider

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

current_index = [0]
color = [(255, 255, 255)]  # Default white color

fig, axs = plt.subplots(1, 2, figsize=(15, 7.5))
fig.subplots_adjust(bottom=0.25)

# Callback functions
def next_camera(event):
    current_index[0] = (current_index[0] + 1) % len(caps)
    update_display()

def sliders_update(val):
    color[0] = (int(color_sliders['Red'].val), int(color_sliders['Green'].val), int(color_sliders['Blue'].val))
    update_display()

def update_display():
    axs[0].cla()
    axs[1].cla()

    ret, frame = caps[current_index[0]].read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = resize(frame_rgb, (512, 512))
        
        image_batch = np.repeat(frame_resized[np.newaxis, ...], 1, axis=0)
        img_tensor_batch = torch.tensor(image_batch)
        target_color_tensor_batch = torch.tensor(np.array([color[0]])).float()
        
        filtered = smooth_filter(img_tensor_batch, target_color_tensor_batch, 100.0).cpu().numpy()[0]
        
        axs[0].imshow(frame_rgb)
        axs[0].axis('off')
        axs[1].imshow(filtered)
        axs[1].axis('off')

    plt.draw()

# RGB sliders
color_sliders = {}
axcolor = 'lightgoldenrodyellow'
ax_red = fig.add_axes([0.15, 0.01, 0.65, 0.03], facecolor=axcolor)
ax_green = fig.add_axes([0.15, 0.05, 0.65, 0.03], facecolor=axcolor)
ax_blue = fig.add_axes([0.15, 0.09, 0.65, 0.03], facecolor=axcolor)

color_sliders['Red'] = Slider(ax_red, 'Red', 0, 255, valinit=color[0][0], valfmt='%1.0f')
color_sliders['Green'] = Slider(ax_green, 'Green', 0, 255, valinit=color[0][1], valfmt='%1.0f')
color_sliders['Blue'] = Slider(ax_blue, 'Blue', 0, 255, valinit=color[0][2], valfmt='%1.0f')

color_sliders['Red'].on_changed(sliders_update)
color_sliders['Green'].on_changed(sliders_update)
color_sliders['Blue'].on_changed(sliders_update)

# Next camera button
next_button_ax = fig.add_axes([0.85, 0.05, 0.1, 0.075])
next_button = Button(next_button_ax, 'Next Camera')
next_button.on_clicked(next_camera)

update_display()
plt.show()

