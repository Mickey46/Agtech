import cv2
import numpy as np
import tensorflow.compat.v2 as tf
import tensorflow_hub as hub

def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        exit()

    cap.release()
    return frame

def classify_image(image, model, labels):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    predictions = model(img)
    predicted_index = np.argmax(predictions)
    predicted_label = labels[predicted_index]
    return predicted_label

def load_labels(csv_file):
    labels = np.loadtxt(csv_file, dtype=str, delimiter=',')
    return labels

def main():
    model = hub.KerasLayer('https://tfhub.dev/google/aiy/vision/classifier/plants_V1/1')
    
    # Path to the CSV file containing label mappings
    csv_file = './aiy_plants_V1_labelmap.csv'

    labels = load_labels(csv_file)

    while True:
        frame = capture_image()
        label = classify_image(frame, model, labels)
        print(label)

        cv2.imshow('Image', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

