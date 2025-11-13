import os

folder = r"C:\Users\You\Desktop\files"

files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

for i, filename in enumerate(files, start=1):
    ext = os.path.splitext(filename)[1]
    new_name = f"file_{i}{ext}"
    src = os.path.join(folder, filename)
    dst = os.path.join(folder, new_name)

    # Prevent overwriting if name already exists
    if os.path.exists(dst):
        print(f"Skipping {filename}: {new_name} already exists.")
        continue

    os.rename(src, dst)

print("Renaming completed.")

