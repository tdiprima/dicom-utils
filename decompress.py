"""
Convert DICOM Image to an Uncompressed Format

Author: tdiprima
Version: 1.0
License: MIT
"""

__author__ = "tdiprima"
__version__ = "1.0"
__license__ = "MIT"

import pydicom

# Read DICOM file
ds = pydicom.dcmread("img/dicom1.dcm")

# Check whether your images are compressed:
print(f"Transfer Syntax UID: {ds.file_meta.TransferSyntaxUID}")

# If the DICOM file contains compressed pixel data, decompress it
if "PixelData" in ds and ds.file_meta.TransferSyntaxUID.is_compressed:
    ds.decompress()

# Now, you can safely access ds.pixel_array
# image_array = ds.pixel_array
# print(image_array)

print(f"Transfer Syntax UID: {ds.file_meta.TransferSyntaxUID}")
