import SimpleITK as sitk
from PIL import Image
import numpy as np
import os
from radiomics import featureextractor
import glob


def get_paths(root_dir):
    # 遍历目录树  
    image_paths = [] 

    for dirpath, dirnames, filenames in os.walk(root_dir):
        if not filenames:
            continue
            
        for filename in filenames:  
            
            if filename.lower().endswith( '.png'):  
                file_path = os.path.join(dirpath, filename)        
                image_paths.append(file_path)  
                    
    return image_paths

def convert_png_to_mask(png_path, threshold=128):
    # 使用PIL读取PNG图片
    img = Image.open(png_path)
    # 将图片转换为numpy数组
    img_np = np.array(img)
    
    # 根据需要将图像转换为二值图像，这里以阈值128为例
    #mask_np = (img_np > threshold).astype(np.uint8) * 255
    mask_np = (img_np > threshold).astype(np.uint8) * 1
    # 创建SimpleITK图像对象
    mask_sitk = sitk.GetImageFromArray(mask_np)
    
    return mask_sitk

def get_mask_paths(source_paths, output_path):
    # 检查输出文件夹是否存在，如果不存在则创建它
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 遍历源文件夹中的所有PNG文件
    for src_file_path in source_paths:
        if os.path.isfile(src_file_path) and src_file_path.lower().endswith('.png'):
            # 构建输出文件的名称和路径
            output_filename = os.path.splitext(os.path.basename(src_file_path))[0] + '_mask.nrrd'
            output_file_path = os.path.join(output_path, output_filename)
            
            # 转换PNG文件为SimpleITK格式的掩码图像并保存
            mask_image = convert_png_to_mask(src_file_path)
            sitk.WriteImage(mask_image, output_file_path)


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
                
#提取特征
def extract_glcm_features_from_folder(folder_path):
    # 初始化特征提取器
    extractor = featureextractor.RadiomicsFeatureExtractor()

    # 启用GLCM特征
    extractor.enableFeatureClassByName('glcm')

    # 使用glob模块找到所有.nrrd文件
    nrrd_files = glob.glob(folder_path + '/*.nrrd')

    # 存储所有文件的特征
    all_features = {}

    # 遍历所有文件
    for file_path in nrrd_files:
        # 读取图像和掩膜
        image = sitk.ReadImage(file_path)
        # 假设掩膜文件与图像文件同名，但后缀为_mask.nrrd
        mask_path = file_path.replace('.nrrd', '.nrrd')
        mask = sitk.ReadImage(mask_path)

        # 提取特征
        features = extractor.execute(image, mask)

        # 获取所有GLCM特征
        glcm_features = {k: v for k, v in features.items() if 'glcm' in k}

        # 将特征存储在字典中，使用文件名作为键
        file_name = file_path.split('/')[-1]
        all_features[file_name] = glcm_features

    return all_features








#得到mask的图片集
mask_dir = '/home/lei/SVM_ruxianai/histology_slides/breast/malignant'
mask_image_paths = get_paths(mask_dir)       
output_path = '/home/lei/SVM_ruxianai/test_one/image'
get_mask_paths(mask_image_paths,output_path)

#得到image的图片集
source_image_path = '/home/lei/SVM_ruxianai/histology_slides/breast/malignant'    
output_path = '/home/lei/SVM_ruxianai/test_one/image'
get_using_image(source_image_path,output_path)

#提取特征所用的文件夹
all_folder = output_path

# 提取所有特征
features = extract_glcm_features_from_folder(all_folder)
print(features)


