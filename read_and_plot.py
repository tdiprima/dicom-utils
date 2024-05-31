import matplotlib.pyplot as plt
from pydicom import dcmread

path = "./img/D0001.dcm"

x = dcmread(path)
# print(x)  # DICOM file structure
# print()
# print(dir(x))  # attributes
# print()
# print(x.PixelSpacing)

plt.imshow(x.pixel_array, cmap=plt.cm.gray)
plt.show()
