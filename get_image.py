from PIL import Image
import numpy as np
import os

my_root_dir = '/home/lei/svm/BreaKHis_v1/histology_slides/breast' 
label_dict = {'benign': 1, 'malignant': 2}  

def get_fifth_dirname(dirpath):  
    # 初始化目录计数器和当前目录名  
    count = 0  
    current_dir = ''  
  
    # 使用 os.path.split() 迭代地分解路径  
    while True:  
        dirpath, dirname = os.path.split(dirpath)  
          
        # 递增计数器  
        count += 1  
          
        # 保存当前目录名  
        current_dir = dirname  
          
        # 如果到达根目录或已经找到第5个目录，则停止迭代  
        if not dirname or count == 5:  
            break  
      
    # 如果计数器未达到5，则返回None或抛出异常  
    if count < 5:  
        return None  # 或者可以抛出异常：raise ValueError("Path does not contain 7 directories")  
      
    # 返回第7个目录名  
    return current_dir  
  

def get_name_and_label(root_dir):
    # 遍历目录树  
     
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if not filenames:
            continue
            
        for filename in filenames:  
            
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  
                file_path = os.path.join(dirpath, filename)        
                dir_basename = get_fifth_dirname(dirpath)  
                  
                  
                if dir_basename in label_dict:
                    label = label_dict[dir_basename]
                    image_name.append(dir_basename)
                    image_paths.append(file_path)  
                    labels.append(label)

    return image_paths, labels, image_name

def get_images_from_paths(image_paths):  
    img_list = []  
    for file_path in image_paths:  
        if os.path.isfile(file_path) and file_path.lower().endswith('.png'):  
            with Image.open(file_path) as img:  
                img_list.append(img)  
    return img_list
    


