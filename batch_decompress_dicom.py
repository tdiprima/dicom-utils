"""
Detects pixel data in a batch of DICOM files and decompresses those requiring decompression.

Author: tdiprima
Version: 1.0
License: MIT
"""

__author__ = "tdiprima"
__version__ = "1.0"
__license__ = "MIT"

import os
from pathlib import Path

from pydicom import dcmread
from pydicom.filewriter import write_file


def detect_pixel_data(dicom_file):
    try:
        ds = dcmread(dicom_file)
        if "PixelData" in ds:
            print(f"{dicom_file}: Pixel Data is present.")
            return True
        else:
            print(f"{dicom_file}: No Pixel Data found.")
            return False
    except Exception as e:
        print(f"Error reading {dicom_file}: {e}")
        return False


def decompress_dicom(dicom_file, output_dir):
    try:
        ds = dcmread(dicom_file)
        if ds.file_meta.TransferSyntaxUID.is_compressed:
            print(f"Decompressing: {dicom_file}")
            ds.decompress()
            output_path = os.path.join(output_dir, os.path.basename(dicom_file))
            write_file(output_path, ds)
            print(f"Decompressed file saved to: {output_path}")
        else:
            print(f"{dicom_file} is already uncompressed.")
    except Exception as e:
        print(f"Error decompressing {dicom_file}: {e}")


def process_dicom_directory(input_dir, output_dir):
    Path(output_dir).mkdir(exist_ok=True, parents=True)
    for root, _, files in os.walk(input_dir):
        for file in files:
            dicom_path = os.path.join(root, file)
            if dicom_path.endswith(".dcm"):
                has_pixel_data = detect_pixel_data(dicom_path)
                if has_pixel_data:
                    decompress_dicom(dicom_path, output_dir)


if __name__ == "__main__":
    input_directory = "img"
    output_directory = "decompressed"
    process_dicom_directory(input_directory, output_directory)
