#!/bin/bash
# This script streamlines the installation of OpenCV, Tesseract, and other necessary tools.

# Function to check and install a package if missing
install_if_missing() {
    if ! dpkg -l | grep -q $1; then
        echo "Installing $1..."
        sudo apt update
        sudo apt install -y $1
    else
        echo "$1 is already installed."
    fi
}

# Install Tesseract OCR
echo "Setting up Tesseract OCR..."
install_if_missing tesseract-ocr
install_if_missing libtesseract-dev

# Install OpenCV dependencies
echo "Setting up OpenCV dependencies..."
install_if_missing python3-opencv
install_if_missing libopencv-dev
install_if_missing openjdk-11-jdk

# Install pip and Python libraries
echo "Setting up Python environment..."
install_if_missing python3-pip
pip3 install --upgrade pip
pip3 install pydicom

# Verify installations
echo "Verifying installations..."
tesseract --version
python3 -c "import cv2; print('OpenCV version:', cv2.__version__)"
python3 -c "import pydicom; print('PyDICOM version:', pydicom.__version__)"

echo "Setup completed successfully!"
