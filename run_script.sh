#!/bin/bash 

script_dir="$(dirname "$(realpath "$0")")"

cd "$script_dir"

python3 minimize_and_crop.py
