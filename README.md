# 基于SVM的乳腺癌图像识别
DDSM数据集里的图片集 只放了一部分
完整下载链接 http://www.inf.ufpr.br/vri/databases/BreaKHis_v1.tar.gz

一、
my_root_dir = ''  可以改为类似 my_root_dir = 'G:\\SVM\\new\\histology_slides\\breast' 
用 test_svm.py跑
代码很简单，正在改进

二、
新传了extract_glcm_features.py，使用了 影像组学 - pyradiomics库，所以需要将原来的png图像转化为nrrd格式，同时设置一个掩模mask。
extract_glcm_features.py提取了GLCM的24个特征。
