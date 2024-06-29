import SimpleITK as sitk
import os

image = sitk.ReadImage('/home/lei/SVM_ruxianai/test_one/mask/SOB_M_DC-14-2773-40-030.nrrd')

# 获取尺寸
image_size = image.GetSize()

# 获取维度
image_dimension = image.GetDimension()

print(image_size)
print(image_dimension)

