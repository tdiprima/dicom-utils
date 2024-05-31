import csv

import pydicom as dicom

ds = dicom.dcmread("./img/D0001.dcm")  # read one file

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
