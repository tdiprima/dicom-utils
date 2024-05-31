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

# Sort the slices based on their ImagePositionPatient attribute to ensure correct order
try:
    slices = sorted(slices, key=lambda x: x.ImagePositionPatient[2])
except Exception as ex:
    print(ex)

# Extract pixel spacing and slice thickness from the first slice
pixel_spacing = slices[0].PixelSpacing
slices_thickess = slices[0].SliceThickness

# Calculate aspect ratios for different views
axial_aspect_ratio = pixel_spacing[1] / pixel_spacing[0]
sagital_aspect_ratio = pixel_spacing[1] / slices_thickess
coronal_aspect_ratio = slices_thickess / pixel_spacing[0]

# print("Pixel spacing:", pixel_spacing)
# print("Slices thickness:", slices_thickess)
# print("Axial a/r:", axial_aspect_ratio)
# print("Sagital a/r:", sagital_aspect_ratio)
# print("Coronal a/r:", coronal_aspect_ratio)

# Determine the shape of the 3D volume by taking the shape of one slice and adding the number of slices
img_shape = list(slices[0].pixel_array.shape)
img_shape.append(len(slices))

# Create an empty 3D array to hold the volume data
volume3d = np.zeros(img_shape)

try:
    # Fill the 3D array with pixel data from each slice
    for i, s in enumerate(slices):
        array2D = s.pixel_array
        volume3d[:, :, i] = array2D
except Exception as ex:
    print(ex)

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
