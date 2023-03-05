import os
import random
from shutil import copy2
from PIL import ImageEnhance
import cv2
import numpy as np
import torch
from PIL.Image import Image
from torchvision.datasets import ImageFolder
from sklearn.model_selection import train_test_split


class preprocess:
    '''
    读取源数据文件夹，生成划分好的文件夹，分为trian、val、test三个文件夹进行
    :param src_data_folder: 源文件夹
    :param target_data_folder: 目标文件夹
    :param train_scale: 训练集比例
    :param val_scale: 验证集比例
    :param test_scale: 测试集比例
    :return:
    '''

    def __init__(self, operator, data_path, *args):
        if operator == "split":
            self.splitDataByRate(data_path, args[0])
        elif operator == "splitCsvData":
            self.splitCsvData(data_path, args[0], args[1])  # data,label,test_size 把data改为data_path
        elif operator == "crop":
            self.imageCrop(data_path, args[0])
        elif operator == "enlargeImage":
            self.enlargeImage(data_path, args[0], args[1])
        elif operator == "shrinkImage":
            self.shrinkImage(data_path, args[0], args[1])
        elif operator == "random_distort":
            self.random_distort(data_path)


    def splitDataset(self,src_data_folder, target_data_folder, train_scale=0.8, val_scale=0.1, test_scale=0.1):
        print("开始数据集划分")
        class_names = os.listdir(src_data_folder)
        # 在目标目录下创建文件夹
        split_names = ['train', 'val', 'val']
        for split_name in split_names:
            split_path = os.path.join(target_data_folder, split_name)
            if os.path.isdir(split_path):
                pass
            else:
                os.mkdir(split_path)
            # 然后在split_path的目录下创建类别文件夹
            for class_name in class_names:
                class_split_path = os.path.join(split_path, class_name)
                if os.path.isdir(class_split_path):
                    pass
                else:
                    os.mkdir(class_split_path)

        # 按照比例划分数据集，并进行数据图片的复制
        # 首先进行分类遍历
        for class_name in class_names:
            current_class_data_path = os.path.join(src_data_folder, class_name)
            current_all_data = os.listdir(current_class_data_path)
            current_data_length = len(current_all_data)
            current_data_index_list = list(range(current_data_length))
            random.shuffle(current_data_index_list)

            train_folder = os.path.join(os.path.join(target_data_folder, 'train'), class_name)
            val_folder = os.path.join(os.path.join(target_data_folder, 'val'), class_name)
            test_folder = os.path.join(os.path.join(target_data_folder, 'test'), class_name)
            train_stop_flag = current_data_length * train_scale
            val_stop_flag = current_data_length * (train_scale + val_scale)
            current_idx = 0
            train_num = 0
            val_num = 0
            test_num = 0
            for i in current_data_index_list:
                src_img_path = os.path.join(current_class_data_path, current_all_data[i])
                if current_idx <= train_stop_flag:
                    copy2(src_img_path, train_folder)
                    train_num = train_num + 1
                elif (current_idx > train_stop_flag) and (current_idx <= val_stop_flag):
                    copy2(src_img_path, val_folder)
                    val_num = val_num + 1
                else:
                    copy2(src_img_path, test_folder)
                    test_num = test_num + 1
                current_idx = current_idx + 1

            print("*********************************{}*************************************".format(class_name))
            print(
                "{}类按照{}：{}：{}的比例划分完成，一共{}张图片".format(class_name, train_scale, val_scale, test_scale,
                                                      current_data_length))
            print("训练集{}：{}张".format(train_folder, train_num))
            print("验证集{}：{}张".format(val_folder, val_num))
            print("测试集{}：{}张".format(test_folder, test_num))


    '''
    读取源数据文件夹，按比例拆分数据集，返回拆分结果列表
    :param dataPath: 数据集文件夹
    :param test_size: 测试集比例
    '''
    def splitDataByRate(self, dataPath, test_size):
        dat = os.listdir(dataPath)
        train, test = train_test_split(dat, test_size = test_size)
        return train, test

    '''
    对CSV数据，按比例拆分数据集，返回拆分结果
    :param data: 数据
    :param label: 数据对应的标签
    :param test_size: 测试集比例
    '''
    def splitCsvData(self,data,label,test_size):
        x_train, x_test, y_train, y_test = train_test_split(data, label, test_size=test_size)
        return  x_train, x_test, y_train, y_test

    '''
    裁剪图像
    :param img_path: 数据集的路径
    :param points: 列表,points[0]、points[1]为裁剪区域左下坐标；points[2]、points[3]为裁剪区域右上坐标
    '''
    def imageCrop(self,dataPath, points):
        dataset = ImageFolder(dataPath)
        datalist = dataset.imgs[:]
        for l in datalist:
            img = Image.open(l[0])
            crop_img = img.crop(points)
            crop_img.save(l[0])
        dataset = ImageFolder(dataPath)
        return torch.utils.data.DataLoader(dataset)

    '''
    放大图像
    :param dataPath: 数据集路径
    :param props: 列表,props[0]、props[1]分别为图像宽和长的放大比例
    :param mode: 插值方法, INTER_NEAREST-最近邻插值法；INTER_AREA-基于局部像素的重采样
    INTER_LINEAR-双线性插值法(默认)；INTER_CUBIC-基于4x4像素邻域的3次插值法
    INTER_LANCZOS4-基于8x8像素邻域的Lanczos插值
    '''
    def enlargeImage(self,dataPath, props, mode=cv2.INTER_LINEAR):
        dataset = ImageFolder(dataPath)
        datalist = dataset.imgs[:]

        for l in datalist:
            img = cv2.imread(l[0])
            if img.all() == None:
                os._exit(0)
            enlargeImg = cv2.resize(img, (0, 0), fx=props[0], fy=props[1], interpolation=mode)
            cv2.imwrite(l[0], enlargeImg)

        dataset = ImageFolder(dataPath)
        return torch.utils.data.DataLoader(dataset)

    '''
    放大图像
    :param dataPath: 数据集路径
    :param props: 列表,props[0]、props[1]分别为图像宽和长的放大比例
    :param mode: 插值方法, INTER_NEAREST-最近邻插值法；INTER_AREA-基于局部像素的重采样
    INTER_LINEAR-双线性插值法(默认)；INTER_CUBIC-基于4x4像素邻域的3次插值法
    INTER_LANCZOS4-基于8x8像素邻域的Lanczos插值
    '''
    def shrinkImage(self, dataPath, props, mode=cv2.INTER_LINEAR):
        dataset = ImageFolder(dataPath)
        datalist = dataset.imgs[:]
        for l in datalist:
            img = cv2.imread(l[0])
            if img.all() == None:
                os._exit(0)
            height, width = img.shape[:2]
            size = (int(width * props[0]), int(height * props[1]))
            shrinkImg = cv2.resize(img, size, interpolation=mode)
            cv2.imwrite(l[0], shrinkImg)
        dataset = ImageFolder(dataPath)
        return torch.utils.data.DataLoader(dataset)


    '''
    随机改变亮暗、对比度和颜色等
    :param dataPath: 数据集路径
    '''
    def random_distort(self,dataPath):
        # 随机改变亮度
        def random_brightness(img, lower=0.5, upper=1.5):
            e = np.random.uniform(lower, upper)
            return ImageEnhance.Brightness(img).enhance(e)

        # 随机改变对比度
        def random_contrast(img, lower=0.5, upper=1.5):
            e = np.random.uniform(lower, upper)
            return ImageEnhance.Contrast(img).enhance(e)

        # 随机改变颜色
        def random_color(img, lower=0.5, upper=1.5):
            e = np.random.uniform(lower, upper)
            return ImageEnhance.Color(img).enhance(e)

        ops = [random_brightness, random_contrast, random_color]
        np.random.shuffle(ops)

        dataset = ImageFolder(dataPath)
        datalist = dataset.imgs[:]
        for l in datalist:
            img = cv2.imread(l[0])
            img = Image.fromarray(img)
            img = ops[0](img)
            img = ops[1](img)
            img = ops[2](img)
            img = np.asarray(img)
            cv2.imwrite(l[0], img)

        dataset = ImageFolder(dataPath)
        return torch.utils.data.DataLoader(dataset)
