import cv2
import matplotlib.pyplot as plt

# Initialize the USB camera (0 indicates the first available camera)
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the frame using Matplotlib
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.axis('off')  # Turn off axis numbers and ticks
    plt.pause(0.01)  # Pause to display the updated image
    plt.clf()  # Clear the previous plot

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the Matplotlib window
cap.release()
cv2.destroyAllWindows()

