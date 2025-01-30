## See: `scripts/debug.sh`

If the program runs fine for one DICOM file but fails with the `UnsatisfiedLinkError` for another, the issue is likely related to how the problematic DICOM file is formatted or processed by the OpenCV native library.

### Possible Causes:
1. **File Format or Metadata Difference**:
   - The problematic DICOM file might use an encoding or structure that the OpenCV `Imgcodecs.dicomJpgFileRead` function cannot handle.
   - OpenCV might not support certain DICOM compression types (e.g., JPEG2000, RLE, etc.).

2. **Unsupported Features**:
   - The file might have optional or proprietary DICOM tags/features that your OpenCV build doesn't handle.

3. **Data Corruption**:
   - The problematic DICOM file could be malformed or partially corrupted, causing the library to crash when it tries to process the file.

---

The **"good" DICOM file** uses Little Endian Explicit transfer syntax. Specifically:

1. The file meta-information header uses Little Endian Explicit transfer syntax
2. The main DICOM dataset also uses Little Endian Explicit transfer syntax
3. This is confirmed by the TransferSyntaxUID (0002,0010) with value "LittleEndianExplicit"

The file appears to be a valid DICOM file with a proper meta-information header and data set structure. It's a Secondary Capture Image with 512x512 dimensions and 8-bit monochrome pixels.

The **"bad" DICOM file** uses JPEG Lossless compression with the following transfer syntax details:

1. The file meta-information header uses Little Endian Explicit transfer syntax
2. The main DICOM dataset uses "JPEG Lossless, Non-hierarchical, 1st Order Prediction" transfer syntax
3. This is confirmed by the TransferSyntaxUID (0002,0010) with value "JPEGLossless:Non-hierarchical-1stOrderPrediction"

The file is a valid DICOM CT Image from a GE LightSpeed VCT scanner. It's a scout/localizer image with dimensions 1149x888 pixels and 16-bit depth. The image data is stored using JPEG lossless compression to maintain full diagnostic quality while reducing file size.

---

The key difference lies in the **transfer syntax** and **compression**:

1. **Good DICOM File**:
   - Uses **Little Endian Explicit transfer syntax**.
   - No compression; straightforward for OpenCV to process.
   - Secondary Capture Image: 512x512, 8-bit monochrome.

2. **Bad DICOM File**:
   - Uses **JPEG Lossless compression** with **1st Order Prediction**.
   - Requires specific handling or decompression that OpenCV may not support.
   - CT Image: 1149x888, 16-bit depth.

### Likely Cause of the Issue:
The **JPEG Lossless compression** in the bad DICOM file is not natively supported by OpenCV's `Imgcodecs.dicomJpgFileRead` function. OpenCV struggles to decode or interpret this format, leading to the crash.

### Potential Fixes:
- **Decompress the File**: Use a tool like `dcmdjpeg` (from DCMTK) to decompress the DICOM file into an uncompressed format:

  ```bash
  dcmdjpeg bad.dcm decompressed.dcm
  ```

  This will convert the JPEG Lossless data into raw pixel data that OpenCV can handle.

- **Switch to a DICOM-Specific Library**: Use a library like `dcm4che` or `pydicom` for reading JPEG Lossless compressed DICOM files. They provide robust support for different transfer syntaxes.

- **Rebuild OpenCV with JPEG Support**: Ensure your OpenCV build includes the necessary codecs for handling JPEG Lossless (though this may require custom compilation and dependencies).

By decompressing the problematic files or using a more specialized library, you should be able to handle them effectively.

<br>
