#!/bin/sh

python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install Pillow

echo "Activate your virtual environment by running:"
echo "'. venv/bin/activate'" # Newline for easy copy and paste
