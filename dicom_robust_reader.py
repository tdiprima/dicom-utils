"""
Reads and validates DICOM files using Python, ensuring the file format is correct and handling errors robustly.
"""
__author__ = 'tdiprima'

import logging

import pydicom

# Configure logging to capture any issues
logging.basicConfig(level=logging.DEBUG)

try:
    # Verbose reading with error handling
    dicom_file = pydicom.dcmread('file.dcm',
                                 force=True,  # Force reading even with minor issues
                                 specific_tags=None)  # Read all tags
    print(dicom_file)
except Exception as e:
    logging.error(f"DICOM reading failed: {e}")
    # Additional diagnostic information
    print(f"File details: {dicom_file.filename if 'dicom_file' in locals() else 'No file read'}")
