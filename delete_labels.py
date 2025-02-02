import os

def remove_yolo_labels(label_ids, directory):
    """
    Remove lines from YOLO label files where label_id matches any id from label_ids list
    
    Args:
        label_ids (list): List of label IDs to remove
        directory (str): Path to directory containing label files
    """
    # Convert label_ids to strings for comparison
    label_ids = [str(id) for id in label_ids]
    
    # Walk through all files in directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):  # Assuming YOLO labels are in .txt files
                file_path = os.path.join(root, file)
                
                # Read all lines from file
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                
                # Keep only lines where label_id is not in label_ids
                filtered_lines = []
                for line in lines:
                    label_id = line.strip().split()[0]
                    if label_id not in label_ids:
                        filtered_lines.append(line)
                
                # Write filtered lines back to file
                with open(file_path, 'w') as f:
                    f.writelines(filtered_lines)
                
                # Print progress
                print(f"Processed: {file_path}")


import os

def replace_yolo_label_id(old_id, new_id, directory):
    """
    Replace specific label_id with new_id in YOLO label files
    
    Args:
        old_id (int): Label ID to be replaced
        new_id (int): New label ID to replace with
        directory (str): Path to directory containing label files
    """
    # Convert IDs to strings for comparison
    old_id_str = str(old_id)
    new_id_str = str(new_id)
    
    # Walk through all files in directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                modified = False
                
                # Read all lines from file
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                
                # Process each line
                new_lines = []
                for line in lines:
                    parts = line.strip().split()
                    if parts and parts[0] == old_id_str:
                        # Replace the label ID and keep the rest of the line unchanged
                        new_line = new_id_str + ' ' + ' '.join(parts[1:]) + '\n'
                        new_lines.append(new_line)
                        modified = True
                    else:
                        new_lines.append(line)
                
                # Write back to file only if modifications were made
                if modified:
                    with open(file_path, 'w') as f:
                        f.writelines(new_lines)
                    print(f"Modified: {file_path}")

# Example usage
if __name__ == "__main__":
    # List of label IDs to remove
    ids_to_remove =[1, 3]  # Replace with your label IDs
    
    # Directory containing label files
    label_directory = ["/home/danila/check_parking_place/data/train/labels", "/home/danila/check_parking_place/data/valid/labels",
                       "/home/danila/check_parking_place/data/test/labels"]  # Replace with your directory path
    for i in label_directory:
        remove_yolo_labels(ids_to_remove, i)
        replace_yolo_label_id(2, 0, i)