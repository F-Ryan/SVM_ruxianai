import SimpleITK as sitk
from PIL import Image
import numpy as np
import os
import radiomics
from radiomics import featureextractor
import sys
import time
import pandas as pd
from collections import OrderedDict
import re
import csv


def get_second_dirname(dirpath):
    # 初始化目录计数器和当前目录名列表
    count = 0
    dirs = []
    
    # 使用 os.path.split() 迭代地分解路径
    while True:
        dirpath, dirname = os.path.split(dirpath)
        # 如果到达根目录，则停止迭代
        if not dirname:
            break
        # 将当前目录名添加到列表
        dirs.append(dirname)
        # 递增计数器
        count += 1

    # 如果目录数量少于1个，则返回 None
    if count < 1:
        return None
    # 返回第一个目录名
    return dirs[-1]

def get_last_two_dirs(dirpath):
    # 使用 os.path.split() 迭代地分解路径
    dirs = []
    while dirpath:
        dirpath, dirname = os.path.split(dirpath)
        if dirname:
            dirs.append(dirname)
    # 返回最后两个目录名
    return '/'.join(dirs[-2:])

def find_matching_image(mask_path, all_folder):
    # 使用正则表达式从蒙版路径中提取信息
    mask_filename = os.path.basename(mask_path)
    mask_dirname = os.path.dirname(mask_path)
    image_dirname = re.sub(r'_\d$', '', mask_dirname)  # 移除文件夹名称中的数字后缀
    image_filename = mask_filename.replace('-2.dcm', '-1.dcm')
    
    # 构建图像的预期路径
    image_path = os.path.join(image_dirname, image_filename)
    
    # 检查图像文件是否存在
    if os.path.exists(image_path):
        return image_path
    else:
        return None

def resize_dicom_image(dicom_path, target_size):
    # 读取 DICOM 图像
    image = sitk.ReadImage(dicom_path)
    size = image.GetSize()
    # 创建一个转换器，用于调整图像大小
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(image)  # 设置参考图像，确保缩放后的图像与原图像对齐
    resampler.SetInterpolator(sitk.sitkLinear)  # 设置插值器
    if size == target_size:
        return image
    
    resampler.SetSize(target_size)

    # 应用变换并返回调整大小的图像
    resized_image = resampler.Execute(image)
    
    # 返回调整大小的 DICOM 图像
    return resized_image


    
def extract_features(all_folder, output_file):
    # 检查图像和蒙版文件夹是否存在
    if not os.path.isdir(all_folder):
        print(f'Image folder "{all_folder}" does not exist.')
        return

    # 检查输出文件是否可以创建或写入
    if os.path.exists(output_file) and not os.access(output_file, os.W_OK):
        print(f'Output file "{output_file}" is not writable.')
        return
    if not os.path.exists(output_file):
        try:
            with open(output_file, 'w') as f:
                pass  # 创建文件
        except IOError as e:
            print(f'Unable to create or write to output file "{output_file}": {e}')
            return


     # 提取器设置
    params = '/home/lei/SVM/test_one/params_glcm.yaml'
    extractor = featureextractor.RadiomicsFeatureExtractor(params)
    features_df = pd.DataFrame()
    
    for root, dirs, files in os.walk(all_folder):
        for file in files:
            if file.lower().endswith('-2.dcm'):  # 检查文件名是否以"-1.dcm"结尾
                mask_file_path = os.path.join(root, file)  # 构建蒙版文件的完整路径
                # 构建相对于根目录的相对路径，并去掉末尾的文件名
                relative_dir_path = os.path.relpath(root, all_folder)
                #print(f'relative_dir_path: {relative_dir_path}')
                # 替换文件夹名称中的"_1"或"_2"等后缀
                #relative_dir_path_replaced = re.sub(r'_[1-5]$', '', relative_dir_path)
                second_name = get_second_dirname(relative_dir_path)
                second_name = re.sub(r'_[1-5]$', '', second_name)
                
                
                mask_file = find_matching_image(mask_file_path, all_folder)
                    
                #print(f"Mask: {mask_file}")

                #print(f'specific_part: {specific_part}')
                replace_path = os.path.join(all_folder, second_name)
                for root, dirs, files in os.walk(replace_path):
                    for file in files:
                        if file.lower().endswith('-1.dcm'): 
                            image_file = os.path.join(root,file)
                print(f"\nImage:{image_file}\nMask: {mask_file}")
                try:
                    # 读取图像和蒙版
                    target_size = (2761, 5056, 1)
                    image = resize_dicom_image(image_file,target_size)
                    mask = resize_dicom_image(mask_file,target_size)
                    mask = sitk.BinaryThreshold(mask, 128, 65535)

                    # 提取特征
                    features = extractor.execute(image, mask)
                    print(f'\nfeatures:{features}\n')
                    # 将特征转换为列表
                    feature_list = [features[feature_name] for feature_name in features]
                    
                    # 将特征列表添加到DataFrame中
                    features_df = features_df.append([feature_list], ignore_index=True)
                    
                except Exception as e:
                    print(f'Error processing {file}: {e}')
                    
                features_df.to_csv(output_file, index=False, header=False, mode='a')


def redirect_stdout_to_file(file_path):
    # 打开指定的文件
    with open(file_path, 'w') as f:
        # 保存原来的标准输出
        original_stdout = sys.stdout
        try:
            # 重定向标准输出到文件
            sys.stdout = f
            # 这里执行您的代码，其输出将被重定向到文件
            print("这是一条重定向到文件的输出。")
        finally:
            # 恢复标准输出到原来的值
            sys.stdout = original_stdout

# 调用函数并指定文件路径
redirect_stdout_to_file('/home/lei/SVM/test_one/stdout.txt')


start_time = time.time()

#提取器设置
#params = '/home/lei/SVM/test_one/params_glcm.yaml'
#extractor = featureextractor.RadiomicsFeatureExtractor(params)

#image an mask
all_path = '/home/lei/SVM/train'


# 提取所有特征
features_folder = '/home/lei/SVM/test_one/out_features.csv'
extract_features(all_path, features_folder)

end_time = time.time()  
elapsed_time = end_time - start_time

hours = int(elapsed_time // 3600)
minutes = int((elapsed_time % 3600) // 60)
seconds = elapsed_time % 60

print(f"程序运行了 {hours} 小时 {minutes} 分钟 {seconds} 秒")

