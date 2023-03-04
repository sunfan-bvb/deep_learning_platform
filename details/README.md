我使用工厂模式对算法的封装和调用过程进行了解构，使得添加一个模型变得容易。

首先，软件架构图中展示了具体的后端架构。

而网络封装接口说明详细地定义了如何去封装一个已经能在服务器上跑通的模型，来把它加入到平台中。请严格根据说明的定义来放置模型文件和定义Trainer及Infer类。

接下来，就是如何在工厂中加入新的模型。

后端步骤：

1. 将Dataset类文件放到dataset目录下。
2. 将dataset/PreFactory.py中的PreFactory类做两个改动。
  (1)将类dataset的定义如源代码中的格式加入到constructPreClass函数中。
  (2)将默认的batchsize值加入到getBatchSize函数中。
3. 在RunHelp.py文件的RunHelp类中，找到所有包含模型名称的列表，将新的模型名称加进去。这一步可以在后续代码中继续优化。
4. 将模型类按说明放好后，将model/ModelFactory.py文件中的四个函数加入新的类定义（Trainer、Infer类的构造、训练函数的默认调用以及获取loss的方法调用）。

前端步骤：

在src/components/data_A.js文件中加入新的节点定义。模型名称要与后端中的模型名称一致。

至此，新的模型就可以使用了。
