---
title: deb与rpm打包
tags: 计算机技术，打包工具
date: 2021-06-24 10:17:29
grammar_cjkRuby: true
---

### *0x00 引言*
&emsp;&emsp; Debian下的安装包后缀名.deb，Unix服务器的安装包后缀名一般为.rpm 。本文主要研究如何打这两种包。

### *0x01 rpm打包*
&emsp;&emsp;rpm打包默认是以源码打包的形式，当然也可以利用这种机制实现非源码打包。
```
1 环境搭建
2 基础知识构建
  2.1 rpm打包文件结构
  2.2 rpm目录路径宏
  2.3 rpm常用路径宏
3 源码打包方法
4 非源码打包方法
```

***1、环境搭建***  
&emsp;&emsp; 这里以centos7为rpm打包平台，具体的环境配置已经在仓库里面，可以自行[查阅资料](https://github.com/JailbreakFox/Linux-sh-package/blob/master/Centos/Centos%20Mini.md)<sup>[1]</sup>。  

***2、基础知识构建***  
***2.1、rpm打包文件结构***  
&emsp;&emsp; rpmdev-setuptree命令由工具rpmdevtools提供，可以直接在/root/rpmbuild/目录下生成rpm打包所需的目录结构。下面具体描述各个文件夹的作用:  
```sh
$ tree /root/rpmbuild
rpmbuild
├── SOURCES    # 源码路径
├── BUILD      # 源码编译路径
├── SPECS      # rpm生成规则存放路径
├── RPMS       # rpm包生成路径
└── SRPMS      # rpm源码包生成路径
```
- SOURCES - 如果是用源码打包，则只需要将源码的tar.gz文件存放于此即可;
- BUILD - rpmbuild工具会自行将SOURCES目录中的源码在此处解压，该文件无需手动修改，具体编译方法需要在SPECS下的.spec文件中描述;
- SPECS - 需要人工操作的只有该文件夹，里面可以存放各种rpm打包规则的.spec文件，后面详细介绍;
- RPMS - 当打包完成，会在此处生成release与debug版的.rpm包;
- SRPMS - 当打包完成，会在此处生成源码.rpm包;
- *BUILDROOT - 该目录是在SPECS打包过程中自动生成的，其重要性是最后打完的包需要安装的文件及其路径都以该目录为模板。  

***2.2、rpm目录路径宏***  
&emsp;&emsp; 各路径宏参考[文献](https://blog.csdn.net/get_set/article/details/53453320)<sup>[2]</sup>  

| 目录                     | 宏代码         | 用途                                         |
|--------------------------|----------------|----------------------------------------------|
| /root/rpmbuild/SOURCES   | %_sourcedir    | 保存源码包（如 .tar 包）和所有 patch 补丁    |
| /root/rpmbuild/BUILD     | %_builddir     | 源码包被解压至此，并在该目录的子目录完成编译 |
| /root/rpmbuild/BUILDROOT | %_buildrootdir | 保存 %install 阶段安装的文件                 |
| /root/rpmbuild/SPECS     | %_specdir      | 保存 RPM 包配置（.spec）文件                 |
| /root/rpmbuild/RPMS      | %_rpmdir       | 生成/保存二进制 RPM 包                       |
| /root/rpmbuild/SRPMS     | %_srcrpmdir    | 生成/保存源码 RPM 包(SRPM)                   |

***2.3、rpm常用路径宏***  
&emsp;&emsp; 各路径宏参考[文献](https://blog.csdn.net/get_set/article/details/53453320)<sup>[2]</sup>  

| 路径                                                    | 宏                 |
|---------------------------------------------------------|--------------------|
| /etc                                                    | %{_sysconfdir}     |
| /usr                                                    | %{_prefix}         |
| %{_prefix}                                              | %{_exec_prefix}    |
| %{_exec_prefix}/bin                                     | %{_bindir}         |
| %{_exec_prefix}/%{_lib}                                 | %{_libdir}         |
| %{_exec_prefix}/libexec                                 | %{_libexecdir}     |
| %{_exec_prefix}/sbin                                    | %{_sbindir}        |
| /var/lib                                                | %{_sharedstatedir} |
| %{_prefix}/share                                        | %{_datarootdir}    |
| %{_datarootdir}                                         | %{_datadir}        |
| %{_prefix}/include                                      | %{_includedir}     |
| /usr/share/info                                         | %{_infodir}        |
| /usr/share/man                                          | %{_mandir}         |
| /var                                                    | %{_localstatedir}  |
| %{_sysconfdir}/rc.d/init.d                              | %{_initddir}       |
| /var                                                    | %{_var}            |
| %{_var}/tmp                                             | %{_tmppath}        |
| /usr                                                    | %{_usr}            |
| %{_usr}/src                                             | %{_usrsrc}         |
| lib (lib64 on 64bit multilib systems)                   | %{_lib}            |
| %{_datadir}/doc                                         | %{_docdir}         |
| %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch} | %{buildroot}       |
| %{buildroot}                                            | $RPM_BUILD_ROOT    |

***3、源码打包方法***  
&emsp;&emsp; SPECS撰写方法参考[文献](https://www.cnblogs.com/SQL888/p/5776442.html)<sup>[3]</sup>，这里以最后实现的一个rpm项目打包为例。首先要在/root/rpmbuild/SPECS/目录下新建一个.spec文件，并且内部需要实现一些字段，下面解释各个部分的作用:
```sh
# 项目名
name: CTest
# 项目版本
Version: 1.0
# 发布序列号
Release: 1%{?dist}
# 概要
Summary: The "CTest" program from GNU
Summary(zh_CN):  GNU "Hello World" 程序
# 开源协议
License: GPLv3+
# 源代码路径，即放在SOURCES目录下的tar包名
Source0: %{name}.tar.gz

# 简介
%description
The "CTest" program

# 简介中文
%description -l zh_CN
"CTest" 程序

# rpm进行实际打包准备工作的阶段
%prep

# rpm安装前执行的脚本
%prep
# 作用: 将解压后的源码重命名为/root/rpmbuild/BUILD/CTest/
%setup -n CTest

# rpm安装后执行的脚本
%post

# rpm卸载前执行的脚本
%preun

# rpm卸载后执行的脚本
%postun

# build默认 cd /root/rpmbuild/BUILD/CTest/ 目录下
%build
mkdir build
cd build
cmake ..
make %{?_smp_mflags}

# install默认 cd /root/rpmbuild/BUILD/CTest/ 目录下
# 开始把软件安装到虚拟的根目录中，正规写法应该是在MakeFile里面些install
# 虚拟根目录即 /root/rpmbuild/BUILDROOT/’包名‘
# 可以用宏 $RPM_BUILD_ROOT 或 %{buildroot} 代替
%install
mkdir -p %{buildroot}%{_bindir}
cd build
cp CTest %{buildroot}%{_bindir}

# files能指定最终打包到安装包的文件
# !!files默认 cd /root/rpmbuild/BUILDROOT/'包名'/ 目录下
# %defattr(文件权限,用户名,组名,目录权限),其中'-'表示默认权限
%files
%defattr(-,root,root,-)
%{_bindir}/*

# 变更日志
%changelog
* Sun MAY 4 2021 Your Name <youremail@xxx.xxx> - 1.0
- Update to 1.0
```
&emsp;&emsp;最后只需要执行生成rpm包的指令:
```sh
rpmbuild -ba '.spec文件路径'
```

***4、非源码打包方法***  
&emsp;&emsp; 如果无源码，只有一些已经编译完成的链接库与可执行文件，则可以借用打包机制，跳过编译步骤，直接将需要打入rpm包的文件拷贝到/root/rpmbuild/BUILDROOT/目录下:
```sh
...
# rpm进行实际打包准备工作的阶段
%prep
mkdir -p %{buildroot}/'文件安装的路径'
cp -r '要存放的文件夹' %{buildroot}/'文件安装的路径'
...
...
# files能指定最终打包到安装包的文件
%files
%defattr(-,root,root,-)
%'需要打包的路径'
```
&emsp;&emsp;最后只需要执行生成rpm包的指令:
```sh
rpmbuild -ba '.spec文件路径'
```

### *0x02 deb打包*
&emsp;&emsp;虽然deb打包的网上资料较少，但是实际上也是能实现源码与非源码打包的，并且天然支持CMake。可以参考下[debian维护手册](https://www.debian.org/doc/manuals/maint-guide/index.zh-cn.html)<sup>[4]</sup>。  
&emsp;&emsp;打包方法总共有三种:  
- debuild - 这种方法较复杂但是做的事情最多。该方法会创建上传Debian软件包所需的所有文件。它首先运行 dpkg-buildpackage，然后在创建的 .changes 文件上运行 lintian（假设安装了 lintian，这是一个 Debian 上面的包质量的检测工具），最后根据需要对 .changes 和/或 .dsc 文件进行签名。  
- dpkg-buildpackage - debuild方法的第一步，如果不做签名等复杂操作，这个方法足矣
- dpkg-deb - 这种方法是为了快速打包，并且只能非源码打包，但并不是常用的方法，相比之下，还是使用dpkg-buildpackage更好
```
1 环境搭建
2 基础知识构建
  2.1 deb打包文件结构
  2.2 debian/control文件详解
  2.3 debian/rules文件粗解
  2.4 debian/install + debian/postinst的使用
3 源码打包方法
  3.1 debuild / dpkg-buildpackage
4 非源码打包方法
  4.1 debuild / dpkg-buildpackage
  4.2 dpkg-deb
```
***1、环境搭建***  
```sh
# debuild环境
sudo apt install dh-make devscripts cmake gcc

# dpkg-buildpackage环境
sudo apt install dh-make cmake gcc

# dpkg-deb环境
sudo apt install fakeroot cmake gcc
```

***2、基础知识构建***  
***2.1、deb打包文件结构***  
&emsp;&emsp; 在已有tar.gz包的情况下(无论里面放源码还是编译生成后文件，自动生成debian目录只需要得到tar包名字)，可以使用dh_make工具自动生成debian目录(具体方法在下面几节)。下面具体描述debian文件夹各文件的作用:  
```sh
# deb源码打包示例项目的最终结构如下
debbuild/
├── ctest-1.0
│   ├── CMakeLists.txt
│   ├── CTest.cpp
│   └── debian
│       ├── changelog
│       ├── compat
│       ├── control
│       ├── rules
│       └── source
│           └── format
└── ctest-1.0.tar.gz

# debian目录是自动生成的，初始生成结构如下
# 需要注意dpkg-buildpackage指令使用小写debian
# dpkg-deb指令使用大写DEBIAN文件夹
debian/
├── changelog          # 包的更新历史，后面可以使用dch -i指令修改
├── compat             # 包的兼容性，与debian policy版本有关
├── control            # 包的描述信息
├── copyright          # 包的版权信息
├── ctest.cron.d.ex
├── ctest.default.ex
├── ctest.doc-base.EX
├── ctest-docs.docs
├── init.d.ex
├── manpage.1.ex
├── manpage.sgml.ex
├── manpage.xml.ex
├── menu.ex
├── postinst.ex        # 安装后执行脚本，使用前去掉.ex后缀
├── postrm.ex          # 卸载后执行脚本，使用前去掉.ex后缀
├── preinst.ex         # 安装前执行脚本，使用前去掉.ex后缀
├── prerm.ex           # 卸载前执行脚本，使用前去掉.ex后缀
├── README.Debian
├── README.source
├── rules              # 包的编译方法
├── source
│   └── format         # 包的版本
└── watch.ex           # 包的升级链接，使用前去掉.ex后缀
```

***2.2、debian/control文件详解***  
&emsp;&emsp;其他文件均可自行研究，但是control文件是最重要的，与初始状态不一致，已经改过，这边有必要解释一下:
```sh
$ cat debbuild/ctest-1.0/debian/control 
Source: ctest  # 这就是根据tar.gz包名自动生成的项目名
Section: unknown  # 该源码包要进入发行版中的分类
Priority: optional  # 描述用户安装该包的重要程度
Maintainer: xyh <yhxu94@126.com>  # 源码维护者的名字和邮箱
Build-Depends: debhelper (>=9)  # 编译依赖
 cmake,
 qtbase5-dev
Standards-Version: 3.9.6  # 此软件包所依据的“Debian Policy Manual”标准版本号
Homepage: https://jailbreakfox.github.io/

Package: ctest  # 二进制软件包的名称。通常情况下与源代码包相同，但不是必须的
Architecture: any  # 目标机架构，可以是其他架构，比如amd64
# Debian软件包系统最强大的特性之一。每个软件包都可以和其他软件包有各种不同的关系
Depends: ${shlibs:Depends}, ${misc:Depends}  # 运行时依赖
Recommends: XXXX(>=5.1.0.0)   # 建议依赖，不影响使用
Description:  # 软件的简短描述
```

***2.3、debian/rules文件粗解***  
&emsp;&emsp;网上都说control是debian目录下的核心文件，但其实还有一个很重要的文件就是rules，但由于目前精力有限，只能大致窥探其作用。在不知道如何使用的情况下，使用初始化的rules文件即可。  
&emsp;&emsp;rules文件本质上是一个Makefile文件，这个Makefile文件定义了创建deb格式软件包的规则。打包工具按照rules文件指定的规则，完成编译，将软件安装到临时安装目录，清理编译目录等操作，并依据安装到临时目录的文件来生成deb格式的软件包。
dh_make 会生成一个使用 dh 命令的非常简单但非常强大的默认的 rules 文件:
```sh
#!/usr/bin/make -f
# -*- makefile -*-
# Uncomment this to turn on verbose mode.
#export DH_VERBOSE=1  打开后编译输出更详细
#export DH_BUILD_OPTIONS=nocheck  可以跳过编译后的测试，对于某些编译不过的包有效

%:
  dh $@
```
&emsp;&emsp;实际上rules文件的dh语言是由debhelper工具来解析的，不要看上面只有短短一行语句，但实际上它的进化简化过程很漫长:  

<div align=center>
<img src="./debhelper进化.png" />
<div align=left>  

&emsp;&emsp;甚至有些指令会在实际打包的时候用到，从中可以窥见其运行的过程:  
```sh
# 打包结束后，打包目录下是非常乱的
$ tree debian
debian/
├── changelog
├── compat
├── control
├── ctest
│   ├── DEBIAN
│   │   ├── control
│   │   └── md5sums
│   └── usr
│       ├── bin
│       │   └── CTest
│       └── share
│           └── doc
│               └── ctest
│                   └── changelog.Debian.gz
├── ctest.debhelper.log
├── ctest.substvars
├── debhelper-build-stamp
├── files
├── rules
└── source
    └── format

# 此时可以在打包目录下执行dh clean，清理打包产生的文件
# 实际上dh clean就是执行了下面三个指令
$ dh clean
output:
   dh_testdir
   dh_auto_clean
   dh_clean
```

***2.4、debian/install + debian/postinst的使用***  
&emsp;&emsp;还有一个文件对于非源码打包作用很大，即debian/install。如果你的软件包需要那些标准的make install没有安装的文件，你可以把文件名和目标路径写入 debian/install文件，它们将被 dh_install安装:
```sh
# 假设有个空文件的tar.gz包，文件结构如下
$ tree test-1.0
test-1.0/
├── debian
│   └── install
└── 1.md
```
&emsp;&emsp;install的初始位置就是在打包根目录下，install文件可以这样写:
```sh
#!/bin/bash
cp 1.md /home
```
&emsp;&emsp;如果想在安装成功后修改文件的权限，则需要修改postinst文件，可以这样写:
```sh
#!/bin/sh
chmod 777 /home/1.md
```
&emsp;&emsp;目前还有一个遗留问题，就是打包前给的777权限，安装后权限变成了755。

***3.1、源码打包方法 - debuild / dpkg-buildpackage***  
&emsp;&emsp;deb源码打包一个优点是能够识别CMake文件，并自动编译。现以一个实例程序展示源码打包的流程:  
```sh
# 源码结构
# 注意源码根文件夹名不能有大写
# 根文件名一般取 项目名称 + '-' + 版本号，例如ctest-1.0
$ tree debbuild
debbuild/
└── ctest-1.0
    ├── CMakeLists.txt
    └── CTest.cpp

# 生成tar.gz包
$ tar -zcvf debbuild/ctest-1.0.tar.gz
$ tree debbuild
debbuild/
├── ctest-1.0
│   ├── CMakeLists.txt
│   └── CTest.cpp
└── ctest-1.0.tar.gz

# 使用dh_make自动生成debian包，选择'single' 'Y'
$ cd ctest-1.0
$ dh_make -f ../ctest-1.0.tar.gz
$ tree debbuild
debbuild/
├── ctest-1.0
│   ├── CMakeLists.txt
│   ├── CTest.cpp
│   └── debian
└── ctest-1.0.tar.gz

# 最后使用debuild / dpkg-buildpackage去生成deb包
$ cd ctest-1.0
$ debuild -us -uc -b
# 或者
$ dpkg-buildpackage -us -uc -b
$ tree debbuild
debbuild/
├── ctest-1.0
│   ├── CMakeLists.txt
│   ├── CTest.cpp
│   ├── debian
│   └── obj-x86_64-linux-gnu
├── ctest_1.0-1_amd64.deb
└── ctest-1.0.tar.gz

# 末了，可以使用dh clean清理生成的多余文件
$ dh clean
```
&emsp;&emsp;值得注意的是，目前仍不知道如何使用rules文件，因此源码打包流程中所有的make install过程均在CMakeList.txt实现(实际上也应该这么实现)。

***4.1、非源码打包方法 - debuild / dpkg-buildpackage***  
&emsp;&emsp;非源码打包需要使用debian/install与debian/rules文件的作用。
```sh
# 打一个空tar包
# 并在打包根目录下新建一个1.md的文档
$ tree debbuild
debbuild/
├── ctest-1.0
│   ├── 1.md
│   └── debian
└── ctest-1.0.tar.gz

# 添加debian/install文件，内容如下
"
#!/bin/bash
cp 1.md /home
"

# 最后使用dpkg-buildpackage去生成deb包
# 观察debian的目录结构，发现有一个ctest文件夹，该目录就是创建的假根目录
# 而1.md文件已经被放了进去
$ tree debian
debian/
└── ctest
    ├── DEBIAN
    │   ├── control
    │   └── md5sums
    ├── home
    │   └── 1.md
    └── usr
        └── share
            └── doc
                └── ctest
                    ├── changelog.Debian.gz
                    ├── copyright
                    └── README.Debian
# 另外也可以观察生成的deb包，文件确实已经打进deb包
$ dpkg -c ctest_1.0-1_amd64.deb
output:
drwxr-xr-x root/root         0 2021-06-25 17:17 ./home/
-rwxr-xr-x root/root         0 2021-06-25 17:03 ./home/1.md

# 最后使用debuild / dpkg-buildpackage去生成deb包
$ cd ctest-1.0
$ debuild -us -uc -b
# 或者
$ dpkg-buildpackage -us -uc -b

# 末了，可以使用dh clean清理生成的多余文件
$ dh clean
```

***4.2、非源码打包方法 - dpkg-deb***  
&emsp;&emsp;该方法只适用于非源码打包，但是优点是不需要写make install，因为它的DEBIAN文件同级目录下的其他目录结构就代表了需要install的路径:
```sh
# 先搭建一个打包目录
# 注意DEBIAN文件夹必须大写，且DEBIAN/control文件与自动生成的格式不同
$ tree dpkgdeb
dpkgdeb/
├── CTest                   # 源码包
│   ├── CMakeLists.txt
│   ├── CTest.cpp
│   └── build               # 手动编译结果存放文件夹
└── ctest-1.0
    ├── DEBIAN              # 手动生成的DEBIAN文件
    │   ├── changelog
    │   ├── compat
    │   ├── control
    │   └── rules
    └── usr                 # DEBIAN同级目录下的其他文件夹，即最终安装位置
        └── bin
            └── CTest       # 编译出来的可执行程序，从CTest/build文件夹下拷贝

# DEBIAN/control文件格式
$ cat DEBIAN/control
Package: ctest
Version: 1.0
Architecture: any
Maintainer: xuyanghe <yhxu94@126.com>
Section: devel
Priority: optional
Homepage: https://jailbreakfox.github.io
Description: deb package make tutorial

# 在打包根目录的父目录执行dpkg-deb
$ cd dpkgdeb
$ fakeroot dpkg-deb -b ctest-1.0 ctest-1.0.deb
```

### *0x03 引用文献*
[1]https://github.com/JailbreakFox/Linux-sh-package/blob/master/Centos/Centos%20Mini.md
[2]https://blog.csdn.net/get_set/article/details/53453320
[3]https://www.cnblogs.com/SQL888/p/5776442.html
[4]https://www.debian.org/doc/manuals/maint-guide/index.zh-cn.html