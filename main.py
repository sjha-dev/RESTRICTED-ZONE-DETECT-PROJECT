import cv2
from ultralytics import YOLO
import numpy as np
from tkinter import Tk, filedialog
import os
import winsound  # Windows inbuilt sound module
import time

points = []

# Mouse callback function to capture coordinates
def mouse_click(event, x, y, flags, frame):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Point recorded: ({x}, {y})")
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Setup ROI", frame)

def get_restricted_roi(frame):
    # Window ko resizable banane ke liye WINDOW_NORMAL set kiya
    cv2.namedWindow("Setup ROI", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Setup ROI", 960, 540)  # Standard display size
    
    cv2.imshow("Setup ROI", frame)
    cv2.setMouseCallback("Setup ROI", mouse_click, frame)
    print("\n--- RESTRICTED AREA SETUP ---")
    print("1. Mouse se restricted zone ke corners par LEFT CLICK karo (At least 3 points).")
    print("2. Points lagane ke baad keyboard par 'q' dabao setup complete karne ke liye.\n")

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyWindow("Setup ROI")
    return np.array(points)

def get_roi_mask(frame, roi_points):
    mask = np.zeros(frame.shape[:-1], dtype=np.uint8)
    if len(roi_points) >= 3:
        cv2.fillPoly(mask, [np.array(roi_points)], 255)
    return mask

# ----------------- MAIN EXECUTION -----------------

model = YOLO("yolov8n.pt")

root = Tk()
root.withdraw()

input_video_name = filedialog.askopenfilename(
    initialdir=os.getcwd(),
    title="Select Video File",
    filetypes=(("Video files", "*.mp4 *.avi *.mov *.mkv"), ("All files", "*.*"))
)

if not input_video_name:
    print("No file selected. Exiting...")
    exit()

cap = cv2.VideoCapture(input_video_name)

if not cap.isOpened():
    print("Error: Could not open video")
    exit()

ret, frame = cap.read()
if not ret:
    print("Error: Could not read frame")
    cap.release()
    exit()

# Get ROI from user
temp_frame_setup = frame.copy()
restricted_area_roi = get_restricted_roi(temp_frame_setup)

if len(restricted_area_roi) < 3:
    print("Error: Minimum 3 points required for restricted area. Exiting...")
    cap.release()
    cv2.destroyAllWindows()
    exit()

restricted_area_mask = get_roi_mask(frame, restricted_area_roi)

cv2.namedWindow("Restricted Area Mask", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Restricted Area Mask", 960, 540)
cv2.imshow("Restricted Area Mask", restricted_area_mask)
print("Review the mask. Press ANY KEY to start monitoring...")
cv2.waitKey(0)
cv2.destroyWindow("Restricted Area Mask")

print("\n🚀 Monitoring Started! Press 'q' on video window to exit.")

# Main Monitoring Window setup with normal sizing
cv2.namedWindow("Restricted Zone Detection", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Restricted Zone Detection", 960, 540)

last_beep_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, classes=0, conf=0.4)[0]
    alarm_trigger = False

    for box in results.boxes:
        coords = box.xyxy[0].tolist()
        x1, y1, x2, y2 = map(int, coords)

        px_center = int((x1 + x2) / 2)
        py_bottom = y2

        if 0 <= px_center < restricted_area_mask.shape[1] and 0 <= py_bottom < restricted_area_mask.shape[0]:
            if restricted_area_mask[py_bottom, px_center] == 255:
                alarm_trigger = True
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                cv2.putText(frame, 'Person - Danger!', (x1, max(20, y1 - 10)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            else:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, 'Person - Safe', (x1, max(20, y1 - 10)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.polylines(frame, [restricted_area_roi], isClosed=True, color=(0, 0, 255), thickness=2)

    if alarm_trigger:
        cv2.putText(frame, "⚠️ ALARM: RESTRICTED ZONE VIOLATION!", (30, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        current_time = time.time()
        if current_time - last_beep_time > 0.8:
            winsound.Beep(2500, 400)
            last_beep_time = current_time

    cv2.imshow('Restricted Zone Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Execution Finished.")