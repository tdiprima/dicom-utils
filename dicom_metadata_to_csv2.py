import csv
import os

import pydicom as dicom

data_dir = "./img"  # Directory containing the DICOM files
patients = os.listdir(data_dir)  # List all files in the data directory

with open('file2.csv', 'w') as myfile:  # Open a new CSV file to write data
    writer = csv.writer(myfile)  # Create a CSV writer object
    # Write the header row to the CSV file
    writer.writerow("Group Elem Description VR Value".split())

    for patient in patients:  # Iterate over each file in the directory
        if patient.lower().endswith('.dcm'):  # Check if the file is a DICOM file
            dm = dicom.dcmread(os.path.join(data_dir, patient))  # Read the DICOM file
            for elem in dm:  # Iterate over each element in the DICOM file
                # Write the DICOM element's group, element, description, Value Representation, and value to the CSV file
                writer.writerow(
                    [f"{elem.tag.group:04x}", f"{elem.tag.element:04x}", elem.description(), elem.VR, str(elem.value)])
