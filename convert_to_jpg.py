import os

import numpy as np
import pydicom as dicom
from PIL import Image


def convert(filename):
    im = dicom.dcmread('./img/' + filename)
    im = im.pixel_array.astype(float)
    # Normalize the pixel values to the range [0, 1] and scale them to [0, 255]
    rescaled_image = (np.maximum(im, 0) / im.max()) * 255
    # Convert them to 8-bit integers
    final_image = np.uint8(rescaled_image)
    final_image = Image.fromarray(final_image)
    return final_image


path = "./img"
ct_images = os.listdir(path)
arr_filename = [x for x in ct_images if x.endswith(".dcm")]

for name in arr_filename:
    image = convert(name)
    image.save('./JPG_IMG/' + name + '.jpg')
