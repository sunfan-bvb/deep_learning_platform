import json
import os.path

from dataset.PreFactory import PreFactory
from torch.utils.data import DataLoader
from model.ModelFactory import getModel, trainModel, getLossMatrix, testModel
# -*- coding: utf-8 -*-
"""
@Time ： 2022/4/5 09:16
@Auth ： FAN SUN
@File ：RunHelp.py
@IDE ：PyCharm

"""


class RunHelp:
    def __init__(self):
        self.name, self.path, self.pro, self.para, self.batch, self.out_path, self.model_param, self.epoch, self.saveType = "", "", "", [], -1, "", {}, 0, "best"
        self.model, self.pretrainModel = None, None

    def getparams(self, process, params, saveP, g_path, g_name, project_name):
        '''
            process, params, saveP ->
            model, path, process, params, batch_size, out_path, model_param, epoch
        '''
        # pro_l, para_l = [], []
        model, path, pro, para, batch, out_path, model_param = "", "", "", [], -1, "", {}
        for i in range(len(process)):
            if process[i] in ["crop", "enlarge", "shrink", "random_distort"]:
                # pro_l.append(process[i])
                # para_l.append(params[i])
                pro = process[i]
                para = params[i]
            if process[i] in ["ssd", "yolo", "fea", "change detection", "mask rcnn", "cycle gan"]:
                model = process[i]
                model_param = params[i]
                # data = str(model_param, 'utf8')
                # data = json.loads(model_param)
                batch = -1 if "batch" not in model_param.keys() or model_param['batch'] == '' else int(model_param["batch"])
            if process[i] in ["upload"]:
                path = g_path + g_name + "/data/" + params[i]['packname']
            if process[i] in ["personal"]:
                path = g_path + g_name + "/data/" + params[i]['package']
            if process[i] in ["node", "change_detection"]:
                path = g_path + "shared_data/" + process[i]
            if process[i] in ["coco2017", "levir-cd", "yolo_dataset", "VOCdevkit"]:
                path = "/home/DL/Gaozzzz/data/" + process[i]
            if process[i] in ["cycle_gan"]:
                path = "/home/DL/GAN/CycleGAN/datasets"
        out_path = g_path + g_name + "/params/" + project_name + "/" + saveP[2]
        if not os.path.exists(g_path + g_name + "/params/" + project_name):
            os.makedirs(g_path + g_name + "/params/" + project_name)
        epoch = int(saveP[1])
        saveType = saveP[0]
        pretrainModel = None if saveP[3] == "不使用预训练" else g_name + "/params/" + project_name + "/" + saveP[3] + ".pth.tar"
        return model, path, pro, para, batch, out_path, model_param, epoch, saveType, pretrainModel

    def getmodelname(self, process):
        model = ""
        for i in range(len(process)):
            if process[i] in ["ssd", "yolo", "fea", "change detection", "mask rcnn", "cycel gan"]:
                model = process[i]
        return model

    def operation(self, name, path, process, params, batch_size):
        # give name, path, process, params, batch
        train_dataset = PreFactory().constructPreClass(name, path, process, [10, 100, 200, 200], True)
        test_dataset = PreFactory().constructPreClass(name, path, process, [10, 100, 200, 200], False)
        print("batch-name:", name)
        batch_size = PreFactory().getBatchSize(name, batch_size)
        print("batch-size: ", batch_size)
        if name == "mask rcnn":
            train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, pin_memory=True,
                                      collate_fn=train_dataset.collate_fn)
            test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=True, pin_memory=True,
                                     collate_fn=train_dataset.collate_fn)
        else:
            train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, pin_memory=True)
            test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=True, pin_memory=True)
        return train_loader, test_loader
        # for dataset in [train_dataset, test_dataset]:
        #     for data, box, label in dataset:
        #         print(data)

    def getmodel(self, process, params, saveP, g_path, g_name, project_name):
        self.name, self.path, self.pro, self.para, self.batch, self.out_path, self.model_param, self.epoch, self.saveType, self.pretrainModel = \
            self.getparams(process, params, saveP, g_path, g_name, project_name)
        self.model = getModel(self.name)
        return self.model, self.name

    def train(self, process, params, q, file_name):
        # name, path, pro, para, batch, out_path, model_param, epoch = self.getparams(process, params, saveP, g_path, g_name)
        train_loader, test_loader = self.operation(self.name, self.path, process, params, self.batch)
        trainModel(self.name, self.out_path, train_loader, test_loader, self.model, self.model_param, q, self.pretrainModel, file_name, self.saveType)

    def getLossMatrix(self, name, g_model):
        return getLossMatrix(name, g_model)

    def infer(self, g_path, g_name, param_name, data_name, pro_name, model_name):
        input_path = []
        for i in data_name:
            input_path.append(g_path + g_name + "/val/" + pro_name + "/" + i)
        model_path = g_path + g_name + "/params/" + pro_name + "/" + param_name
        output_path = g_path + g_name + "/results/" + pro_name
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        if len(data_name) == 1:
            save_path = output_path + "/" + data_name[0]
        else:
            save_path = output_path + "/" + data_name[0].split(".")[0] + "_" + data_name[1].split(".")[0] + ".png"
        testModel(model_name, input_path, model_path, save_path)

    def getModelType(self, g_path, g_name, project):
        path = g_path + g_name + "/projects/visual/" + project + ".txt"
        with open(path, 'r') as f:
            j = f.readline()
            j = "\"".join(j.split("'"))
            data = eval(j)
        model = ''
        for p in data['nodeList']:
            if p['name'] in ["fea", "ssd", "yolo", "变化检测", "mask rcnn", "cycle gan"]:
                model = p['name']
        # d = {"fea": "csv", "changedetection": "image_2"}
        d = {"变化检测": "change detection"}
        return model if model not in d.keys() else d[model]
