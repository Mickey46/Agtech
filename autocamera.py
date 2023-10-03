import cv2
import matplotlib.pyplot as plt

def get_available_camera_indices(max_check=10):
    available_indices = []
    for index in range(max_check):
        cap = cv2.VideoCapture(index)
        ret, _ = cap.read()
        if ret:
            available_indices.append(index)
        cap.release()
    return available_indices

camera_indices = get_available_camera_indices()
camera_indices = camera_indices[:5]

caps = [cv2.VideoCapture(index) for index in camera_indices]

rows = len(camera_indices) // 5 + (len(camera_indices) % 5 > 0)
fig, axs = plt.subplots(rows, min(len(camera_indices), 5))

if rows == 1 or len(camera_indices) == 1:
    axs = [axs]  # Ensure axs is always a list of lists.

try:
    while True:
        for idx, cap in enumerate(caps):
            ret, frame = cap.read()
            if ret:
                row, col = divmod(idx, 5)
                axs[row][col].imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
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

