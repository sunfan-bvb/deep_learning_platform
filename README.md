# deep_learning_platform

这是一个深度学习平台，可以通过拖拽组成网络模型，在线上进行调参、训练、测试。

## 技术路线
前端：vue2, jsPlumb
后端：flask，mysql，pytorch
前后端认证：jwt

## 主要功能

### login
首先是注册和登录，包含容错。
<video src="/videos/login.mp4" controls="controls">您的浏览器不支持播放该视频！</video>

### system
新的账号登录进入后，没有任何项目，可以新建三种不同的项目。
<video src="/videos/system.mp4" controls="controls">您的浏览器不支持播放该视频！</video>

### train
系统内置了几个数据集，也可以用户上传个人数据集进行训练和测试，这里可能涉及数据量过大，分片上传的问题，系统中没有涉及，可以自行完善。我们直接用内置数据集演示。
通过拖拽和连线完成模型搭建，点击模块可以设置参数，针对不同模型系统定义了不同的初始化参数，用户可以自行更改参数，也可以更改保存模型的名字，在训练结束后模型会自动下载到本地，同时，服务器也保存一份，方便用户后续的测试。
<video src="/videos/train.mp4" controls="controls">您的浏览器不支持播放该视频！</video>

### loss
训练结束后也支持loss和evaluation的图片下载。
<video src="/videos/loss.mp4" controls="controls">您的浏览器不支持播放该视频！</video>

### test
我们开发了两种测试模式，这一种可以上传多个文件批量测试。测试后无法直接查看测试结果，结果支持打包下载查看。
<video src="/videos/test.mp4" controls="controls">您的浏览器不支持播放该视频！</video>

### rename
自定义文件名称。
<video src="/videos/rename.mp4" controls="controls">您的浏览器不支持播放该视频！</video>

### infer
第二种测试方式，只支持单次上传一组输入文件，可视化输出结果。可以支持不同类型的输出。
<video src="/videos/csv_infer.mp4" controls="controls">您的浏览器不支持播放该视频！</video>
<video src="/videos/png_infer.mp4" controls="controls">您的浏览器不支持播放该视频！</video>

### ide
我们还内嵌了一个简单的python ide，可以在服务器当前环境下运行。
<video src="/videos/ide.mp4" controls="controls">您的浏览器不支持播放该视频！</video>

### log
我们还定义了日志管理，包含登录、训练等结果的日志。
<video src="/videos/log.mp4" controls="controls">您的浏览器不支持播放该视频！</video>


## 运行方式
1. 首先配置并启动mysql数据库。
2. 后端
按照requirements.txt安装环境并激活。
```bash
  cd 到 flask 路径下
  python app.py
```
4. 前端
```bash
  cd 到 panel 路径下
  npm run serve -- --port 8081
```


