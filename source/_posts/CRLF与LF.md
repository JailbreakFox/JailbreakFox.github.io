---
title: CRLF与LF
tags: 计算机技术
date: 2019-08-29 13:41:23
grammar_cjkRuby: true
---

### *0x00 引言*
&emsp;&emsp;CRLF, LF 是用来表示文本换行的方式。CR(Carriage Return) 代表回车，对应字符 '\r'；LF(Line Feed) 代表换行，对应字符 '\n'。  
&emsp;&emsp;不同操作系统会使用不同的换行方式，这也是导致我们传输文件时出现乱码的原因之一。目前主流的操作系统中，Windows使用的是CRLF, Unix系统(包括Linux, MacOS近些年的版本)使用的是LF。

### *0x01 Git换行符*  
&emsp;&emsp;Git服务器使用的换行方式是LF。  

***1、换行符自动转换***  
&emsp;&emsp;由于要考虑操作系统区别，Git提供了一个"[换行符自动转换](https://blog.csdn.net/weixin_33275327/article/details/81485051)<sup>[1]</sup>"(AutoCRLF)功能，即当Windows用户向Git提交代码时，自动将CRLF格式转换为LF格式，当Windows用户拉代码时，又自动将代码转换为CRLF格式。  
&emsp;&emsp;AutoCRLF使用方法如下：
```sh
##Windows系统
#提交时转换为LF，检出时转换为CRLF
git config --global core.autocrlf true
##Unix系统
#提交时转换为LF，检出时不转换
git config --global core.autocrlf input
##None
#提交、检出均不转换
git config --global core.autocrlf false
```
***2、禁止/警告不可逆转换***
&emsp;&emsp;由于没有一个绝对有效的算法来判断一个文件是否采用多种换行符混合模式，因此Git还提供了"[禁止/警告不可逆转换](https://www.jianshu.com/p/ec9564fe1c2b)<sup>[2]</sup>"的配置，可以自动完成标准化与转换。它的设置方式如下：
&emsp;&emsp;SafeCRLF使用方法如下：
```sh
#拒绝提交包含混合换行符的文件
git config --global core.safecrlf true
#允许提交包含混合换行符的文件
git config --global core.safecrlf false
#提交包含混合换行符的文件时给出警告
git config --global core.safecrlf warn
```

### *0x02 换行符格式转换工具*
&emsp;&emsp;由于日常工作的时候会经常下载到不同换行符格式的文件，导致出现乱码或无法编译。现使用Unix下的一个转换工具[dos2unix](https://blog.csdn.net/yonggang7/article/details/38459143)<sup>[3]</sup>，它能将LF、CRLF格式文件进行相互转换。安装方式较为简单：
```sh
sudo apt-get install dos2unix
```
&emsp;&emsp;另外附上其常用的使用方法：
```sh
#-k 保持源文件mtime
#-n 保留旧文件，转换结果输出到新文件。
dos2unix -k -n file newfile
```

### *0x03 引用文献*
[1]https://blog.csdn.net/weixin_33275327/article/details/81485051
[2]https://www.jianshu.com/p/ec9564fe1c2b
[3]https://blog.csdn.net/yonggang7/article/details/38459143
