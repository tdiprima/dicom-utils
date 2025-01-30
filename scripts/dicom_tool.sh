#!/bin/bash
# ./dicom_tool.sh <filename> <function>

# Function to dump the full DICOM file and dataset
dump_dicom() {
    echo "Dumping full DICOM file and dataset..."
    dcmdump "$1"
}

# Function to search for Pixel Data
search_pixel_data() {
    echo "Searching for Pixel Data..."
    dcmdump "$1" | grep -i "PixelData"
}

# Function to search for Transfer Syntax
search_transfer_syntax() {
    echo "Searching for Transfer Syntax..."
    dcmdump "$1" | grep -i "Transfer Syntax"
}

# Function to search for Transfer Syntax UID
search_transfer_syntax_uid() {
    echo "Searching for Transfer Syntax UID..."
    dcmdump "$1" | grep "Transfer Syntax UID"
    gdcmdump "$1" | grep "Transfer Syntax UID"
}

# Function to decode JPEG-compressed DICOM file
decode_jpeg_dicom() {
    echo "Decoding JPEG-compressed DICOM file..."
    dcmdjpeg "$1" decompressed.dcm
    echo "Decompressed file saved as decompressed.dcm"
}

# Main entry point
if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <filename> <function>"
    echo "Available functions:"
    echo "  dump            - Dump full DICOM file and dataset"
    echo "  pixeldata       - Search for Pixel Data"
    echo "  transfersyntax  - Search for Transfer Syntax"
    echo "  syntaxuid       - Search for Transfer Syntax UID"
    echo "  decodejpeg      - Decode JPEG-compressed DICOM file"
    exit 1
fi

# Map second argument to corresponding function
case $2 in
    dump)
        dump_dicom "$1"
        ;;
    pixeldata)
        search_pixel_data "$1"
        ;;
    transfersyntax)
        search_transfer_syntax "$1"
        ;;
    syntaxuid)
        search_transfer_syntax_uid "$1"
        ;;
    decodejpeg)
        decode_jpeg_dicom "$1"
        ;;
    *)
        echo "Invalid function: $2"
        echo "Available functions: dump, pixeldata, transfersyntax, syntaxuid, decodejpeg"
        exit 1
        ;;
esac
