#!/usr/bin/env python3

# functions.py
import os
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageOps

ratio = 5 / 4

def is_image_file(file_path):
    try:
        Image.open(file_path).close()
        return True
    except:
        return False

def extract_number(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group(0)) if match else float('inf')

def create_output_directory(base_dir):
    base_name = "output"
    i = 1
    while True:
        new_dir = os.path.join(base_dir, f"{base_name} {i}")
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
            return new_dir
        i += 1

def process_file(file_name, file_type, index, input_directory, output_directory, process_type="crop"):
    print(f"{process_type.capitalize()}ing", file_name)
    input_path = os.path.join(input_directory, file_name)
    output_name = file_name if process_type == "minimize" else f"{index}_{file_type.lower()}{os.path.splitext(file_name)[1]}"
    output_path = os.path.join(output_directory, output_name)

    if process_type == "crop":
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', input_path,
            '-vf', f'crop=in_w:in_w*{ratio}',
            '-c:a', 'copy',
            output_path
        ]
    else:
        ffmpeg_cmd = [
            'ffmpeg', '-y',
            '-i', input_path,
            '-vf', 'scale=480:-2',
            '-c:a', 'copy',
            output_path
        ]
    subprocess.run(ffmpeg_cmd)
    return output_path

def process_directory(input_directory, output_directory, process_type="crop"):
    files = os.listdir(input_directory)
    images = sorted((f for f in files if is_image_file(os.path.join(input_directory, f))), key=extract_number)
    videos = sorted((f for f in files if not is_image_file(os.path.join(input_directory, f)) and not f.startswith('.')), key=extract_number)

    if process_type == "minimize":
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_file, f, 'P' if is_image_file(os.path.join(input_directory, f)) else 'V', 0, input_directory, output_directory, process_type) for f in images + videos]
            for future in as_completed(futures):
                future.result()
    else:
        with ThreadPoolExecutor() as executor:
            futures = []
            index = 1
            paired_files = zip(images, videos)
            for img, vid in paired_files:
                futures.append(executor.submit(process_file, img, 'P', index, input_directory, output_directory, process_type))
                futures.append(executor.submit(process_file, vid, 'V', index, input_directory, output_directory, process_type))
                index += 1
            for future in as_completed(futures):
                future.result()

def crop_dir(input_directory, base_output_directory):
    output_directory = create_output_directory(base_output_directory)
    process_directory(input_directory, output_directory, "crop")
    
    input_files = os.listdir(input_directory)
    for file in input_files:
        file_path = os.path.join(input_directory, file)
        try:
            os.remove(file_path)
            print(f"Deleted {file} from input directory")
        except Exception as e:
            print(f"Error deleting {file}: {e}")

    print_folder = os.path.join(output_directory, "Print")
    os.makedirs(print_folder, exist_ok=True)
    
    for file in os.listdir(output_directory):
        if is_image_file(os.path.join(output_directory, file)):
            src_path = os.path.join(output_directory, file)
            dst_path = os.path.join(print_folder, file)
            shutil.copy(src_path, dst_path)
            print(f"Copied {file} to {print_folder}")

def minimize_dir(input_directory, output_directory):
    process_directory(input_directory, output_directory, "minimize")
    for file in os.listdir(input_directory):
        os.remove(os.path.join(input_directory, file))