"""
Removes or anonymizes all patient-identifiable information while maintaining the integrity of the image and metadata necessary for analysis

Author: tdiprima
Version: 1.0
License: MIT
"""

__author__ = 'tdiprima'
__version__ = '1.0'
__license__ = 'MIT'

import datetime

import pydicom
from pydicom.uid import generate_uid


def deidentify_dicom(input_file, output_file, shift_dates=True):
    """
    De-identifies a DICOM file by removing patient information, dates, times, private tags, and physician names.
    Optionally shifts all dates instead of removing them.

    Parameters:
        input_file (str): Path to the input DICOM file.
        output_file (str): Path to save the de-identified DICOM file.
        shift_dates (bool): If True, shifts dates instead of removing them.
    """
    dicom_data = pydicom.dcmread(input_file)

    # DICOM Tags
    tags_to_remove = ["PatientName", "PatientID", "PatientBirthDate", "PatientSex", "PatientAddress", "PatientAge",
                      "ReferringPhysicianName", "StudyDescription", "SeriesDescription", "AccessionNumber",
                      "OtherPatientIDs", "OtherPatientNames"]

    # Institution and Physician tags
    institution_tags = ["InstitutionName", "InstitutionAddress", "InstitutionalDepartmentName"]

    # TODO: Tried "PhysiciansReadingStudy", etc., but none of it worked.
    physician_tags = [
        "PerformingPhysicianName", "ReferringPhysicianName", "PhysiciansOfRecord",
        "OperatorsName", "RequestingPhysician",
        "NameOfPhysiciansReadingStudy", "ConsultingPhysicianName",
        "ResponsiblePerson", "RequestingService", "AdmittingDiagnosesDescription",
        "MedicalAlerts", "Allergies", "PatientInsurancePlanCodeSequence",
        "DerivationDescription", "PerformedProcedureStepDescription",
        "ScheduledPerformingPhysicianName", "ResponsibleOrganization"
    ]

    # Date & Time tags
    date_time_tags = ["StudyDate", "SeriesDate", "AcquisitionDate", "ContentDate", "PatientBirthDate", "StudyTime",
                      "SeriesTime", "AcquisitionTime", "ContentTime", "InstanceCreationDate", "InstanceCreationTime",
                      "PerformedProcedureStepStartDate", "PerformedProcedureStepStartTime"]

    # Remove sensitive fields safely
    for tag in tags_to_remove + institution_tags + physician_tags:
        if tag in dicom_data:
            dicom_data[tag].value = ''

    # Shift or remove date/time fields (if they exist)
    shift_days = 10000  # Shift by 10,000 days
    for tag in date_time_tags:
        if tag in dicom_data and dicom_data[tag].value:
            try:
                original_date = dicom_data[tag].value
                if original_date.isdigit() and len(original_date) == 8:  # YYYYMMDD format
                    new_date = (datetime.datetime.strptime(original_date, "%Y%m%d").date() + datetime.timedelta(
                        days=shift_days)).strftime("%Y%m%d")
                    dicom_data[tag].value = new_date
                else:
                    dicom_data[tag].value = ''  # If not a valid date, remove it
            except ValueError:
                dicom_data[tag].value = ''  # Remove invalid dates

    # Fix invalid time values (e.g., "10490922" is not valid)
    time_tags = ["StudyTime", "SeriesTime", "AcquisitionTime", "ContentTime"]
    for tag in time_tags:
        if tag in dicom_data and dicom_data[tag].value:
            time_value = dicom_data[tag].value
            if not (len(time_value) == 6 or len(time_value) == 4):  # Ensure HHMMSS or HHMM format
                dicom_data[tag].value = ''  # Remove invalid time

    # Generate new UIDs for anonymity
    dicom_data.StudyInstanceUID = generate_uid()
    dicom_data.SeriesInstanceUID = generate_uid()
    dicom_data.SOPInstanceUID = generate_uid()

    # Remove private tags
    dicom_data.remove_private_tags()

    # Save the de-identified DICOM file
    dicom_data.save_as(output_file)
    print(f"De-identified DICOM saved as: {output_file}")


# Example usage
input_dicom_file = "img/dicom1.dcm"
output_dicom_file = "deidentified/dicom1.dcm"
deidentify_dicom(input_dicom_file, output_dicom_file)
