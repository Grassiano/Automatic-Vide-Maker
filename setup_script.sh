#!/bin/bash

# Check if Homebrew exists. If not, install it.
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew is already installed."
fi

# Check if Python 3.11 and pip exist. If not, install them.
if ! command -v python3.11 &> /dev/null; then
    echo "Installing Python 3.11..."
    brew install python@3.11
else
    echo "Python 3.11 is already installed."
fi

if ! command -v pip3 &> /dev/null; then
    echo "Installing pip for Python 3.11..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3.11 get-pip.py
    rm get-pip.py
else
    echo "pip for Python 3.11 is already installed."
fi

# Check if ffmpeg exists. If not, install it.
if ! command -v ffmpeg &> /dev/null; then
    echo "Installing ffmpeg..."
    brew install ffmpeg
else
    echo "ffmpeg is already installed."
fi

# Install the pillow library using pip (or pip3)
echo "Installing pillow library..."
pip3 install pillow

# Give executable permissions to a list of files
files=("script1.sh" "script2.sh" "script3.sh") # Add your list of file names here

for file in "${files[@]}"; do
    if [[ -e "$file" ]]; then
        chmod +x "$file"
        echo "Added executable permissions to $file."
    else
        echo "$file does not exist."
    fi
done

echo "Script execution completed."

