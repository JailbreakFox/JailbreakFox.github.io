---
title: CMake
tags: 计算机技术，编译工具
date: 2019-04-29 20:41:00
grammar_cjkRuby: true
---

### *0x00 引言*
&emsp;&emsp; 一个完整的软件是由很多函数库组成的，那么编译程序或者可执行程序是如何知道该怎么调用和组织这些.cpp/.h/.so/.a等等后缀名的文件呢？通常我们会处在比较高层的位置，很多IDE软件都能帮我们自动完成这些任务，比如Windows平台上就会使用Visual Studio，在Linux平台上就会使用QT creator或者CLion等<sup>[1]</sup>。但再深一层次地说，编译时文件之间的组织关系都是由一个名叫makefile的文件来完成的，只不过IDE已经代替完成了这件复杂的任务，所以通常我们对该文件并不熟悉。
&emsp;&emsp; makefile定义了一系列的规则来指定，哪些文件需要先编译，哪些文件需要后编译，哪些文件需要重新编译，甚至于进行更复杂的功能操作。但是makefile语言本身比较抽象，让程序猿来手写是件非常费时费力的事情，于是CMake便应运而生了。CMake是比makefile抽象层次更高的项目管理工具，CMake能够通过命令转换成makefile文件，而所有一切软件设计人猿需要实现的编译任务均写在名为CMakeLists.txt文件内。
&emsp;&emsp; 本文将从两方面入手，来剖析和学习CMake。一个方向是从CMake的[官方文档](https://cmake.org/cmake-tutorial)<sup>[2]</sup>入手,当然也可以看[中文版文档](https://www.hahack.com/codes/cmake)<sup>[3]</sup>，推荐看中文版资料，详细且循序渐进，[代码](https://github.com/wzpan/cmake-demo)<sup>[4]</sup>可在git上找到，该方向不再赘述；第二个方向是从一些比较实际的编译目标入手。

### *0x01 CMake可移植程序编译*
&emsp;&emsp; 由于程序经常需要在不同电脑之间使用，但是每次都需要重新搭建环境非常繁琐，现在希望通过CMake编译，能够将可执行程序用到的三方库打包，那么在统一个ubuntu系统下即可即插即用。
```
1 基础知识
  1.1 静态库与动态库
  1.2 CMake基础编译方式
  1.3 Ubuntu搜索路径方式
  1.4 CMake RPATH简介
  1.5 可执行程序链接库批量处理
2 CMake编译可移植程序方案
  2.1 方案一：添加环境变量
  2.2 方案二：安装至默认lib文件夹
  *2.3 方案三：CMake添加RPATH
  2.4 方案四：CMake静态编译
```

***1、基础知识***  
***1.1、静态库与动态库***  
&emsp;&emsp; 现在的软件基本不可能全部是自己写的函数或类，我们经常需要使用别人的函数或类，那么就有必要得到那些软件的三方库，而库又分为静态库和动态库，在Windows下分别为.lib/.dll后缀文件，在Linux下分别为.a/.so文件。所谓静态库就是编译时和源代码一起被打包入可执行程序的库，而动态库是一些可重复使用的模块，他们的具体区别可参考[教程](https://www.runoob.com/w3cnote/cpp-static-library-and-dynamic-library.html)<sup>[5]</sup>。

***1.2、CMake基础编译方式***  
&emsp;&emsp;看过基本的中文教程demo1可知，CMake实际上都在CmakeList.txt文件内描述完成，一旦写完，只需在顶层的CmakeList.txt文件目录下执行以下语句：
```cmd
#做配置
./configure
#新建build目录，用来储存编译结果，否则会很乱
mkdir build
#进入build目录
cd build
#开始生成makefile
cmake ..
#使用makefile编译程序
make
#安装程序，即在目标位置生成可执行程序以及对库文件做操作等
make install
```
***1.3、Ubuntu搜索路径方式***  
&emsp;&emsp;编译之后的可执行程序在其他电脑上无法运行，实质上最关键的问题就在于新的操作系统环境下，程序不知道去什么地方寻找依赖库。Ubuntu系统默认的[.so库搜索方式](https://blog.csdn.net/qq_16097611/article/details/53484724)<sup>[6]</sup>根据优先级依次为:1)-L;2)/usr/lib;3)/lib;4)LIBRARY_PATH。  
&emsp;&emsp;第二三种方法，系统只会该目录下的文件，而不会遍历文件夹，若要识别文件夹下的文件，还需要修改/etc/ld.so.conf，并调用ldconfig命令，这里不再深究。  
&emsp;&emsp;主要讲的是最后一种方法，修改LIBRARY_PATH，其实就是我们熟知的[修改环境变量](https://www.cnblogs.com/trying/archive/2013/06/07/3123577.html)<sup>[7]</sup>，所以ROS也是这样，要执行rospack find就需要添加环境变量（该文件实质上是命令行每次开启时执行的一段命令，所以这样修改环境变量来运行程序的方法必须是使用./程序，双击的话就无法运行，除非新建一个快捷方式并指定优先运行一段export），那么可以采用：
```cmd
#向/.bashrc中填入搜索路径
echo "export LD_LIBRARY_PATH=目标路径" >>~/.bashrc
```
***1.4、CMake RPATH简介***  
&emsp;&emsp;实际上，CMake在编译和安装后生成的可执行程序头部都会有一个[RPATH参数](https://www.cnblogs.com/rickyk/p/3884257.html)<sup>[8]</sup>，其用来表示搜索库的路径。操作系统本身搜索库路径的方式有环境变量和默认路径，但RPATH能跟随程序本身，所以不受程序所在环境的制约。

***1.5、可执行程序链接库批量处理***  
&emsp;&emsp;make步骤之后生成的中间可执行程序，在Ubuntu下可通过指令ldd拿到所有用到的链接库，可通过制作.sh脚本的方式将链接库文件批量导入目标文件夹中，具体步骤如下：
```cmd
#1、在build文件夹下新建脚本test.sh
#2、在test.sh中添加语句
chk_lock_test=$( ldd $1 | awk '{if (match($3,"/")){ print $3}}' )
cp -L -n $chk_lock_test $2
#3、给脚本一个权限，使其可移动所有文件
sudo chmod 777 test.sh
#4、脚本目录下执行命令，
 ./test.sh 可执行程序目录 目标目录
```

***2、CMake编译可移植程序方案***  
***2.1、方案一：添加环境变量***  
&emsp;&emsp;具体思路为:1)可执行程序链接库批量处理至CmakeList.txt根目录下;2)CMake将批量处理得到的动态链接库install至目标文件夹下;3)在目标机器的~/.bashrc文件中添加第二步链接库install所在路径;  
&emsp;&emsp;思路其实非常简单，但是关键的难点在于链接库取得的技巧，这里有必要叙述一下。第一点为取得可执行程序的所有动态链接库，第二点为分析取得所有未被ldd出来的动态链接库。  
&emsp;&emsp;难点一已经在1.5节中指出，难点二这里以取得Qt所有动态链接库为例展开讨论。实现上述三个步骤以后，我们修改LIBRARY_PATH参数，在可执行程序根目录下输入命令行：
```cmd
echo "export LD_LIBRARY_PATH=目标路径" >>~/.bashrc
#cd到可执行程序根目录下，运行程序
./程序名称
```
&emsp;&emsp;发现程序报错，错误内容如下：
```cmd
This application failed to start because it could not find or load the Qt platform plugin "xcb"
```
&emsp;&emsp;根据上述提示可知，缺少了名为xcb的一个链接库，[查阅资料](https://blog.csdn.net/u010168781/article/details/82150105)<sup>[9]</sup>可知我们需要在可执行目录下新建platforms文件夹，并添加libqxcb.so文件（该文件在qt的/Qt5.7.1/5.7/gcc_64/lib目录下，包括qt所有的链接库都在这个文件夹下面。*如何修改该libqxcb.so链接库位置仍未知*）。继续执行可执行程序，发现报出同样错误，为了找到错误原因，这里[引入一个技巧](https://blog.csdn.net/sinat_26106275/article/details/82778951)<sup>[10]</sup>，即设置命令行的环境变量参数QT_DEBUG_PLUGINS，并修改/.bashrc文件，使其在命令行开启前执行：
```cmd
echo "export QT_DEBUG_PLUGINS=1" >>~/.bashrc
```
&emsp;&emsp;再次运行可执行程序，报错出现具体的错误原因：
```cmd
    Found metadata in lib /home/cobot/PathImporter/build/platforms/libqxcb.so, metadata={
        "IID": "org.qt-project.Qt.QPA.QPlatformIntegrationFactoryInterface.5.3",
        "MetaData": {
            "Keys": [
                "xcb"
            ]
        },
        "className": "QXcbIntegrationPlugin",
        "debug": false,
        "version": 329473
    }
    Got keys from plugin meta data ("xcb")
    Cannot load library /home/cobot/PathImporter/build/platforms/libqxcb.so:(libQt5XcbQpa.so.5: 无法打开共享对象文件: 没有那个文件或目录)
```
&emsp;&emsp;可见文件夹里实质上还缺少一个名为libQt5XcbQpa.so.5的动态链接库，那么我们只需从qt的lib下找到该库并放入我们的目标文件夹下。再次运行程序并报错：
```cmd
Cannot mix incompatible Qt library (version 0x50201) with this library (version 0x50701)
```
&emsp;&emsp;大意是Qt版本5.2.1与5.7.1的链接库不匹配，无法融合。可知实际上我的系统里存在多版本的Qt，Qt实质上会在默认库路径/usr/lib下生成一些必要的库，这也是报错的原因。这里有一个解决的技巧，即将所有lib文件全部放入目标文件夹，并执行程序，最后发现程序正常运行，可见库中必然还存在一个特定的动态链接库，使用二分法，多次将不同文件放入目标文件夹运行，迭代排查后发现缺少链接库libQt5DBus.so.5链接库，将其放入目标文件夹，运行正常（这个方法很牛逼，我都佩服我自己，全网基本上没有资料说这个文件的）。  
&emsp;&emsp;这里还有两个细节，第一点libQt5DBus.so.5是一个类似于快捷方式的文件，它会链接到libQt5DBus.so.5.7.1上（库里还有一个libQt5DBus.so.5.7，暂时不知道何用），所以最后只需要取出libQt5DBus.so.5.7.1并重命名为libQt5DBus.so.5即可，链接库libQt5XcbQpa.so.5同理。第二点，有必要猜测下这三个链接库存在的意义，libqxcb.so应该是qt的入口库，然后libQt5XcbQpa.so.5是实际运行的函数，并且链接到了5.7.1的子版本上（方便版本控制），而这里的libQt5DBus.so.5应该是做Qt不同版本之间的一个解释器。

***2.2、方案二：安装至默认lib文件夹***  
&emsp;&emsp;方案一虽然可以顺利运行，但是每次要修改环境变量实际上是非常麻烦的事情，且并不是所有软件使用者都有这个觉悟，那么我们要考虑更加便捷的方法，即将库文件用CMake install至系统默认搜索的库，即在1.3节中已经叙述过的/usr/lib与/lib位置。在1.3节也讲过了，如果将所有库文件放入lib文件夹下的子文件夹内，则系统仍搜索不到链接库（如果要采取修改/etc/ld.so.conf以及添加ldconfig命令，则还不如方案一便捷）。唯一的办法就是将所有库文件全部install至lib文件夹下，运行程序完美报错：
```cmd
    ./PathImporter: /usr/lib/x86_64-linux-gnu/libQt5Gui.so.5: no version information available (required by ./PathImporter)
    ./PathImporter: /usr/lib/x86_64-linux-gnu/libQt5Core.so.5: no version information available (required by ./PathImporter)
    ./PathImporter: /usr/lib/x86_64-linux-gnu/libQt5Core.so.5: no version information available (required by ./PathImporter)
    ./PathImporter: /usr/lib/x86_64-linux-gnu/libQt5Widgets.so.5: no version information available (required by ./PathImporter)
    ./PathImporter: /usr/lib/x86_64-linux-gnu/libQt5Core.so.5: no version information available (required by /usr/lib/libvtkGUISupportQt-8.2.so.1)
    ./PathImporter: /usr/lib/x86_64-linux-gnu/libQt5Core.so.5: no version information available (required by /usr/lib/libvtkGUISupportQt-8.2.so.1)
    ./PathImporter: /usr/lib/x86_64-linux-gnu/libQt5Gui.so.5: no version information available (required by /usr/lib/libvtkGUISupportQt-8.2.so.1)
    ./PathImporter: /usr/lib/x86_64-linux-gnu/libQt5Widgets.so.5: no version information available (required by /usr/lib/libvtkGUISupportQt-8.2.so.1)
    ./PathImporter: /usr/lib/x86_64-linux-gnu/libQt5Gui.so.5: no version information available (required by /usr/lib/libQt5X11Extras.so.5)
    ./PathImporter: /usr/lib/x86_64-linux-gnu/libQt5Core.so.5: no version information available (required by /usr/lib/libQt5X11Extras.so.5)
    ./PathImporter: /usr/lib/x86_64-linux-gnu/libQt5Core.so.5: no version information available (required by /usr/lib/libQt5X11Extras.so.5)
    ./PathImporter: relocation error: /usr/lib/libQt5X11Extras.so.5: symbol qt_version_tag, version Qt_5.7 not defined in file libQt5Core.so.5 with link time reference
```
&emsp;&emsp;未知错误（应该是多版本Qt的原因，还害得我修改了lib库所有文件权限，导致sudo用不了、系统时间出错、U盘都不出等一系列尿频尿急症状T_T）等待填坑。

****2.3、方案三：CMake添加RPATH***  
&emsp;&emsp;在1.4节中已经叙述过CMake RPATH的用途，该方案可以说是最便捷和人性化的了，第一不用修改环境变量，第二在make与make install的过程中就能决定中间执行程序与安装执行程序的库链接路径。  
&emsp;&emsp;根据1.4节中提到的[博客](https://www.cnblogs.com/rickyk/p/3884257.html)<sup>[8]</sup>，我们只需要在CmakeList.txt的install部分添加如下指令：
```cmd
#方法一：在CMakeLists.txt文件中修改
#修改安装执行程序的库链接路径
set(CMAKE_INSTALL_RPATH 目标路径)
#保证只针对当前的target进行make install的时候RPATH的写入了
set_target_properties(程序名 PROPERTIES INSTALL_RPATH CMAKE_INSTALL_RPATH)

#方法二：在编译时修改
#这里将install路径设置为build
cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=../build/ ..
```
&emsp;&emsp;这里依旧分享两个小技巧
```sh
# 使用指令readelf可以查看某一可执行程序的RPATH
readelf -d '程序路径'

# 使用ldd可查看某一可执行程序的链接库
ldd '程序路径'
```
***2.4、方案四：CMake静态编译***  
&emsp;&emsp;除了上述三种调控动态链接库位置与链接的方式之外，我们还可以用CMake实现静态编译，即将三方库的动态链接库或者静态链接库加上自己的程序编译在一起，得到不需要外接库的可执行程序，在1.1节之中已经分析过了这种程序的优缺点（小型项目还好，一旦做大型项目，不但编译慢而且运行的电脑也会被大量占用空间）。目前该方式只在网上搜索到设置CMake设置静态编译的一段命令：
```cmd
set(CMAKE_CXX_FLAGS "-static ${CMAKE_CXX_FLAGS}")
```
&emsp;&emsp;该方法等待填坑（不了解意思，执行之后也会报错）。

### *0x02 链接库选择路径*
&emsp;&emsp;由于链接库路径选择的重要性，这一章节着重分析一下Linux链接库选择路径顺序及其修改方式。
```
1 Linux动态库选择顺序
2 Linux如何添加链接库搜索路径
3 如何修改Qt链接库路径
4 CMake链接库三要素*
```
***1、Linux 动态库选择顺序***  
```sh
# gcc 编译程序时查找SO顺序
    1.gcc 编译时参数-L指定的路径
    2.环境变量 LIBRARY_PATH LD_LIBRARY_PATH
    3.系统默认库位置 /lib    /usr/lib
# Linux 程序运行时查找SO顺序
    1.gcc 编译时指定的运行时库路径 -Wl,-rpath
    2.环境变量 LD_LIBRARY_PATH
    3.ldconfig 缓存 /etc/ld.so.cache
    4.系统默认库位置 /lib    /usr/lib
# 包含目录顺序
    1.-I 指定的路径
    2./usr/include
    3./usr/local/include
```

***2、Linux如何添加链接库搜索路径***
```sh
# ===== 方案一 =====
# 首先找到.so或.a文件所在路径
# 比如/home/uos/Desktop/test.so

# 修改搜索路径，在如下文件中添加链接库所在路径
sudo vim /etc/ld.so.conf
# 添加/home/uos/Desktop/
# 或者在/etc/ld.so.conf.d/文件夹下新建.conf文件

# 使修改生效
sudo /sbin/ldconfig

# ===== 方案二 =====
# LD_LIBRARY_PATH是Linux环境变量名
# 主要用于指定查找链接库时除默认路径外的其他路径
export LD_LIBRARY_PATH=/home/uos/Desktop/

# ===== 方案三 =====
# 在CMakeLists.txt文件中添加rpath的搜索路径
FIND_LIBRARY(MY_LIB NAMES libMathFunctions.so PATHS /home/uos/Desktop)
TARGET_LINK_LIBRARYS(${CMAKE_PROJECT_NAME} ${MY_LIB})
```

***3、如何修改Qt链接库路径***  
&emsp;&emsp;为了少踩编译中或编译后的坑，请注意以下事项:  
```sh
1.编译Qt、DTK 的生产目录，一定不要设置在 /usr 目录，这样非常容易桌面系统崩溃
2.在编译其他应用时。请设置以下环境变量来确保程序加载的库不是系统自带的库(如果需要指定多个路径，请使用英文的:隔开)
    1.export LD_LIBRARY_PATH=qtbuilddir/lib:dtkbuilddir/lib   说明： 设置程序运行是链接库的路径
    2.export QT_QPA_PLATFORM_PLUGIN_PATH=qtbuilddir/plugins/platforms 说明： 平台相关插件
    3.export QT_PLUGIN_PATH=qtbuilddir/plugins    说明： Qt插件
    4.export PKG_CONFIG_PATH=qtbuilddir/lib/pkgconfig:dtkbuilddir/lib/pkgconfig说明：我们在Qt pro 中配置的 phgconfig 就是用过查找该目录下的.PC文件 实现头文件和库的引入
3.设置上述环境变量的方式有多种。各有优点，如下： 我们建议通过终端的方式设置环境变量，然后在该终端上启动Qt，不会影响系统。
    1.通过脚本的方式在终端设置环境变量。
        生效时间：立即生效  有效期：仅仅在该终端生效，关闭终端无效 生效范围：仅对当前用户有效
        优点：不影响系统。
        缺点：需要从该终端启动 qtcreator   修改变量需要关闭qtcreator
    2.在Qt 项目的构建环境中设置  
        生效时间：立即生效  有效期：该项目  生效范围：该项目
        优点：随时修改
        缺点：项目多的时候每个项目都要设置一遍
    3.通过修改用户目录下的<code>~/.bashrc</code>文件进行配置 
        生效时间：下次打开终端  有效期：永久  生效范围：仅对当前用户有效
        缺点：可能导致系统崩溃
    4.修改系统配置，需要管理员权限（如root） 不建议！
4.在情况出乎您的意料的时候，请检查加载的库路径是否正确，检查方法如下
    1.QtCreator 调试模式下菜单栏  控件 -> 视图 -> DebugLoger 该对话框输出了加载库的详细信息
    2.使用ldd + 程序名（库名） 可以看到依赖库
```

***4*、CMake链接库三要素***
- .so / .o 文件
- 库头文件
- 环境变量

### *0x03 CMake常用变量*
```sh
SET(CMAKE_CXX_STANDARD 11)
SET(CMAKE_INCLUDE_CURRENT_DIR ON)
# 设置自动生成moc文件,AUTOMOC打开可以省去QT5_WRAP_CPP命令
SET(CMAKE_AUTOMOC ON)
# 设置自动生成ui.h文件,AUTOUIC打开可以省去QT5_WRAP_UI命令
SET(CMAKE_AUTOUIC ON)
# 设置c++编译属性  https://blog.csdn.net/rheostat/article/details/19811407
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}  -g -Wall -pthread -Wl,--as-need -fPIE -Wl,-E")
SET(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS} -O0 -ggdb")
SET(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS} -O3")
# 设置CMake模块寻找路径  CMAKE_SOURCE_DIR代表该CMakeLists.txt文件路径
SET(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake/modules)

# 龙芯系统
IF (${CMAKE_SYSTEM_PROCESSOR} MATCHES "mips64")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -ftree-vectorize -march=loongson3a -mhard-float -mno-micromips -mno-mips16 -flax-vector-conversions -mloongson-ext2 -mloongson-mmi")
ENDIF()

# 如果不是Debug模式.
# EXECUTE_PROCESS(COMMAND <一句shell命令> WORKING_DIRECTORY <这句shell命令执行的工作目录>)
IF (NOT (${CMAKE_BUILD_TYPE} MATCHES "Debug"))
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Ofast")

    # generate qm
    EXECUTE_PROCESS(COMMAND bash "translate_generation.sh"
                    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR})
ENDIF ()

# 设置编译类型
SET(CMAKE_BUILD_TYPE "Release")
SET(CMAKE_BUILD_TYPE "Debug")
SET(CMAKE_BUILD_TYPE "RelWithDebInfo")
```

### *0x04 CMake学习中获得优质且繁杂的资源*
&emsp;&emsp;[CMake中调用Qt模块](https://www.jianshu.com/p/7eeb6f79a275)<sup>[11]</sup>  
&emsp;&emsp;[CMake中add_library include_library以及target_link_libraries区别](https://blog.csdn.net/bigdog_1027/article/details/79113342)<sup>[12]</sup>  
&emsp;&emsp;[CMake构建动态、静态库](https://www.cnblogs.com/zhoug2020/p/5904206.html)<sup>[13]</sup>  
&emsp;&emsp;[CMake的一些变量](https://cmake.org/cmake/help/v3.0/manual/cmake-variables.7.html)<sup>[14]</sup>  
&emsp;&emsp;[CMake跨平台编译以及静态编译](https://zilongshanren.com/blog/2014-08-31-how-to-use-cmake-to-compile-static-library.html)<sup>[15]</sup>

### *0x05 引用文献*
[1]https://blog.csdn.net/caowei880123/article/details/52497550
[2]https://cmake.org/cmake-tutorial
[3]https://www.hahack.com/codes/cmake
[4]https://github.com/wzpan/cmake-demo
[5]https://www.runoob.com/w3cnote/cpp-static-library-and-dynamic-library.html
[6]https://blog.csdn.net/qq_16097611/article/details/53484724
[7]https://www.cnblogs.com/trying/archive/2013/06/07/3123577.html
[8]https://www.cnblogs.com/rickyk/p/3884257.html
[9]https://blog.csdn.net/u010168781/article/details/82150105
[10]https://blog.csdn.net/sinat_26106275/article/details/82778951
[11]https://www.jianshu.com/p/7eeb6f79a275
[12]https://blog.csdn.net/bigdog_1027/article/details/79113342
[13]https://www.cnblogs.com/zhoug2020/p/5904206.html
[14]https://cmake.org/cmake/help/v3.0/manual/cmake-variables.7.html
[15]https://zilongshanren.com/blog/2014-08-31-how-to-use-cmake-to-compile-static-library.html
