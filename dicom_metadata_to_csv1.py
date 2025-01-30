# Reads a DICOM file, extracts its elements, and writes them into a CSV file along with their group, element, description, VR, and value.
import csv

import pydicom as dicom

ds = dicom.dcmread("./img/dicom_file.dcm")  # read one file

with open('file1.csv', 'w', newline='') as csvfile:
    # Create a CSV writer object
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow("Group Elem Description VR Value".split())

    # Iterate over each element in the DICOM file
    for elem in ds:
        # Format integer as zero-padded hexadecimal number
        writer.writerow(
            [f"{elem.tag.group:04x}", f"{elem.tag.element:04x}", elem.description(), elem.VR, str(elem.value)])
