import cv2
import time

cap = cv2.VideoCapture('rtsp://danila:admin@192.168.1.24/V_ENC_000', cv2.CAP_FFMPEG)

n = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    cv2.imwrite(f'./night/{n}.jpg', cv2.rotate(frame, cv2.ROTATE_180))
    n += 1
    time.sleep(60)