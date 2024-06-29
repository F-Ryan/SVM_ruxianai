import SimpleITK as sitk

# 读取 DICOM 文件
dicom_image = sitk.ReadImage('/home/lei/SVM/train/Calc-Training_P_00271_LEFT_MLO/08-07-2016-DDSM-52887/1.000000-full mammogram images-48159/1-1.dcm')

# 获取图像大小
size = dicom_image.GetSize()

# 打印图像大小
print(f'stick: {size}\n')
