from ultralytics import YOLO

model = YOLO('yolov10s.pt')

model.train(data='/home/danila/check_parking_place/data/data.yaml', epochs=10, imgsz=640, batch=2)