---
title: pytorch-BP神经网络拟合非线性函数
tags: pytorch，神经网络，机器学习
date: 2018-12-12 20:41:00
grammar_cjkRuby: true
---

### *0x00 引言*
&emsp;&emsp;神经网络是机器学习中常用的一种方法，而BP神经网络在近些年是运用极为广泛的一种，如[吴恩达课程](https://study.163.com/course/courseMain.htm?courseId=1004570029)<sup>[1]</sup>所涉及的神经网络方面的课程便是用的BP神经网络。由于近期刚接触pytorch，以及毕设上的需要，尝试写一篇有关用pytorch和BP神经网络对非线性函数进行拟合的文章。

### *0x01 BP神经网络的概念与原理*
&emsp;&emsp;BP(back propagation)神经网络最初是1986年由Rumelhart和McClelland提出的概念，其是一种按照误差逆向传播算法训练的多层前馈神经网络，也是目前应用最广泛的神经网络<sup>[2]</sup>。
```
1 人工神经元
  1.1 神经元模型
  1.2 激活函数
2 BP神经网络的结构与原理
  2.1 前向传播算法
  2.2 代价函数
  2.3 反向传播算法
```
***1 人工神经元***
***1.1 神经元模型***
&emsp;&emsp;神经生理学和神经解剖学的研究结果表明，神经元是脑组织的基本单元，同时也是神经系统结构与功能的单位。人类大脑中的神经元互相连接，构成了一庞大复杂的网络，即生物神经网络。神经元在结构上是由细胞体、树突、轴突以及突触四个部分组成的。树突是一种管状延伸物，其作用是接受来自周围的神经冲击信息，相当于细胞的输入端，信息流从树突发出，经过细胞体，接着由轴突传出，轴突相当于细胞的输出端。突触是神经元之间通信的媒介，相当于是不同神经元之间的输入输出接口。
<div align=center>![神经元1](神经元1.jpg)<div align=left>

&emsp;&emsp;借鉴神经元的存在形式，神经元模型便应运而生。早在1943年，心理学家McCulloch和数学家W.Pitts就在分析总结神经元基本特性的基础上提出了MP模型，该模型经过不断改进后，形成了现在被广泛使用的BP神经元模型。人工神经元模型应具备三个要素：
&emsp;&emsp;&emsp;&emsp;1）至少具备一组突触或连接，其连接强度常用表示，也可称之为权值；
&emsp;&emsp;&emsp;&emsp;2）神经元的输出是由多个输入经过加权处理，并通过累加算法得到的；
&emsp;&emsp;&emsp;&emsp;3）具备一个激励函数用于限制神经元的输出。激励函数的作用是将输出信号限制在一个范围内，通常设置值为[0,1]或[-1,1]。
&emsp;&emsp;一个典型的人工神经元模型如下图所示：
<div align=center>![神经元2](神经元2.jpg)<div align=left>
&emsp;&emsp;其中$x_{j}\left ( j=1,2,\cdots ,N \right )$为输入信号,$w_{ij}$为连接权值，$\theta_{i}$为偏置量，$g\left( \cdot \right )$是激励函数，$y_{i}$是神经元的输出。输出与输入量的关系可用下式表示：
$$y_{i}=g\left ( \sum_{j=1}^{N}w_{ij}x_{j}+\theta _{i} \right )$$

***1.2 激活函数***
&emsp;&emsp;激励函数$g\left ( \cdot  \right )$有多种选择，常用的基本激励函数有以下几种<sup>[3]</sup>：
&emsp;&emsp;1）sigmoid函数
&emsp;&emsp;&emsp;&emsp;又称为S型函数，是神经网络中使用最多的激励函数，其表达式如下所示：
$$g\left ( t \right )=\frac{1}{1+exp(-\alpha t)}$$
&emsp;&emsp;&emsp;&emsp;式中的$\alpha$代表sigmoid函数的斜率参数，其曲线图如下所示：
<div align=center>![激活函数1](激活函数1.jpg)<div align=left>
&emsp;&emsp;2）tanh函数
&emsp;&emsp;&emsp;&emsp;tanh函数是将$\left ( -\infty ,+\infty  \right )$的数映射到$\left ( -1,1 \right )$之间，其表达式与图形如下所示：
$$g\left ( t \right )=\frac{e^{t}-e^{-t}}{e^{t}+e^{-t}}$$
<div align=center>![激活函数2](激活函数2.jpg)<div align=left>
&emsp;&emsp;&emsp;&emsp;tanh函数在零点附近很短一段区域内可看做线性的。由于tanh函数均值为0，因此弥补了sigmoid函数均值为0.5的缺点。tanh函数的缺点同sigmoid函数的第一个缺点一样，当t很大或很小时，$g^{'}\left ( t \right )$接近于0，会导致梯度很小，权重更新非常缓慢，即梯度消失问题。

&emsp;&emsp;3）ReLU函数
&emsp;&emsp;&emsp;&emsp;ReLU函数又称为修正线性单元（Rectified Linear Unit），是一种分段线性函数，其弥补了sigmoid函数以及tanh函数的梯度消失问题。ReLU函数的公式以及图形如下：
$$g\left ( t \right )=\begin{cases}
0 & t < 0 \\\
t & t > 0 
\end{cases}$$
<div align=center>![激活函数3](激活函数3.jpg)<div align=left>
&emsp;&emsp;&emsp;&emsp;ReLU函数的优点是在输入为正数的时候，不存在梯度消失问题。且计算速度要快很多。ReLU函数只有线性关系，不管是前向传播还是反向传播，都比sigmod和tanh要快很多。ReLU函数的缺点是当输入为负时，梯度为0，会产生梯度消失问题。

***2 BP神经网络的结构与原理***
&emsp;&emsp;神经网络模型是许多逻辑单元按照不同层级组织的网络，其每层的输出变量均为下一层的输入变量。最简单的神经网络一般包含三层，分别是输入层、隐含层以及输出层，如下图所示：
<div align=center>![bp1](bp1.jpg)<div align=left>

&emsp;&emsp;图中第一层为输出层，第二层为隐含层，最后一层为输出层。$a_{i}^{j}$代表第j层的第i个激活单元，其中神经元$x_{0}$、$a_{0}^{\left ( 2 \right )}$均为偏置单元，$\theta ^{j}$代表权重矩阵。

***2.1 前向传播算法***
对应上图可以得到激活单元与输出的表达式:
$$a_{1}^{\left ( 2 \right )}=g\left ( \theta_{10}^{(1)}x_{0}+\theta_{11}^{(1)}x_{1}+\theta_{12}^{(1)}x_{2}+\theta_{13}^{(1)}x_{3}  \right )$$
$$a_{2}^{\left ( 2 \right )}=g\left ( \theta_{20}^{(1)}x_{0}+\theta_{21}^{(1)}x_{1}+\theta_{22}^{(1)}x_{2}+\theta_{23}^{(1)}x_{3}  \right )$$
$$a_{3}^{\left ( 2 \right )}=g\left ( \theta_{30}^{(1)}x_{0}+\theta_{31}^{(1)}x_{1}+\theta_{32}^{(1)}x_{2}+\theta_{33}^{(1)}x_{3}  \right )$$
$$h_{\theta }\left ( x \right )=g\left ( \theta_{10}^{(2)}a_{0}^{(2)}+\theta_{11}^{(2)}a_{1}^{(2)}+\theta_{12}^{(2)}a_{2}^{(2)}+\theta_{13}^{(2)}a_{3}^{(2)}  \right )$$
&emsp;&emsp;当给定神经网络一组输入值，便能根据上述公式推导出输出，这种从左到右的算法称为前向传播算法。

***2.2 代价函数<sup>[4]</sup>***
&emsp;&emsp;假设有训练样本(x, y)，模型为h，参数为。且$h\left ( \theta  \right )=\theta ^{T}x$，其中$\theta ^{T}$表示$\theta$的转置。
&emsp;&emsp;任何能够衡量模型预测值$h\left ( \theta  \right )$与真实值y之差的函数都可以称为代价函数，若有多个样本，则将所有代价函数的取值求平均值，记作$J\left ( \theta  \right )$。
&emsp;&emsp;在逻辑回归中，最常用的代价函数是交叉熵，其表达式如下：
$$J\left ( \theta  \right )=-\frac{1}{m}\left [ \sum_{i=1}^{m}y^{(i)}logh_{\theta}(x^{(i)})+(1-y^{(i)})log(1-h_{\theta}(x^{(i)})) \right ]+\frac{\lambda }{2m}\sum_{j=1}^{n}\theta_{j}^{2}$$
&emsp;&emsp;神经网络的代价函数与逻辑回归的代价函数非常相似：
$$J\left ( \theta  \right )=-\frac{1}{m}\left [ \sum_{i=1}^{m}\sum_{k=1}^{k}y^{(i)}logh_{\theta }(x^{(i)})+(1-y^{(i)})log(1-h_{\theta }(x^{(i)})) \right ]+\frac{\lambda }{2m}\sum_{l=1}^{L-1}\sum_{i=1}^{s_{l}}\sum_{j=1}^{s_{l}+1}\left ( \Theta_{ji}^{(1)} \right )^{2}$$

***2.3 反向传播算法<sup>[5]</sup>***
&emsp;&emsp;在得到前向传播以及代价函数的计算结果之后，需要将误差反向传播，以修改神经网络的权值。以隐含层至输出层的权值更新为例，将输出层神经元简化为下图：
<div align=center>![bp2](bp2.jpg)<div align=left>
&emsp;&emsp;图中，$E_{o1}$为考虑代价函数得到的总误差，$T_{o1}$为目标输出值，$O_{o1}$为前向传播得到的输出值，$N_{o1}$为$O_{o1}$被激活前的值，h为隐藏层输出值，w为权值。则权值$w_{21}$对整体误差的影响可由链式法则得：
$$\frac{\partial E_{o1}}{\partial w_{21}}=\frac{\partial E_{o1}}{\partial O_{o1}}\cdot \frac{\partial O_{o1}}{\partial N_{o1}}\cdot \frac{\partial N_{o1}}{\partial w_{21}}$$
&emsp;&emsp;设学习速率为$\eta $，则$w_{21}$的更新权值$w_{21}^{+}$为：
$$w_{21}^{+}=w_{21}-\eta \cdot \frac{\partial E_{o1}}{\partial w_{21}}$$

### *0x02 代码实例*
***拟合线性函数***

```python
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import random

x1 = torch.unsqueeze(torch.linspace(2, 4, 100), dim=1)
x2 = x1
x = torch.zeros(10000,2)
x0 = x

for i in range(0,10000):
    j1 = random.randint(0,99)
    j2 = random.randint(0,99)
    x0[i][0] = x1[j1]
    x0[i][1] = x2[j2]

x3 = x0[:,0].unsqueeze(0).t()
x4 = x0[:,1].unsqueeze(0).t()
y = 1/x3+1/x4

class Net(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()
        self.hidden1 = torch.nn.Linear(n_feature, n_hidden)   # hidden layer
        self.hidden2 = torch.nn.Linear(n_hidden, n_hidden)
        self.predict = torch.nn.Linear(n_hidden, n_output)   # output layer

    def forward(self, x):
        x = F.relu(self.hidden1(x))      # activation function for hidden layer
        x = F.relu(self.hidden2(x))
        x = self.predict(x)             # linear output
        return x

net = Net(n_feature=2, n_hidden=10,n_output=1)     # define the network
print(net)  # net architecture

optimizer = torch.optim.SGD(net.parameters(), lr=0.2)
loss_func = torch.nn.MSELoss()  # this is for regression mean squared loss

for t in range(200):
    prediction = net(x)     # input x and predict based on x

    loss = loss_func(prediction, y)     # must be (1. nn output, 2. target)

    optimizer.zero_grad()   # clear gradients for next train
    loss.backward()         # backpropagation, compute gradients
    optimizer.step()        # apply gradients
 
print(net(torch.Tensor([3,3])))
```

***拟合非线性函数***
```python
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import random
import math

x1_0 = torch.unsqueeze(torch.linspace(-10, 10, 1000), dim=1)
x2_0 = x1_0
x3_0 = x1_0
x4_0 = x1_0
x5 = 1
x7_0 = torch.unsqueeze(torch.linspace(-0.785, 0.785, 100), dim=1)
x8_0 = x7_0
x9_0 = x7_0
x10_0 = x7_0

kd1 = 1.2
kp1 = 0.8
k1 = -2
g = 10

x = torch.zeros(10000,8)
x0 = x

for i in range(0,10000):
    j1 = random.randint(0,999)
    j2 = random.randint(0,999)
    j3 = random.randint(0,999)
    j4 = random.randint(0,999)
    j5 = random.randint(0,99)
    j6 = random.randint(0,99)
    j7 = random.randint(0,99)
    j8 = random.randint(0,99)
    x0[i][0] = x1_0[j1]
    x0[i][1] = x2_0[j2]
    x0[i][2] = x3_0[j3]
    x0[i][3] = x4_0[j4]
    x0[i][4] = x7_0[j5]
    x0[i][5] = x8_0[j6]
    x0[i][6] = x9_0[j7]
    x0[i][7] = x10_0[j8]

x1 = x0[:,0].unsqueeze(0).t()
x2 = x0[:,1].unsqueeze(0).t()
x3 = x0[:,2].unsqueeze(0).t()
x4 = x0[:,3].unsqueeze(0).t()
x7 = x0[:,4].unsqueeze(0).t()
x8 = x0[:,5].unsqueeze(0).t()
x9 = x0[:,6].unsqueeze(0).t()
x10 = x0[:,7].unsqueeze(0).t()

y = -torch.cos(x7)*(kd1*(-x2)+kp1*(-x1)-k1*x8)/(x5*torch.cos(x9))+2*torch.sin(x9)*x8*x10/torch.cos(x9)-g*torch.sin(x7)/(x5*torch.cos(x9))
#print(torch.cos(x9))

class Net(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()
        self.hidden1 = torch.nn.Linear(n_feature, n_hidden)   # hidden layer
        self.hidden2 = torch.nn.Linear(n_hidden, n_hidden)
        self.predict = torch.nn.Linear(n_hidden, n_output)   # output layer

    def forward(self, x):
        x = F.relu(self.hidden1(x))      # activation function for hidden layer
        x = F.relu(self.hidden2(x))
        x = self.predict(x)             # linear output
        return x

net = Net(n_feature=8, n_hidden=50,n_output=1)     # define the network
#print(net)  # net architecture

optimizer = torch.optim.SGD(net.parameters(), lr=0.0015)  #decrease the lenrning rate.
loss_func = torch.nn.MSELoss()  # this is for regression mean squared loss

for t in range(400):
    prediction = net(x)     # input x and predict based on x

    loss = loss_func(prediction, y)     # must be (1. nn output, 2. target)

    optimizer.zero_grad()   # clear gradients for next train
    loss.backward()         # backpropagation, compute gradients
    optimizer.step()        # apply gradients
 
print(net(torch.Tensor([1,1,0,0,0,0,0,0])))
print(loss)

#检验神经网络计算结果准确性
x_1=1
x_2=1
x_3=0
x_4=0
x_5=1
x_7=0
x_8=0
x_9=0
x_10=0
y_ = -math.cos(x_7)*(kd1*(-x_2)+kp1*(-x_1)-k1*x_8)/(x_5*math.cos(x_9))+2*math.sin(x_9)*x_8*x_10/math.cos(x_9)-g*math.sin(x_7)/(x_5*math.cos(x_9))
print(y_)
```

***使用visdom绘制loss曲线<sup>[6]</sup>***
&emsp;&emsp;为了实时生成拟合的loss曲线图，有必要使用visdom视图工具，安装和运行方式如下：
```
pip install visdom  #cmd安装

python -m visdom.server  #启动交互网页

http://localhost:8097/  #网页启动
```

&emsp;&emsp;可视化损失函数在代码中加入如下内容：
```python
from visdom import Visdom
import numpy as np

vis = Visdom(env='my_wind')#设置环境窗口的名称是'my_wind',如果不设置名称就在main中

for t in range(400):
    x_loss = torch.Tensor([t])
    
    prediction = net(x)     # input x and predict based on x

    loss = loss_func(prediction, y1)     # must be (1. nn output, 2. target)
    
    vis.line(X=x_loss,Y=loss.unsqueeze(0),win='polynomial',update='append' if t>0 else None)

    optimizer.zero_grad()   # clear gradients for next train
    loss.backward()         # backpropagation, compute gradients
    optimizer.step()        # apply gradients
```
&emsp;&emsp;其输出的loss曲线图如下所示：
<div align=center>![bp3](bp3.jpg)<div align=left>

### *0x03 引用文献*
[1]https://study.163.com/course/courseMain.htm?courseId=1004570029
[2]《神经网络的研究及应用》
[3]https://www.cnblogs.com/lliuye/p/9486500.html
[4]https://www.cnblogs.com/Belter/p/6653773.html？utm_source=itdadao&utm_medium=referral
[5]https://www.cnblogs.com/charlotte77/p/5629865.html
[6]http://www.rrcun.com/it/LXX516/article/details/79019328