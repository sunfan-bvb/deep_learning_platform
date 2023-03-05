# -*- coding: utf-8 -*-
"""
@Time ： 2022/4/5 13:39
@Auth ： FAN SUN
@File ：ModelFactory.py
@IDE ：PyCharm

"""
from model.FEA import FEA, FEA_Trainer, FEA_Infer
import model.change_detection_pytorch as cdp
from model.ChangeDetection import CD_Trainer, CD_Infer
from model.mask_rcnn.backbone import resnet50_fpn_backbone
from model.mask_rcnn.network_files import MaskRCNN
import torch
from model.MaskRCNN import Segmentation_Train, Segmentation_Infer
from model.CycleGAN import GeneratorUNet, Discriminator, CycleGAN_Trainer, CycleGAN_Infer


def getModel(name):
    if name == "fea":
        return FEA(7)
    if name == "change detection":
        return cdp.Unet(
                    encoder_name="resnet34",  # choose encoder, e.g. mobilenet_v2 or efficientnet-b7
                    encoder_weights="imagenet",  # use `imagenet` pre-trained weights for encoder initialization
                    in_channels=3,  # model input channels (1 for gray-scale images, 3 for RGB, etc.)
                    classes=2,  # model output channels (number of classes in your datasets)
                    siam_encoder=True,  # whether to use a siamese encoder
                    fusion_form='concat',  # the form of fusing features from two branches. e.g. concat, sum, diff, or abs_diff.
                )
    if name == "mask rcnn":
        backbone = resnet50_fpn_backbone(pretrain_path="/home/DL/flask/model/mask_rcnn/backbone/resnet50.pth", trainable_layers=3)
        model = MaskRCNN(backbone, num_classes=91)
        # coco weights url: "https://download.pytorch.org/models/maskrcnn_resnet50_fpn_coco-bf2d0c1e.pth"
        weights_dict = torch.load("/home/DL/Gaozzzz/Segmentation/mask_rcnn/weights/maskrcnn_resnet50_fpn_coco.pth", map_location="cpu")
        for k in list(weights_dict.keys()):
            if ("box_predictor" in k) or ("mask_fcn_logits" in k):
                del weights_dict[k]
        print(model.load_state_dict(weights_dict, strict=False))
        return model
    if name == "cycle gan":
        generator = GeneratorUNet()
        discriminator = Discriminator()
        return [generator, discriminator]


def trainModel(name, out_path, train_dataloader, test_dataloader, model, params, q, pretrainModel, file_name, save_type):
    if name == "fea":
        FEA_Trainer().train(out_path, train_dataloader, test_dataloader, model=model, model_params=params, q=q, pretrainModel=pretrainModel, file_name=file_name)
    if name == "change detection":
        CD_Trainer(out_path, train_dataloader=train_dataloader, val_dataloader=test_dataloader, model=model, model_params=params, q=q, pretrainModel=pretrainModel, file_name=file_name).train()
    if name == "mask rcnn":
        Segmentation_Train(out_path, train_dataloader=train_dataloader, val_dataloader=test_dataloader, model=model, model_params=params, q=q, pretrainModel=pretrainModel, file_name=file_name).mask_rcnn_train()
    if name == "cycle gan":
        CycleGAN_Trainer(out_pathdir=out_path, model={'gen': model[0], 'dis': model[1]}, train_dataloader=train_dataloader, val_dataloader=test_dataloader, param_save_type=save_type, model_params=params).train()


def getLossMatrix(name, model):
    train_loss, train_metric, val_loss, val_metric = [], [], [], []
    if name == "fea":
        train_loss = model.get_train_loss()
        train_metric = model.get_train_rsquare()
        val_loss = model.get_val_loss()
        val_metric = model.get_val_rsquare()
    if name == "change detection":
        train_loss = model.get_train_loss1_statistic()
        train_metric = model.get_train_metric2_statistic()
        val_loss = model.get_valid_loss1_statistic()
        val_metric = model.get_valid_metric2_statistic()
    if name == "cycle gan":
        train_loss = model[0].get_train_loss()
        train_metric = model[1].get_train_loss()
        val_loss = model[0].get_train_loss()
        val_metric = model[1].get_train_loss()
    return train_loss, train_metric, val_loss, val_metric


def testModel(name, input_path, model_path, save_path):
    if name == "fea":
        FEA_Infer().infer(input_path[0], model_path, save_path)
    if name == "change detection":
        CD_Infer().infer(input_path[0], input_path[1], model_path, save_path)
    if name == "mask rcnn":
        Segmentation_Infer(input_path[0], model_path, save_path).mask_rcnn_infer()
    if name == "cycle gan":
        CycleGAN_Infer(input_path[0], model_path, save_path).infer()

