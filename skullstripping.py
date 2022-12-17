
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
 
