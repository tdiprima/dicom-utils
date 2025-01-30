#!/usr/bin/env bash
# DICOM viewer (see if file is readable): dcm2pnm, dcmj2pnm

# Check for differences in metadata between the working and non-working files
dcmdump file1.dcm > file1_metadata.txt
dcmdump file2.dcm > file2_metadata.txt
diff file1_metadata.txt file2_metadata.txt

# Re-encode the file using a tool like dcmodify to a simpler transfer syntax (e.g., uncompressed)
dcmconv --write-xfer-little input.dcm output.dcm
