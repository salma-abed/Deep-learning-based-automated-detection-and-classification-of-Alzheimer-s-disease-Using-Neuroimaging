"""
* `SimpleITK` for managing `.nii` files.
* `numpy` for matrix operations. It is neccesary for `SimpleITK` to work.
* `pandas` for loading tables with basic information about the images, like their label.
* `matplotlib` for image visualization.
* `dltk.io.preprocessing` for some useful functions, like whitening.
* `skimage.filters`, to try some filters on the images.
* `os` for file interaction.
"""

import SimpleITK as sitk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from dltk.io import preprocessing
from skimage import filters
import os
"""

`SimpleITK` is supposed to be a great alternative for working with `.nii` images, which is the format provided by ADNI. Let's try it. Load the path and name of a random image.
"""

# path to .nii file
IMAGE = 'ADNI2.nii'

"""Try `SimpleITK`:"""

# load in sitk format
sitk_image = sitk.ReadImage("ADNI2.nii")
# transform into a numpy array
img = sitk.GetArrayFromImage(sitk_image)
# check the final shape 
imagge = img.shape

"""### Image Visualization

Now, let's try visualizing the images. Using `matplotlib.pyplot` is a very simple and perfectly valid option, but selecting a certain slice. There are three dimensions that can be used for slicing. In the following cell, slice 70 of the third dimension is shown.
"""

plt.imshow(img[:, :, 70], cmap='gray')
plt.show()

"""Let´s try appliying otsu´s thresholding, like in Ding et al. (2018). It should binarize the image. This tecnhique was not used in the final work, this was just a test."""

otsu = filters.threshold_otsu(img)
otsu_img = img > otsu
plt.imshow(otsu_img[:, :, 70], cmap='gray')
plt.show()

"""Now, a very important preprocessing step for the images will be space normalization. For that, the following `resample_img` method will be used. As mentioned in the complete paper, it is taken from a sample code at [this post](https://medium.com/tensorflow/an-introduction-to-biomedical-image-analysis-with-tensorflow-and-dltk-2c25304e7c13)."""

def resample_img(itk_image, out_spacing=[2.0, 2.0, 2.0]):
    ''' This function resamples images to 2-mm isotropic voxels.
    
        Parameters:
            itk_image -- Image in simpleitk format, not a numpy array
            out_spacing -- Space representation of each voxel
            
        Returns: 
            Resulting image in simpleitk format, not a numpy array
    '''
    
    # Resample images to 2mm spacing with SimpleITK
    original_spacing = itk_image.GetSpacing()
    original_size = itk_image.GetSize()

    out_size = [
        int(np.round(original_size[0] * (original_spacing[0] / out_spacing[0]))),
        int(np.round(original_size[1] * (original_spacing[1] / out_spacing[1]))),
        int(np.round(original_size[2] * (original_spacing[2] / out_spacing[2])))]

    resample = sitk.ResampleImageFilter()
    resample.SetOutputSpacing(out_spacing)
    resample.SetSize(out_size)
    resample.SetOutputDirection(itk_image.GetDirection())
    resample.SetOutputOrigin(itk_image.GetOrigin())
    resample.SetTransform(sitk.Transform())
    resample.SetDefaultPixelValue(itk_image.GetPixelIDValue())

    resample.SetInterpolator(sitk.sitkBSpline)

    return resample.Execute(itk_image)

"""In the following cell, the method is tried out with the previously loaded image. Also, tried cropping and whitening using `DLTK` methods. Finally, the result is printed, showing the 100th slice of the second axis."""

res = resample_img(sitk_image)
res_img = sitk.GetArrayFromImage(sitk_image)
res_img = preprocessing.resize_image_with_crop_or_pad(res_img, img_size=(128, 192, 192), mode='symmetric')
res_img = preprocessing.whitening(res_img)
plt.imshow(res_img[:, 100, :], cmap='gray')
plt.show()

# ## Skull stripping

# Section for skull stripping experimentation and execution. The FSL BET interface of `nipype` is used, so FSL BET must be installed in the local machine for this to work.
# """

from nipype.interfaces import fsl
import matplotlib.pyplot as plt

# def skull_strip_nii(original_img, destination_img, frac=0.3):
#     ''' Practice skull stripping on the given image, and save
#         the result to a new .nii image.
#         Uses FSL-BET 
#         (https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/BET/UserGuide#Main_bet2_options:)
        
#         Parameters:
#             original_img -- Original nii image
#             destination_img -- The new skull-stripped image
#             frac -- Fractional intensity threshold for BET
#     '''
    
btr = fsl.BET()
btr.inputs.in_file = IMAGE
btr.inputs.frac = 0.5
btr.inputs.out_file = 'ADNI2new2.nii'
btr.cmdline
res = btr.run()
    # return res

