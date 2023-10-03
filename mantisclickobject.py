import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize
import torch
from matplotlib.widgets import Button

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

def on_click(event):
    if event.xdata is not None and event.ydata is not None:
        x, y = int(event.xdata), int(event.ydata)
        ax = event.inaxes
        image = ax.images[0].get_array()
        if y < 512:  # Only pick colors from the top half (original image)
            picked_color = image[y, x] * 255
            color[0] = (int(picked_color[0]), int(picked_color[1]), int(picked_color[2]))

def update_display():
    for ax, cap in zip(axs, caps):
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
    
    plt.pause(0.01)
    fig.canvas.draw_idle()

fig.canvas.mpl_connect('button_press_event', on_click)

while True:
    update_display()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

for cap in caps:
    cap.release()
cv2.destroyAllWindows()

