import os
import csv

# Define your image base directory. CHANGE IT TO MATCH YOURS!!!
base_dir = "/Users/Brian/Desktop/tntech/CSC-4240/ai-project/Data"

# Define your image folders
folders = ["Zebra", "Buffalo", "Rhino", "Elephant"]

# CSV file to create
csv_file = os.path.join(base_dir, "image_data.csv")

# Write to the CSV file
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["FilePath", "Label"])  # Column headers

    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        for filename in os.listdir(folder_path):
            if filename.endswith(".jpg"):
                # Construct the full path to the image
                full_path = os.path.join(folder_path, filename)
                # Write the full path and the label
                writer.writerow([full_path, folder])
