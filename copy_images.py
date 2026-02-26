import os
import shutil

src_dir = r"C:\Users\vijay\.gemini\antigravity\brain\aeee048a-d2cd-4512-aa7b-ab2634f43834"
dst_dir = r"e:\DOWNLOADS\vijay\vijaypython\.ipynb_checkpoints\cart\static\images"

if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

files_to_copy = {
    "spinach_jpg_1771928678187.png": "spinach.png",
    "apples_jpg_1771928879783.png": "apples.png"
}

for src_name, dst_name in files_to_copy.items():
    src_path = os.path.join(src_dir, src_name)
    dst_path = os.path.join(dst_dir, dst_name)
    if os.path.exists(src_path):
        shutil.copy(src_path, dst_path)
        print(f"Copied {src_name} to {dst_name}")
    else:
        print(f"Source {src_name} not found.")
