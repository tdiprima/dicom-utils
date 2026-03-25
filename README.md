# dicom-utils

A Python toolkit for decompressing, de-identifying, inspecting, and converting DICOM medical imaging files.

## The Medical Imaging Data Challenge

DICOM files are the standard format for medical imaging — CT scans, MRIs, X-rays — but working with them in research or development pipelines is rarely straightforward. Files arrive compressed in formats that standard libraries can't read, packed with patient identifiers that can't leave clinical systems, and structured in ways that resist simple metadata inspection. Getting raw, usable, de-identified imaging data out of a DICOM archive typically requires stitching together multiple fragmented tools.

## What This Toolkit Does

`dicom-utils` provides a focused set of Python modules and shell scripts that cover the full preparation pipeline: decompress DICOM files (individually or in bulk), strip all patient-identifiable information while preserving imaging fidelity, extract metadata to CSV, convert images to JPEG, and verify that redaction was done correctly. Batch jobs use multiprocessing to saturate available CPU cores. Every step produces an audit trail via structured logging.

## Example: De-identify a DICOM File

```python
from src.deidentify import deidentify_dicom

deidentify_dicom(
    input_file="scan.dcm",
    output_file="deidentified/scan.dcm",
    shift_dates=True   # offsets dates by 10,000 days instead of removing them
)
```

Then verify the output is clean:

```python
from src.redaction_checker import check_redacted_dicom

check_redacted_dicom("deidentified/scan.dcm")
# ✅ All sensitive fields are blank or set to REMOVED
```

## Usage

### Requirements

```
pip install -r requirements.txt
```

Requires Python 3 and `pydicom`, `numpy`, `pillow`. Shell scripts additionally require [DCMTK](https://dicom.offis.de/dcmtk.php.en) and [GDCM](https://gdcm.sourceforge.net/).

### Decompress a directory of DICOM files

```python
from src.batch_decompress_dicom import process_dicom_directory

process_dicom_directory(input_dir="./img", output_dir="./decompressed")
```

### Extract metadata to CSV

```python
from src.dicom_to_csv_extractor import extract_dicom_metadata

extract_dicom_metadata("scan.dcm", output_csv="metadata.csv")
# Columns: Group, Elem, Description, VR, Value
```

### Extract accession numbers (parallel)

```python
from src.extract_dicom_accessions_multiproc import extract_accession_numbers_parallel

extract_accession_numbers_parallel(
    dicom_dir="./img",
    output_file="accessions.txt",
    affix=".dcm"
)
```

### Convert DICOM images to JPEG

```python
from src.image_converter import convert_image_to_jpg

convert_image_to_jpg("scan.dcm")
# Output written to ./processed_images/
```

### Shell utilities

```bash
# Inspect a DICOM file
./scripts/dicom_tool.sh scan.dcm dump

# Check if a file uses JPEG compression
./scripts/check_jpeg_dicom.sh scan.dcm
```

## Module Reference

| Module | Purpose |
|---|---|
| `batch_decompress_dicom.py` | Recursively decompress a directory of DICOM files |
| `deidentify.py` | Remove or shift 45+ patient-identifiable tags |
| `redaction_checker.py` | Validate that sensitive fields were properly cleared |
| `dicom_to_csv_extractor.py` | Export all DICOM metadata to CSV |
| `image_converter.py` | Convert DICOM pixel data to JPEG |
| `extract_dicom_accessions.py` | Extract unique accession numbers to a text file |
| `extract_dicom_accessions_multiproc.py` | Same, parallelized across all CPU cores |
| `dicom_reader.py` | Robust DICOM file reader with error handling |

## License

[MIT](LICENSE)
