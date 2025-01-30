# Reads and displays a DICOM image file using matplotlib and pydicom.
import matplotlib.pyplot as plt
from pydicom import dcmread

path = "./img/dicom_file.dcm"

x = dcmread(path)
# print(x)  # DICOM file structure
# print()
# print(dir(x))  # attributes
# print()
# print(x.PixelSpacing)

plt.imshow(x.pixel_array, cmap=plt.cm.gray)
plt.show()
import matplotlib.pyplot as plt
from pydicom import dcmread

path = "./img/dicom_file.dcm"

x = dcmread(path)
# print(x)  # DICOM file structure
# print()
# print(dir(x))  # attributes
# print()
# print(x.PixelSpacing)

plt.imshow(x.pixel_array, cmap=plt.cm.gray)
plt.show()
