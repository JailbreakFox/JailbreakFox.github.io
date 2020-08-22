---
title: DeepFakes(未完成)
tags: 视觉，应用， AI
date: 2019-05-21 09:52:15
grammar_cjkRuby: true
---

### *0x00 引言*
&emsp;&emsp; 这是一款于2017年末出名的人脸交换技术，由于是开源程序，这里直接能clone到[源码](https://github.com/deepfakes/faceswap)。目前有两种安装方法:1)release版本。如果只是用来尝试换脸，则直接下载发行版本即可;2)搭建开发环境。如果是想开发，则直接搭建Anaconda+TensorFlow的开发环境，已经在之前的[博文](https://jailbreakfox.github.io/2019/05/16/环境配置-机器学习)内介绍过。
&emsp;&emsp;这里主要说明一下该项目原理以及开发环境内的操作流程。

### *0x01 DeepFakes原理*
&emsp;&emsp; DeepFakes的核心是一个“自动编码器”，这个“自动编码器”实际上是一个深度神经网络，它能够接收数据输入，并将其压缩成一个小的编码，然后从这个编码中重新生成原始的输入数据。

### *0x02 DeepFakes使用教程*
&emsp;&emsp; 由于网上基本搜索不到该项目的具体使用方法，这里根据DeepFakes官网的英文教程，总结了一套自己的使用流程，内容均使用终端模式，若使用GUI需访问官网教程。以下使用DeepFakes实现胡歌与刘亦菲的换脸。
```
1 图片收集
  1.1 谷歌图片批量下载
2 Extract人脸
3 训练模型
4 人脸转换
  4.1 图片转换人脸
```

***1、图片收集***
&emsp;&emsp;训练AI的图片资源的获取以及前期处理非常重要，如果没有良好的符合标准图片进行训练的话，也就无法获得良好的模型。一般途径有直接去网络上寻找图片资源，或者截取视频帧两种方法。
***1.1、谷歌图批量下载片***
&emsp;&emsp;这里推荐一款极为好用的图片收集工具google-images-download，它可以直接从谷歌图片内爬取我们的目标人物图片，可直接从[GitHub](https://github.com/hardikvasa/google-images-download)上获取。
```py
#直接在Anaconda环境下pip安装
pip install google-images-download
#首先给自己的Anaconda Prompt终端设置SS代理，因为要去谷歌爬取，所以需要翻墙。
set http_proxy=127.0.0.1:1080
set https_proxy=127.0.0.1:1080
#cd到希望存放照片的文件夹，这里以C:\Users\Desktop\为例
cd C:\Users\Desktop\Downloads
#收集目标人物的图片，这里-k参数表示搜索关键词，-l参数代表爬取的张数
googleimagesdownload -k "胡歌" -l 100
googleimagesdownload -k "刘亦菲" -l 100
#为了方便后面的操作，我们分别将胡歌和刘亦菲的照片放到路径C:\Users\Desktop\picin和C:\Users\Desktop\picin2下
```
&emsp;&emsp;爬取完之后注意需要清理一些不好的图片，方便后续处理。

***2、Extract人脸***
&emsp;&emsp;由于目前得到的图片可能是全身照，而我们只需要脸部照片，官网上给出了从图片和视频抽取人脸的代码：
```py
#从图片抽取人脸，并分别放入picout于picout2文件夹
python faceswap.py extract -i C:\Users\Desktop\picin -o C:\Users\Desktop\picout
python faceswap.py extract -i C:\Users\Desktop\picin2 -o C:\Users\Desktop\picout2
#或者从目标视频文件内抽取人脸(未测试)
#python faceswap.py extract -i C:\Users\Desktop\picin.mp4 -o C:\Users\Desktop\picout
```

***3、训练模型***
&emsp;&emsp;在得到了用于训练编码器模型的初始输入图片集以后，我们需要实现训练过程：
```py
#-A与-B参数为之前得到的人脸图片，-m参数代表我们的模型存放文件夹，-p参数代表预览训练过程
python faceswap.py train -A C:\Users\Desktop\picout -B C:\Users\Desktop\picout2 -m C:\Users\Desktop\picoutsum -p
```

***4、人脸转换***
&emsp;&emsp;在得到编码器的模型以后，我们就可以使用它来转换我们人脸了，这里可以实现图片和视频的转换。
***4.1、图片转换人脸***
&emsp;&emsp;这里直接实现将1.1节爬取得到的胡歌人脸转换为刘亦菲的脸。
```py
#-i参数代表想转换的图片，-o表示转换后图片存放文件夹，-m表示使用的模型
python faceswap.py convert -i C:\Users\Desktop\picin -o C:\Users\Desktop\converted -m C:\Users\Desktop\picoutsum
```
&emsp;&emsp;转换的结果非常模糊，由于硬件的限制，这里使用CPU来处理，所以只爬取了100张训练图片，但是DeepFakes的使用过程都是一样的。

### *0x03 引用文献*