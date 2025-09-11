import os

folder = "C:/Users/You/Desktop/files"
for i, filename in enumerate(os.listdir(folder), start=1):
    ext = os.path.splitext(filename)[1]
    new_name = f"file_{i}{ext}"
    os.rename(os.path.join(folder, filename), os.path.join(folder, new_name))
