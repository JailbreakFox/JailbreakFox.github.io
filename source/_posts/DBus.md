---
title: DBus
date: 2020-03-21 16:20:48
tags: Linux 工具
---

### *0x00 引言*
&emsp;&emsp;DBus是针对桌面环境优化的IPC(Interprocess Communication )机制，用于进程间的通信或进程与内核的通信。

<div align=center>
<img src="./DBus框架.png" width = "700" height = "400" />
<div align=left>  

### *0x01 DBus简介*
&emsp;&emsp;DBus是基于socket开发的机制，有低时延、低消耗等优点，提供了一对一的对等通讯；使用dbus-daemon作为后台进程时，可实现多对多通讯。
```
1 运行机制
2 重要ID
```
*1、运行机制*  
- DBus-daemon : 运行一个DBus-daemon就是创建了一条通信的总线Bus。总线分为 系统总线(system daemon)/会话总线(session daemon) 两类，例如Ubuntu系统开启时会自动拉起一个系统总线和会话总线。
- Connection : 当一个进程(Application)连接到Bus总线上面时，就产生了连接(Connection)。
- Application : 每个进程即为一个Application。DBus能实现进程间通信，且其实现是基于socket的，因此总有一个等待连接的Server APP，以及一个主动连接的Client APP。
- Object : 可理解为程序员希望用DBus实现的进程间通信类。
- Interface : 可理解为每个Object内的类成员。
- 通信方式 : D-bus里面支持的通信方式有signal/method两种。前者其实就是广播(UDP,一对多的通信方式);后者则是一问一答(TCP，一对一的通信),这种方式有点像远程调用，Client APP1调用Server APP2的method并传递参数给这个method，获取到这个method返回的结果。

*2、重要ID*  
&emsp;&emsp;在DBus具体实现中，经常会用到一些标志ID，用于寻找指定的进程或方法，具体内容可[参考教程](https://www.cnblogs.com/muxue/archive/2012/12/06/2806305.html)<sup>[1]</sup>。
- Address : 用于标识DBus-daemon。当一个DBus-daemon运行以后，其他的app该怎么连接到这个DBus-daemon，靠的就是address。格式如/com/polkit/qt/example/dbus。
- BusName : 用于标志Application。当一个进程连接上DBus-daemon，就需要注册一个BusName方便其他进程找到自己。格式如com.polkit.qt.example.dbus。
- Object Path : 用于标识Object类。当Client APP1的Object要跟Server APP2的Object通信时，就要告诉DBus-daemon目标的Object Path。格式如/com/polkit/qt/example/dbus。
- Interface name : 用于标志Object类成员。格式如com.polkit.qt.example.dbus。
- Member name : 用于标志通信类型信息。无特殊格式。

### *0x02 QDBus简介*
&emsp;&emsp;Qt有DBus的具体实现库，即QDBus。QDBus可参考QtLearning/QDbus里的实现代码，具体使用方式如下：
```sh
# 用命令qdbuscpp2xml生成dbus.h的xml文件
# dbus类为客户端用来调用服务端的接口
qdbuscpp2xml dbus.h -A -o com.polkit.qt.example.dbus.xml

# 用命令qdbusxml2cpp生成用于服务端的适配器dbus_adaptor.h/dbus_adaptor.cpp
qdbusxml2cpp com.polkit.qt.example.dbus.xml -i dbus.h -a dbus_adaptor

# 用命令qdbusxml2cpp生成用于客户端的接口dbus_interface.h/dbus_interface.cpp
qdbusxml2cpp com.polkit.qt.example.dbus.xml -p dbus_interface
```

### *0x03 DBus工具*
&emsp;&emsp;下面介绍一些用来生成DBus或查看DBus运行状态的工具。
```
1 QDBus文件生成工具
  1.1 qdbuscpp2xml
  1.2 qdbusxml2cpp
2 DBus状态分析工具
  2.1 D-feet
  2.2 dbus-send/dbus-monitor
  2.3 busctl
  2.4 qdbus --literal
```
*1、QDBus文件生成工具*  
&emsp;&emsp;如上一章所示，QDBus的进程间通信类实现需要先根据该类生成xml文件，再根据xml生成用于Server APP的adaptor以及用于Client APP的interface。  
*1.1、qdbuscpp2xml*  
&emsp;&emsp;qdbuscpp2xml会解析QObject派生类的C++头文件或是源文件，生成DBus的内省xml文件。qdbuscpp2xml会区分函数的输入输出，如果参数声明为const则会是输入，否则可能会被当作输出。
```sh
# qdbuscpp2xml使用语法如下：
qdbuscpp2xml [options...] [files...]
# Options参数如下：
# -p|-s|-m：只解析脚本化的属性、信号、方法(槽函数)
# -P|-S|-M：解析所有的属性、信号、方法(槽函数) 
# -a：输出所有的脚本化内容，等价于-psm 
# -A：输出所有的内容，等价于-PSM    
# -o filename：输出内容到filename文件
```
*1.2、qdbusxml2cpp*  
&emsp;&emsp;qdbusxml2cpp能根据上一节生成的xml文件生成用于Server APP的adaptor以及用于Client APP的interface。  
```sh
# 从XML文件生成继承自QDBusAbstractAdaptor的类
# 用命令qdbusxml2cpp生成用于服务端的适配器dbus_adaptor.h/dbus_adaptor.cpp
qdbusxml2cpp com.polkit.qt.example.dbus.xml -i dbus.h -a dbus_adaptor

# 从XML文件生成继承自QDBusAbstractInterface的类
# 用命令qdbusxml2cpp生成用于客户端的接口dbus_interface.h/dbus_interface.cpp
qdbusxml2cpp com.polkit.qt.example.dbus.xml -p dbus_interface
```

*2、DBus状态分析工具*  
&emsp;&emsp;DBus运行过程中，需要用调试工具观察运行状态，这里介绍两种工具，分别是D-feet以及dbus_send/dbus_monitor。  
*2.1、D-feet*  
&emsp;&emsp;D-feet是Red Hat公司研发的DBus调试工具。当你准备用DBus来写你的程序时，D-feet是非常用的，它可以显示service提供的所有对象、信号、和方法，另外还可以通过它实现方法调用。
```sh
# 安装D-feet
sudo apt-get install d-feet
# 运行
d-feet
```

<div align=center>
<img src="./D-feet.png" width = "700" height = "400" />
<div align=left>  

*2.2、dbus-send/dbus-monitor*  
&emsp;&emsp;有时在tty模式或无法打开图形界面的情况下，d-feet还无法满足我们的需求。  
**dbus-send**  
&emsp;&emsp;dbus-send是dbus提供的一个工具程序，用来向dbus维护的消息总线或会话总线发送消息。
```sh
# 使用方法
dbus-send [--system | --session] --type=[method_call | signal] --print-reply --dest=服务名 对象路径 接口名.方法名 参数类型:参数值 参数类型:参数值

# 举例1
dbus-send --system --type=method_call --print-reply --dest=org.bluez /org/bluez/audio org.bluez.audio.Manager.CreateDevice byte:0x01 byte:0x02
# 举例2-获取property值
# 这个关键在于读取属性调用的是org.freedesktop.DBus.Properties.GetAll
dbus-send --system --print-reply --dest=org.freedesktop.Accounts /org/freedesktop/Accounts/User1000 org.freedesktop.DBus.Properties.GetAll string:"org.freedesktop.Accounts.User"
```
- --system / --session  
将命令发向系统总线或会话总线  
- --type  
设置为信号signal，或者方法调用memthod_call
- --print-reply  
打印返回结果
- --dest  
服务名
- 对象路径  
/org/bluez/audio
- 接口名  
org.bluez.audio.Manager.CreateDevice
- 参数类型:参数值  
byte:0x01 byte:0x02

**dbus-monitor**  
&emsp;&emsp;dbus-monitor用于监听消息总线或会话总线发送的消息。
```sh
dbus-monitor --system "type='signal', sender='org.gnome.TypingMonitor', interface='org.gnome.TypingMonitor'"
```
- type  
设置为信号signal，或者方法调用memthod_call
- sender  
要监听的服务名
- interface  
要监听的对象路径

*2.3、busctl*  
&emsp;&emsp;busctl set-property能够用来设置dbus的参数

*2.4、qdbus --literal*  
&emsp;&emsp;可用该方法更改session的属性，比如修改背景图片: 
```sh
qdbus --literal com.deepin.wm /com/deepin/wm com.deepin.wm.ChangeCurrentWorkspaceBackground "图片地址"
```

### *0x04 GSettings配置*
```sh
# 配置文件路径
# /usr/share/glib-2.0/schemas/

# 列出所有schema
gsettings list-schemas

# 查找某个schema下的所有key
gsettings list-keys "org.gnome.settings-daemon.plugins.keyboard"

# 查看某个schema下某个key的值,假如要获取priority
gsettings get "org.gnome.settings-daemon.plugins.keyboard" priority

# 设置某个schema下某个key的值,假如要设置active
gsettings set "org.gnome.settings-daemon.plugins.keyboard" active false
```

### *0x05 引用文献*
[1]https://www.cnblogs.com/muxue/archive/2012/12/06/2806305.html
