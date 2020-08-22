---
title: 远程系统工具-SSH与VNC
date: 2019-05-08 10:26:00
tags: 远程桌面， 工具
---
### *0x00 引言*
&emsp;&emsp;SSH(Secure Shell)又称为安全外壳协议，是目前较可靠且专为*远程登录会话*和其他*网络服务*提供安全性的协议，由于其加密而实现的安全特性，已经开始代替telnet、ftp、rlogin、rsh和rcp等传统协议。SSH主要被用来实现远程命令行控制，但是也有远程桌面的功能，然而在可视化方面没有VNC应用广泛。
&emsp;&emsp;VNC(Virtual Network Console)又称为虚拟网络控制台，它是一款基于UNIX和Linux操作系统的免费的开源软件。

### *0x01 SSH协议工具OpenSSH*
&emsp;&emsp;OpenSSH是SSH协议的免费开源实现，这里介绍一下其在Ubuntu系统下的安装、使用以及一些实用技巧。
```
1 安装与使用
2 SSH可视化
3 root方式登录
4 免密远程登陆
5 免密远程拷贝
6 远程拷贝
```

***1、安装与使用***
&emsp;&emsp;Ubuntu默认安装SSH的client端但没有安装server端，因此输入以下命令进行安装：
```cmd
sudo apt-get install openssh-server
#或者直接全部安装，毕竟也不大
sudo apt-get install openssh
```
&emsp;&emsp;这边注意一点，新安装的OpenSSH默认是不能用root访问的，需要[修改配置文件](https://blog.csdn.net/xiao_yuanjl/article/details/79147314)<sup>[1]</sup>，这里就不详细解释了（*留坑*）。
&emsp;&emsp;安装完成后便可以直接连接目标机器：
```cmd
ssh (账户名)@(目标IP)
#举栗子
ssh MyComp@192.168.112.130
```
&emsp;&emsp;然后根据需要填入该账号的密码即可登陆。

***2、SSH可视化***
***3、root方式登录***
***4、免密远程登陆***
***5、免密远程拷贝***  

***6、远程拷贝***  
&emsp;&emsp;使用工具scp能够远程拷贝文件
```sh
# 在终端环境下运行
# scp "远程机用户名"@"远程机IP":"拷贝文件路径" "目标路径"
scp root@www.runoob.com:/home/root/others/music /home/space/music/1.mp3  
```

### *0x02 VNC*
&emsp;&emsp;VNC包括以下四个命令：vncserver，vncviewer，vncpasswd，和vncconnect，大多数情况下用户只需要其中的两个命令：*vncserver*和*vncviewer*。另外，和SSH一样，实际上有很多软件都能实现VNC，包括vncserver和vncviewer都有各自的实现软件，关键之处就在于选对安装包，避免踩到多余的坑。
```
1 安装与使用
  1.1 Windows平台-RealVNCserver
  1.2 Ubuntu-RealVNCserver
  1.3 Ubuntu-vnc4server
    1.3.1 vnc4server安装与配置
    1.3.2 vnc4server使用
    1.3.3 vnc4server自启动
  1.4 Ubuntu-x11vnc
```

***1、安装与使用***
***1.1、Windows平台-RealVNCserver***
&emsp;&emsp;在Windows平台下，使用[RealVNC官网](https://www.realvnc.com/en)<sup>[2]</sup>的VNCserver和VNCviewer即可，其安装教程可参考[百度经验](https://jingyan.baidu.com/article/d2b1d102b85a825c7e37d405.html)<sup>[3]</sup>。唯一与教程不同的地方是，server和viewer都需要登陆注册的邮箱，实际上和teamviewer差不多了。

***1.2、Ubuntu-RealVNCserver***
&emsp;&emsp;RealVNCviewer是目前用过的VNCvierver软件里最好用的，因此这里的所有教程均使用RealVNCviewer。而server端则有多种选择，这里使用RealVNCserver。
&emsp;&emsp;发现RealVNCserver在Ubuntu里的安装不需要登陆邮箱，可以直接输入Lisence，而且RealVNCviewer也不需要和服务端登陆一个邮箱（可能是该公司对于Linux版本还做的不是很完善），这里写一下安装过程。
```cmd
#从RealVNC官网下载Linux版本的RealVNCserver，在安装目录下打开终端并安装deb包
sudo dpkg -i 包名称
#安装好之后，还需要继续输入命令vnclicense –add vnc的秘钥，密钥可去网上找
sudo vnclicense -add WHJRK-UXY7V-Q34M9-CZU8L-8KGFA
```
&emsp;&emsp;至此安装完成，然后需要对服务端的电脑做一些[配置](http://www.cnblogs.com/xuliangxing/p/7642650.html)<sup>[4]</sup>，可根据上述链接做配置。另外，注意客户端连接时在服务端会弹出允许远程桌面的窗口，点击允许才能继续。
&emsp;&emsp;虽然这种方法安装简单，但是存在很多问题:1)客户端的界面和服务端的界面是共用的，类似于QQ的远程桌面;2)配置过程麻烦，且登陆的时候在服务端还需要点允许;3)存在卡顿问题，即在客户端看视频的时候帧数很低;4)[卸载方法](https://askubuntu.com/questions/653321/how-to-uninstall-real-vnc-in-ubuntu-14-04)<sup>[5]</sup>很繁杂。

***1.3、Ubuntu-vnc4server***
***1.3.1 vnc4server安装与配置***
&emsp;&emsp;相比于1.2节的服务端，现在要介绍一种优点更多的方法，即直接用apt-get的方式来安装。其安装过程可[查阅教程](https://blog.csdn.net/linuxshine/article/details/79972786)<sup>[6]</sup>，由于这种方式的重要性，这里也重复叙述一遍安装过程。
```cmd
#apt-get方式安装vncserver
sudo apt-get install vnc4server
#安装gnome（linux的一种图形桌面环境）
sudo apt-get install gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal
#为当前用户创建密码（也可以不创建，在之后开启server的时候会询问）
vncpasswd
```
&emsp;&emsp;至此，安装完成，开始修改配置，所有的配置文件均在~/.vnc隐藏文件夹下（需要先运行vncserver一次才会生成，*如果实在不知道怎么建，就现在命令行执行vncserver*），但是我们不使用非流程化的操作，还是自己去创建该文件夹，在~/.vnc目录下新建xstartup文件（配置文件），其内容如下（这里有两个方案，第一种是亲自试验过可以的，第二种跑起来很卡）：
```
#=========方案一==========
#!/bin/sh  
  
export XKL_XMODMAP_DISABLE=1  
unset SESSION_MANAGER  
unset DBUS_SESSION_BUS_ADDRESS  
  
[ -x /etc/vnc/xstartup ] && exec /etc/vnc/xstartup  
[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources  
xsetroot -solid grey  
vncconfig -iconic &  
  
gnome-panel &  
gnome-settings-daemon &  
metacity &  
nautilus &  
gnome-terminal & 

#=========方案二==========
#!/bin/sh  
export XKL_XMODMAP_DISABLE=1  
unset SESSION_MANAGER  
unset DBUS_SESSION_BUS_ADDRESS  

gnome-panel &  
gnmoe-settings-daemon &  
metacity &  
nautilus &  
gnome-terminal &  
vncconfig &  
startlxde &  
/usr/bin/ibus-daemon -d &
```
&emsp;&emsp;最后一步，添加配置文件的可执行权限：
```cmd
#为xstartup文件添加可执行权限
chmod +x ~/.vnc/xstartup
```

***1.3.2 vnc4server使用***
(1)开启服务端
&emsp;&emsp;在终端下直接运行下述命令，~/.vnc目录下会出现.log和.pid两个文件。
```
#直接生成pid为1的远程桌面端口
vncserver :1
#新增一个远程桌面端口，pid累加
vncserver
#如果需要指定客户端的屏幕大小，可以使用-geometry参数指定，使用方式为（例如指定屏幕大小为1920*1080）：
vncserver -geometry 1920x1080 :1  
```
(2)客户端访问
&emsp;&emsp;客户端访问实际上除了RealVNCviewer，还有其他的方式比如xvnc4viewer，只不过前者是界面比较友好的GUI软件，而后者是命令行形式（其实后者是和vnc4server配对，前者和RealVNCviewer配对）。
```
#=========使用RealVNCviewer==========
#这种方法和1.1节以及1.2节一致，只不过不需要登陆邮箱，直接输入IP:1
192.168.112.130:1
#=========使用xvnc4viewer==========
#如果客户端是ubuntu系统，可以使用xvnc4viewer软件，但是这种是命令行模式的，先安装
sudo apt-get install xvnc4viewer
#启动vncviewer软件，连接服务端
vncviewer IP:1  
```
(3)关闭服务端
vncserver -kill :1 

***1.3.3、vnc4server自启动***  
&emsp;&emsp;首先确保vnc server已经装好，在/etc文件夹下，新建vncserver文件夹，在vncserver文件夹下新增两个文件startvnc.py和startvnc.sh。
(1)startvnc.py
```py
import sys  
import os  
user=["k40","wcg","szh","zf","yry","lxy","llp"] #不同账户的用户名，port按这个顺序依次是1到7，如：k40即port 1  
i = 1  
depth = "16"  
geometry = "1024x900"  #分辨率  
name = "vncserver"  
for name in user:  
    options = "-name %s -depth %s -geometry %s :%d" % (name, depth, geometry, i)  
    print(options)  
    i = i + 1  
    cmd = "su %s -c '/usr/bin/vncserver %s'" % (name, options)  
    print(cmd)  
    os.system(cmd)
```
(2)startvnc.sh:
```py
#!/bin/bash  
python /etc/vncserver/startvnc.py  
exit 0 
```
&emsp;&emsp;运行.sh，然后重启电脑。

***1.4、Ubuntu-x11vnc***
&emsp;&emsp;vnc4server确实能用，且特点是宿主机界面不跟随客户机(可以黑？)，但是配置真的很烦。还有一种方法和1.2节中的Ubuntu-RealVNCserver效果一样，但是帧率似乎高了一些，并且我自己也写了一个[脚本](https://github.com/JailbreakFox/Ubuntu14.04-LTS-sh/blob/master/Ubuntu14.04配置sh包/x11vnc.sh)<sup>[7]</sup>，直接运行即可且是开机自启动，但是注意:1)运行过程中需要输入希望配置的密码;2)运行结束会reboot。

### *0x03 TeamViewer*
```
1 Ubuntu平台
  1.1 安装TeamViewer
  1.2 设置开机自启动以及登录密码
  1.3 设置局域网联接
```
***1.1、安装TeamViewer***  
&emsp;&emsp;根据[教程介绍](https://blog.csdn.net/qq_38451119/article/details/81369043)<sup>[8]</sup>，去[teamviewer官网](https://www.teamviewer.com/zhcn/download/linux/)<sup>[9]</sup>下载最新版的teamviewer for linux。  
```py
#安装deb包  
sudo dpkg -i teamviewer_13.1.8286_amd64.deb
#安装失败，修复依赖关系  
sudo apt-get install -f  
#重新安装deb包  
sudo dpkg -i teamviewer_13.1.8286_amd64.deb  
```
***1.2、设置开机自启动以及登录密码***  
&emsp;&emsp;根据[教程介绍](https://blog.csdn.net/box172506/article/details/88016732)<sup>[10]</sup>。
```py
#停止teamviewer  
teamviewer –daemon stop  
#给conf文件添加权限  
sudo chmod 777 /opt/teamviewer/config/global.conf  
#打开conf文件  
gedit /opt/teamviewer/config/global.conf
#在conf文件最后添加一段命令  
EulaAccepted = 1  
EulaAcceptedRevision = 6  
#打开teamviewer  
teamviewer –daemon start  
#修改teamviewer登录密码  
sudo teamviewer –passwd 123456
#记录teamviewer ID，方便登录的时候输入  
teamviewer –info print id
#设置开机启动(不操作到这一步，配置重启后就会消失)  
sudo systemctl enable teamviewerd.service  
#(如果想不开启开机自启动)  
sudo systemctl disable teamviewerd.service
```
***1.3、设置局域网联接***  
&emsp;&emsp;根据[教程介绍](https://blog.csdn.net/moshiyaofei/article/details/86431188)<sup>[11]</sup>。
```py
#option->常规->网络设置->呼入的LAN连接->选择accept
```

### *0x04 引用文献*
[1]https://blog.csdn.net/xiao_yuanjl/article/details/79147314  
[2]https://www.realvnc.com/en  
[3]https://jingyan.baidu.com/article/d2b1d102b85a825c7e37d405.html  
[4]http://www.cnblogs.com/xuliangxing/p/7642650.html  
[5]https://askubuntu.com/questions/653321/how-to-uninstall-real-vnc-in-ubuntu-14-04  
[6]https://blog.csdn.net/linuxshine/article/details/79972786  
[7]https://github.com/JailbreakFox/Ubuntu14.04-LTS-sh/blob/master/Ubuntu14.04配置sh包/x11vnc.sh  
[8]https://blog.csdn.net/qq_38451119/article/details/81369043  
[9]https://www.teamviewer.com/zhcn/download/linux/  
[10]https://blog.csdn.net/box172506/article/details/88016732  
[11]https://blog.csdn.net/moshiyaofei/article/details/86431188  