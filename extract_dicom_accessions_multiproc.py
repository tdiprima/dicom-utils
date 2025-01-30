"""
Read a directory of DICOM files, extract the "Accession Number" (tag "0008,0050"),
and write it to a text file called accession_list.txt, ensuring each accession number is unique.
Uses multiprocessing to utilize all available CPU cores.
"""
__author__ = 'tdiprima'

import os
import pydicom
from multiprocessing import Pool, cpu_count, Manager


def process_dicom_file(args):
    """
    Process a single DICOM file to extract the Accession Number.
    Parameters:
        args (tuple): Contains the file path and a shared set of unique accession numbers.
    Returns:
        str: The unique accession number if found, otherwise None.
    """
    file_path, affix = args
    try:
        if file_path.endswith(affix):
            ds = pydicom.dcmread(file_path)
            if "AccessionNumber" in ds:
                return ds.AccessionNumber
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None


def extract_accession_numbers_parallel(dicom_dir, output_file, affix):
    """
    Extracts unique accession numbers from DICOM files using multiprocessing and writes them to a text file.
    Parameters:
        dicom_dir (str): Path to the directory containing DICOM files.
        output_file (str): Path to the output text file.
        affix (str): File suffix to filter files (e.g., ".dcm", ".dat").
    """
    # Get a list of all files in the directory recursively
    file_paths = []
    for root, _, files in os.walk(dicom_dir):
        for file in files:
            file_paths.append(os.path.join(root, file))

    # Use multiprocessing Pool to process files in parallel
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(process_dicom_file, [(file_path, affix) for file_path in file_paths])

    # Filter out None values and keep only unique accession numbers
    unique_accession_numbers = set(filter(None, results))

    # Write unique accession numbers to the output file
    with open(output_file, 'w') as f:
        for accession_number in unique_accession_numbers:
            f.write(f"{accession_number}\n")

    print(f"Unique accession numbers saved to {output_file}")


# Specify the directory containing DICOM files and the output file name
home_directory = os.path.expanduser("~")
full_path = os.path.join(home_directory, "github", "input")
output_file_name = "accession_list.txt"
suffix = ".dat"

extract_accession_numbers_parallel(full_path, output_file_name, suffix)
