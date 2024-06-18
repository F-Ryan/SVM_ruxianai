from PIL import Image
import cv2
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, classification_report

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
      
    # 返回第5个目录名  
    return current_dir  
  
# 遍历目录树
def get_name_and_label(root_dir):
      
    image_paths = [] 
    labels = [] 
    image_name = [] 
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
    
#预处理
def preprocess_image(image_path):
    # 读取图像
    img = cv2.imread(image_path)
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 归一化
    normalized_img = cv2.normalize(gray, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    # 调整大小（根据需要选择适当的大小）
    resized_img = cv2.resize(normalized_img, (760, 400))
    return resized_img

# 特征提取函数
def local_binary_pattern(image, P=8, R=1):
    # 检查图像是否已经是灰度图像
    if len(image.shape) == 2 or image.shape[2] == 1:
        # 如果是灰度图像，直接使用
        gray = image
    else:
        # 如果不是灰度图像，转换为灰度图像
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    

    # 计算LBP特征
    lbp = np.zeros_like(gray)
    for y in range(R, gray.shape[0] - R):
        for x in range(R, gray.shape[1] - R):
            # 中心像素值
            center = gray[y, x]
            binary_code = 0
            for i in range(P):
                # 计算邻域像素的坐标
                tx = x + R * np.cos(2 * np.pi * i / P)
                ty = y - R * np.sin(2 * np.pi * i / P)
                
                # 确保索引在图像范围内
                tx = max(0, min(gray.shape[1] - 1, tx))
                ty = max(0, min(gray.shape[0] - 1, ty))
                
                # 双线性插值
                ty0, ty1 = int(ty), min(gray.shape[0] - 1, int(ty) + 1)
                tx0, tx1 = int(tx), min(gray.shape[1] - 1, int(tx) + 1)
                value = (1 - (tx - tx0)) * (1 - (ty - ty0)) * gray[ty0, tx0] + \
                        (1 - (tx - tx0)) * (ty - ty0) * gray[ty1, tx0] + \
                        (tx - tx0) * (1 - (ty - ty0)) * gray[ty0, tx1] + \
                        (tx - tx0) * (ty - ty0) * gray[ty1, tx1]
                
                # 比较 center 像素值和邻域像素值
                if value >= center:
                    binary_code |= 1 << (P - 1 - i)
            lbp[y, x] = binary_code
    return lbp


def extract_features(images, P=8, R=1):
    features = []
    for img in images:
        lbp = local_binary_pattern(img, P, R)
        # 将LBP图像转换为特征向量
        feature = np.histogram(lbp, bins=np.arange(0, 2**P + 1), range=(0, 2**P))[0]
        features.append(feature)
    return np.array(features)


# SVM分类函数
def train_svm(X_train, y_train, X_test, y_test):
    # 创建SVM分类器
    svm = SVC(kernel='linear', C=1.0, random_state=42)
    # 训练模型
    svm.fit(X_train, y_train)
    # 预测测试集
    y_pred = svm.predict(X_test)
    # 计算准确率
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)
    print("Classification Report:\n", classification_report(y_test, y_pred))
    return svm

# 获取图像路径、标签和名称
image_paths = []
labels = []
image_names = []

image_paths, labels, image_names = get_name_and_label(my_root_dir)

# 图像预处理
processed_images = [preprocess_image(path) for path in image_paths]

# 特征提取
features = extract_features(processed_images)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# 训练SVM模型并进行分类
svm_model = train_svm(X_train, y_train, X_test, y_test)

