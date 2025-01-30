import os
import numpy as np
import pydicom
import matplotlib.pyplot as plt

def load_dicom_images(directory):
    """Load DICOM images from the directory, check for ImagePositionPatient, and sort them."""
    dicom_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".dcm")]

    slices = []
    for file in dicom_files:
        ds = pydicom.dcmread(file)
        if hasattr(ds, "ImagePositionPatient"):
            slices.append(ds)

    if not slices:
        raise ValueError("No valid DICOM slices found with 'ImagePositionPatient'.")

    # Sort slices based on ImagePositionPatient (z-coordinate)
    slices.sort(key=lambda s: s.ImagePositionPatient[2])
    
    return slices

def construct_3d_volume(slices):
    """Convert DICOM slices into a 3D numpy array."""
    pixel_spacing = slices[0].PixelSpacing  # (row_spacing, col_spacing)
    slice_thickness = slices[0].SliceThickness

    volume_shape = (len(slices), slices[0].pixel_array.shape[0], slices[0].pixel_array.shape[1])
    volume = np.zeros(volume_shape, dtype=np.int16)

    for i, s in enumerate(slices):
        volume[i, :, :] = s.pixel_array

    return volume, pixel_spacing, slice_thickness

def plot_views(volume, pixel_spacing, slice_thickness):
    """Plot axial, sagittal, and coronal views of the DICOM 3D volume."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Axial View (Top-down)
    axial_slice = volume[volume.shape[0] // 2, :, :]
    axes[0].imshow(axial_slice, cmap="gray", aspect=pixel_spacing[1] / pixel_spacing[0])
    axes[0].set_title("Axial View")

    # Sagittal View (Side)
    sagittal_slice = volume[:, :, volume.shape[2] // 2]
    axes[1].imshow(sagittal_slice, cmap="gray", aspect=slice_thickness / pixel_spacing[0])
    axes[1].set_title("Sagittal View")

    # Coronal View (Front)
    coronal_slice = volume[:, volume.shape[1] // 2, :]
    axes[2].imshow(coronal_slice, cmap="gray", aspect=slice_thickness / pixel_spacing[1])
    axes[2].set_title("Coronal View")

    plt.tight_layout()
    plt.show()

# Main Execution
if __name__ == "__main__":
    dicom_directory = "./img"  # Change this to your DICOM folder path

    # Load, process, and visualize
    slices = load_dicom_images(dicom_directory)
    volume, pixel_spacing, slice_thickness = construct_3d_volume(slices)
    plot_views(volume, pixel_spacing, slice_thickness)

