import SimpleITK as sitk
from PIL import Image
import numpy as np
import os

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

def convert_png_to_mask(image_path, threshold=128):
    # 使用PIL读取PNG图片
    img = Image.open(image_path)
    # 将图片转换为numpy数组
    img_np = np.array(img)
    
    # 根据需要将图像转换为二值图像，这里以阈值128为例
    mask_np = (img_np > threshold).astype(np.uint8) * 255
    
    # 创建SimpleITK图像对象
    mask_sitk = sitk.GetImageFromArray(mask_np)
    
    return mask_sitk



def get_mask_paths(source_path,output_path):
# 检查文件夹是否存在，如果不存在则创建它
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

# 遍历路径列表，将每个PNG图片转换为SimpleITK格式的掩码图像
    mask_images = []
    for path in image_paths:
        mask_image = convert_png_to_mask(path)
        mask_images.append(mask_image)

# 保存SimpleITK掩码图像到指定文件夹，例如.nii
    for i, mask_img in enumerate(mask_images):
        output_path = os.path.join(output_folder, f'mask_{i}.nrrd')
        sitk.WriteImage(mask_img, output_path)



mask_dir = '/home/lei/SVM_ruxianai/histology_slides/breast/malignant'
mask_image_paths = get_paths(mask_dir)       
output_mask_path = '/home/lei/SVM_ruxianai/test_one/masks'
get_mask_paths(mask_image_paths,output_mask_path)

