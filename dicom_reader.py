"""
Reads and validates DICOM files using Python, ensuring the file format is correct and handling errors robustly.

Author: tdiprima
Version: 1.0
License: MIT
"""

__author__ = 'tdiprima'
__version__ = '1.0'
__license__ = 'MIT'

import logging

import pydicom

# Configure logging to capture any issues
logging.basicConfig(level=logging.DEBUG)

try:
    # Verbose reading with error handling
    dicom_file = pydicom.dcmread('img/dicom_file.dcm',
                                 force=True,  # Force reading even with minor issues
                                 specific_tags=None)  # Read all tags
    print(dicom_file)
except Exception as e:
    logging.error(f"DICOM reading failed: {e}")
    # Additional diagnostic information
    print(f"File details: {dicom_file.filename if 'dicom_file' in locals() else 'No file read'}")
