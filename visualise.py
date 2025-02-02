import cv2
import os
import numpy as np
from pathlib import Path

def visualize_yolo_labels(images_dir, labels_dir, class_names=None):
    """
    Visualize YOLO labels on images
    
    Args:
        images_dir (str): Directory containing images
        labels_dir (str): Directory containing YOLO label files
        class_names (list): List of class names (optional)
    """
    # If class names are not provided, use indices as names
    if class_names is None:
        class_names = {}
    
    # Generate random colors for each class
    np.random.seed(42)
    colors = np.random.randint(0, 255, size=(len(class_names) + 1000, 3), dtype=np.uint8)
    
    # Get all image files
    image_files = []
    for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
        image_files.extend(list(Path(images_dir).glob(f'**/*{ext}')))
    
    for img_path in image_files:
        # Get corresponding label file
        label_path = Path(labels_dir) / f"{img_path.stem}.txt"
        
        if not label_path.exists():
            print(f"No label file found for {img_path}")
            continue
            
        # Read image
        img = cv2.imread(str(img_path))
        if img is None:
            print(f"Could not read image: {img_path}")
            continue
            
        height, width = img.shape[:2]
        
        # Read labels
        with open(label_path, 'r') as f:
            lines = f.readlines()
        
        # Draw each label
        for line in lines:
            try:
                class_id, x_center, y_center, w, h = map(float, line.strip().split())
                class_id = int(class_id)
                
                # Convert YOLO coordinates to pixel coordinates
                x1 = int((x_center - w/2) * width)
                y1 = int((y_center - h/2) * height)
                x2 = int((x_center + w/2) * width)
                y2 = int((y_center + h/2) * height)
                
                # Ensure coordinates are within image boundaries
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(width, x2), min(height, y2)
                
                # Get color for class
                color = tuple(map(int, colors[class_id]))
                
                # Draw rectangle
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                
                # Add label text
                label_text = class_names.get(class_id, f"Class {class_id}")
                cv2.putText(img, label_text, (x1, y1 - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
            except ValueError as e:
                print(f"Error processing line in {label_path}: {line.strip()}")
                continue
        
        # Show image
        cv2.imshow(f"Image: {img_path.name}", img)
        
        # Wait for key press
        key = cv2.waitKey(0)
        
        # Close window
        cv2.destroyAllWindows()
        
        # Break if 'q' is pressed
        if key == ord('q'):
            break

# Example usage
if __name__ == "__main__":
    # Directory paths
    images_dir = "/home/danila/check_parking_place/data/test/images"  # Replace with your images directory
    labels_dir = "/home/danila/check_parking_place/data/test/labels"  # Replace with your labels directory
    
    # Optional: Define class names
    class_names = {
        0: "ocupas"
        # Add more class names as needed
    }
    
    visualize_yolo_labels(images_dir, labels_dir, class_names)