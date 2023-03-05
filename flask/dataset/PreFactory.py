from dataset.YoloDataset import VOCDataset
from dataset.FEADataset import FEADataset
from dataset.LevirCDDataset import LEVIR_CD_Dataset
from dataset.MaskRCNNDataset import VOCInstances
from dataset.CycleGANDataset import ImageDataset
import torchvision.transforms as transforms

# -*- coding: utf-8 -*-

"""
@Time ： 2022/4/5 09:13
@Auth ： FAN SUN
@File ：PreFactory.py
@IDE ：PyCharm

"""
class PreFactory:
	"""
		根据name返回类实例
		name: 运行类名
	"""
	def constructPreClass(self, name, path, process, params, train):
		if name == "yolo":
			print(path, process, params, train)
			return VOCDataset(data_dir=path, preprocess=process, params=params, train=train)
		if name == "fea":
			return FEADataset(data_dir=path, preprocess=process, params=params, train=train)
		if name == "change detection":
			return LEVIR_CD_Dataset(path, sub_dir_1='A', sub_dir_2='B', img_suffix='.png', ann_dir=path, debug=False, train=train)
		if name == "mask rcnn":
			return VOCInstances(voc_root=path, train=train)
		if name == "cycle gan":
			transforms_ = [
				transforms.Resize((256, 256), ),
				transforms.ToTensor(),
				transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
			]
			return ImageDataset(root=path, transforms_=transforms_, train=train)
		# elif name == "ssd":
		# 	return SSDDataset(path, preprocess, params, train)
		# ......

	def getBatchSize(self, name, batch):
		if batch != -1:
			return batch
		# define default batch size
		if name == "yolo":
			return 128  # ?
		if name == "fea":
			return 512
		if name == "change detection":
			return 8
		if name == "mask rcnn":
			return 1
		if name == "cycle gan":
			return 1
