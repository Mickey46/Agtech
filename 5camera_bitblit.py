import cv2
import numpy as np
import pygame
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
color = [(255, 255, 255)]  # Default white color



import pygame
from pygame import surfarray

pygame.init()

w = 1280
h = 256
display = pygame.display.set_mode((w, h))



running = True
while running:
    x_offset = 0  # to position each camera feed
    for cap in caps:
        ret, frame = cap.read()
        if ret:
            # Convert the frame from BGR to RGB (as pygame uses RGB)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Apply any processing here (like smooth_filter)
            # For this example, I'm just resizing and displaying
            
            # Resize frame to match the individual camera feed dimensions
            frame_resized = cv2.resize(frame_rgb, (256, 256))
            # Blit the frame at the correct position
            display.blit(surfarray.make_surface(frame_resized), (x_offset, 0))
            x_offset += 256  # move the position for the next camera feed
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

for cap in caps:
    cap.release()
pygame.quit()
