#!/bin/bash

# check_jpeg_dicom.sh
# Script to check if a DICOM file is JPEG-compressed.

# List of JPEG-compressed Transfer Syntax UIDs
JPEG_COMPRESSED_UIDS=(
    "1.2.840.10008.1.2.4.50"
    "1.2.840.10008.1.2.4.51"
    "1.2.840.10008.1.2.4.57"
    "1.2.840.10008.1.2.4.70"
    "1.2.840.10008.1.2.4.90"
    "1.2.840.10008.1.2.4.91"
)

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <DICOM file>"
    exit 1
fi

# File parameter
DICOM_FILE=$1

# Verify if the file exists
if [ ! -f "$DICOM_FILE" ]; then
    echo "Error: File '$DICOM_FILE' not found."
    exit 2
fi

dcmdump "$DICOM_FILE" | grep "TransferSyntaxUID"

# Extract the Transfer Syntax UID from the DICOM file
# This assumes `dcmdump` (part of DCMTK) is installed
TRANSFER_SYNTAX=$(dcmdump "$DICOM_FILE" | grep "TransferSyntaxUID" | awk -F'\\[|\\]' '{print $2}')

# Check if the extracted UID matches any of the JPEG-compressed UIDs
for JPEG_UID in "${JPEG_COMPRESSED_UIDS[@]}"; do
    if [ "$TRANSFER_SYNTAX" == "$JPEG_UID" ]; then
        echo "The file '$DICOM_FILE' is JPEG-compressed."
        exit 0
    fi
done


# If no match is found
echo "The file might be JPEG-compressed. Check dcmdump output."
exit 0
