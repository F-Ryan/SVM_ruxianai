import os
import SimpleITK as sitk


def get_using_image(source_path , output_path):
   
# 定义源文件夹和目标文件夹
    src_directory = source_path
    dst_directory = output_path

# 确保目标文件夹存在
    if not os.path.exists(dst_directory):
        os.makedirs(dst_directory)

# 遍历源文件夹及其所有子文件夹
    for dirpath, dirnames, filenames in os.walk(src_directory):
        for filename in filenames:
            # 检查文件扩展名是否为PNG
            if filename.lower().endswith('.png'):
                # 构建源文件和目标文件的完整路径
                src_file_path = os.path.join(dirpath, filename)
                # 从文件名中移除扩展名，并添加新的.nrrd扩展名
                dst_file_name = os.path.splitext(filename)[0] + '.nrrd'
                dst_file_path = os.path.join(dst_directory, dst_file_name)
                # 读取PNG图像并将其保存为NRRD格式
                itk_image = sitk.ReadImage(src_file_path)
                sitk.WriteImage(itk_image, dst_file_path)   

    return 0
                
source_image_path = '/home/lei/SVM_ruxianai/histology_slides/breast'    
output_image_path = '/home/lei/SVM_ruxianai/test_one/image'

get_using_image(image_path,output_image_path)


