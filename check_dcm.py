import pydicom
from pydicom.errors import InvalidDicomError

def get_dcm_image_size(dcm_file_path):
    try:
        # 读取DICOM文件
        ds = pydicom.dcmread(dcm_file_path)
        
        # 提取图像尺寸信息
        rows = ds.Rows
        cols = ds.Columns
        
        return rows, cols
    except InvalidDicomError:
        print(f"Error: The file {dcm_file_path} is not a valid DICOM file.")
    except Exception as e:
        print(f"Error: {e}")


# 获取并打印DICOM图像的尺寸
rows1, cols1 = get_dcm_image_size('/home/lei/SVM/train/Calc-Training_P_00005_RIGHT_CC/08-07-2016-DDSM-23157/1.000000-full mammogram images-38548/1-1.dcm')
rows2, cols2 = get_dcm_image_size('/home/lei/SVM/train/Calc-Training_P_00005_RIGHT_CC_1/08-30-2017-DDSM-09081/1.000000-cropped images-94682/1-2.dcm')
rows3, cols3 = get_dcm_image_size('/home/lei/SVM/train/Calc-Training_P_00005_RIGHT_CC_1/08-30-2017-DDSM-09081/1.000000-cropped images-94682/1-1.dcm')

print(f"Image size-原始: {rows1} x {cols1}")
print(f"Image size-掩模: {rows2} x {cols2}")
print(f"Image size-裁剪: {rows3} x {cols3}")
