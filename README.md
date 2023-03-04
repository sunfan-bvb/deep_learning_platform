# deep_learning_platform

这是一个深度学习平台，可以通过拖拽组成网络模型，在线上进行调参、训练、测试。

## 技术路线
前端：vue2, jsPlumb
后端：flask，mysql，pytorch
前后端认证：jwt

## 主要功能

### login
首先是注册和登录，包含容错。

<img src="/videos/login.gif" width="600px">

### system
新的账号登录进入后，没有任何项目，可以新建三种不同的项目。

<img src="/videos/system.gif" width="600px">

### train
系统内置了几个数据集，也可以用户上传个人数据集进行训练和测试，这里可能涉及数据量过大，分片上传的问题，系统中没有涉及，可以自行完善。我们直接用内置数据集演示。
通过拖拽和连线完成模型搭建，点击模块可以设置参数，针对不同模型系统定义了不同的初始化参数，用户可以自行更改参数，也可以更改保存模型的名字，在训练结束后模型会自动下载到本地，同时，服务器也保存一份，方便用户后续的测试。

<img src="/videos/train.gif" width="600px">

### loss
训练结束后也支持loss和evaluation的图片下载。

<img src="/videos/loss.gif" width="600px">

### test
我们开发了两种测试模式，这一种可以上传多个文件批量测试。测试后无法直接查看测试结果，结果支持打包下载查看。

<img src="/videos/test.gif" width="600px">

### rename
自定义文件名称。

<img src="/videos/rename.gif" width="600px">

### infer
第二种测试方式，只支持单次上传一组输入文件，可视化输出结果。可以支持不同类型的输出。

<img src="/videos/cvs_infer.gif" width="600px">

<img src="/videos/png_infer.gif" width="600px">

### ide
我们还内嵌了一个简单的python ide，可以在服务器当前环境下运行。

<img src="/videos/ide.gif" width="600px">

### log
我们还定义了日志管理，包含登录、训练等结果的日志。

<img src="/videos/log.gif" width="600px">


## 运行方式
1. 首先配置并启动mysql数据库。
2. 后端
按照requirements.txt安装环境并激活。
```bash
  cd 到 flask 路径下
  python app.py
```
3. 前端
```bash
  cd 到 panel 路径下
  npm run serve -- --port 8081
```

### 其他
模型的扩展细节写在了detail文件中。
由于这个项目的需求逐步增加，最后又无疾而终，因此代码的架构不是很好，代码量比较大也没有写注释，而且存在一些bug没有解决。但是已经有了一个初步的深度学习可视化框架，安装到服务器上就可以使用（把玩）了。
