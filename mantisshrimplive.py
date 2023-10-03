import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize
import torch

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

rows = len(camera_indices) // 5 + (len(camera_indices) % 5 > 0)
fig, axs = plt.subplots(rows, min(len(camera_indices), 5))

if rows == 1 or len(camera_indices) == 1:
    axs = [axs]

try:
    while True:
        for idx, cap in enumerate(caps):
            ret, frame = cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_resized = resize(frame_rgb, (512, 512))
                
                # Create a batch of images
                image_batch = np.repeat(frame_resized[np.newaxis, ...], 1, axis=0)
                random_color = (np.random.rand(1, 3) * 255).astype(int)
                img_tensor_batch = torch.tensor(image_batch)
                target_color_tensor_batch = torch.tensor(random_color).float()
                
                filtered = smooth_filter(img_tensor_batch, target_color_tensor_batch, 100.0).cpu().numpy()[0]
                
                row, col = divmod(idx, 5)
                axs[row][col].imshow(filtered)
                axs[row][col].axis('off')

        plt.pause(0.01)

        for ax_row in axs:
            for ax in ax_row:
                ax.cla()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    for cap in caps:
        cap.release()
    cv2.destroyAllWindows()
    plt.close()

