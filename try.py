import os

import matplotlib.pyplot as plt
import numpy as np
import pydicom as dicom

# Define the path to the directory containing the DICOM images
path = "./img"

# Get a list of all files in the directory
ct_images = os.listdir(path)

# Read each DICOM file and store it in a list
slices = [dicom.read_file(path + '/' + s, force=True) for s in ct_images]

# Check if the 'ImagePositionPatient' attribute exists in the slices
for i, slice in enumerate(slices):
    if not hasattr(slice, 'ImagePositionPatient'):
        print(f"Slice {i} does not have the 'ImagePositionPatient' attribute.")
    else:
        print(f"Slice {i} has the 'ImagePositionPatient' attribute.")

# If all slices have the attribute, sort the slices based on their ImagePositionPatient attribute
if all(hasattr(slice, 'ImagePositionPatient') for slice in slices):
    slices = sorted(slices, key=lambda x: x.ImagePositionPatient[2])
else:
    print(
        "Not all slices have the 'ImagePositionPatient' attribute. Sorting cannot be performed.")  # Handle this case as needed, such as skipping sorting or using another method

# Proceed if sorting is possible
if all(hasattr(slice, 'ImagePositionPatient') for slice in slices):
    # Extract pixel spacing and slice thickness from the first slice
    pixel_spacing = slices[0].PixelSpacing
    slices_thickess = slices[0].SliceThickness

    # Calculate aspect ratios for different views
    axial_aspect_ratio = pixel_spacing[1] / pixel_spacing[0]
    sagital_aspect_ratio = pixel_spacing[1] / slices_thickess
    coronal_aspect_ratio = slices_thickess / pixel_spacing[0]

    # Determine the shape of the 3D volume by taking the shape of one slice and adding the number of slices
    img_shape = list(slices[0].pixel_array.shape)
    img_shape.append(len(slices))

    # Create an empty 3D array to hold the volume data
    volume3d = np.zeros(img_shape)

    # Fill the 3D array with pixel data from each slice
    for i, s in enumerate(slices):
        array2D = s.pixel_array
        volume3d[:, :, i] = array2D

    # Plot the axial view (view from top to bottom)
    axial = plt.subplot(2, 2, 1)
    plt.title("Axial")
    plt.imshow(volume3d[:, :, img_shape[2] // 2])
    axial.set_aspect(axial_aspect_ratio)

    # Plot the sagittal view (view from side to side)
    sagital = plt.subplot(2, 2, 2)
    plt.title("Sagittal")
    plt.imshow(volume3d[:, img_shape[1] // 2, :])
    sagital.set_aspect(sagital_aspect_ratio)

    # Plot the coronal view (view from front to back)
    coronal = plt.subplot(2, 2, 3)
    plt.title("Coronal")
    plt.imshow(volume3d[img_shape[0] // 2, :, :].T)
    coronal.set_aspect(coronal_aspect_ratio)

    # Display the plots
    plt.show()

    # Print the shape of a 2D slice and the 3D volume for reference
    print(array2D.shape)
    print(volume3d.shape)
else:
    print("Cannot proceed with plotting due to missing 'ImagePositionPatient' attribute in some slices.")
