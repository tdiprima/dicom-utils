"""
Read a directory of DICOM files, extract the "Accession Number" (tag "0008,0050"),
and write it to a text file called accession_list.txt, ensuring each accession number is unique.
"""
__author__ = 'tdiprima'

import os
import pydicom


def extract_accession_numbers(dicom_dir, output_file, affix):
    """
    Extracts accession numbers from DICOM files and writes them directly to the output file.
        Parameters:
        dicom_dir (str): Path to the directory containing DICOM files.
        output_file (str): Path to the output text file.
        affix (str): ".dcm", ".dat"...
    """
    unique_accession_numbers = set()  # Set to track unique accession numbers

    with open(output_file, 'w') as f:
        for root, _, files in os.walk(dicom_dir):
            for file in files:
                if file.endswith(affix):
                    file_path = os.path.join(root, file)
                    try:
                        ds = pydicom.dcmread(file_path)
                        if "AccessionNumber" in ds:
                            accession_number = ds.AccessionNumber
                            # Check if it is already in the set
                            if accession_number not in unique_accession_numbers:
                                unique_accession_numbers.add(accession_number)
                                # Only unique accession numbers are written to the file.
                                f.write(f"{accession_number}\n")
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")


# Specify the directory containing DICOM files and the output file name
home_directory = os.path.expanduser("~")
full_path = os.path.join(home_directory, "trabajo", "obscura", "input")
output_file_name = "accession_list.txt"
suffix = ".dcm"

extract_accession_numbers(full_path, output_file_name, suffix)
