"""
Loads a DICOM file, checks all sensitive fields, and prints any field that was NOT properly redacted.

Author: tdiprima
Version: 1.0
License: MIT
"""

__author__ = "tdiprima"
__version__ = "1.0"
__license__ = "MIT"

import pydicom


def check_redacted_dicom(dicom_file):
    """
    Checks if a DICOM file contains any fields that should be redacted but still have values.
    Prints any non-redacted field names along with their values.

    Parameters:
        dicom_file (str): Path to the DICOM file.
    """
    dicom_data = pydicom.dcmread(dicom_file)

    # List of sensitive fields that should be redacted
    sensitive_tags = [
        "PatientName",
        "PatientID",
        "PatientBirthDate",
        "PatientSex",
        "PatientAddress",
        "ReferringPhysicianName",
        "StudyDescription",
        "SeriesDescription",
        "AccessionNumber",
        "OtherPatientIDs",
        "OtherPatientNames",
        "InstitutionName",
        "InstitutionAddress",
        "InstitutionalDepartmentName",
        "PerformingPhysicianName",
        "ReferringPhysicianName",
        "PhysiciansOfRecord",
        "OperatorsName",
        "RequestingPhysician",
        "NameOfPhysiciansReadingStudy",
        "ConsultingPhysicianName",
        "ResponsiblePerson",
        "RequestingService",
        "AdmittingDiagnosesDescription",
        "MedicalAlerts",
        "Allergies",
        "PatientInsurancePlanCodeSequence",
        "DerivationDescription",
        "PerformedProcedureStepDescription",
        "ScheduledPerformingPhysicianName",
        "ResponsibleOrganization",
        "StudyDate",
        "SeriesDate",
        "AcquisitionDate",
        "ContentDate",
        "StudyTime",
        "SeriesTime",
        "AcquisitionTime",
        "ContentTime",
    ]

    print("\n🔍 **Checking for unredacted DICOM fields...**\n")

    unredacted_fields = []
    for tag in sensitive_tags:
        if tag in dicom_data:
            value = str(
                dicom_data[tag].value
            ).strip()  # Convert value to string and remove extra spaces
            if (
                value and value != "REMOVED"
            ):  # Check if the value is not blank and not "REMOVED"
                unredacted_fields.append((tag, value))

    # Print results
    if unredacted_fields:
        print("🚨 WARNING: Some fields are NOT redacted! 🚨\n")
        for tag, value in unredacted_fields:
            print(f"⚠️  {tag}: {value}")
    else:
        print("✅ All sensitive fields are properly redacted!")


# Example usage
dicom_file = "deidentified/dicom1.dcm"
check_redacted_dicom(dicom_file)
