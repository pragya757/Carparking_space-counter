import cv2
import cvzone
import numpy as np
import pickle
import os

# Specify the path to the video file
video_path = r"C:\Users\PRAGYA\Downloads\Parking_Space_Counter-main\CarParkProject\carPark.mp4"

# Check if the video file exists
if not os.path.exists(video_path):
    print("Error: Video file not found at the specified path.")
    exit()

cap = cv2.VideoCapture(video_path)

# Check if the video capture was successful
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Load the parking space positions
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)
    
width, height = 107, 48

def checkParkingSpace(imgpro):
    space_counter = 0
    
    for pos in posList:
        x, y = pos
        imgCrop = imgpro[y:y+height, x:x+width]
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x, y+height-3), scale=1, thickness=2, offset=0, colorR=(0, 0, 255))
        
        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            space_counter += 1
        else: 
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        
    cvzone.putTextRect(img, f'Free: {space_counter}/{len(posList)}', (100, 50), scale=3, thickness=5, offset=20, colorR=(0, 200, 0))

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    success, img = cap.read()
    if not success:
        print("Error: Failed to read a frame from the video.")
        break
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreashold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    kernel = np.ones((3, 3), np.uint8)
    imgMedian = cv2.medianBlur(imgThreashold, 5)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
    
    checkParkingSpace(imgDilate)
    
    cv2.imshow("Parking Space Status", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
