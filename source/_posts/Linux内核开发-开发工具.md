---
title: Linux内核开发-开发工具
date: 2018-10-20 15:00:44
tags: Linux 工具
---
### *0x00 引言*
&emsp;&emsp;Linux内核开发所用到的工具。

### *0x01 Vim*
&emsp;&emsp;想用终端开发软件的程序员都会选择Vim，使用方法参考[菜鸟教程](https://www.runoob.com/linux/linux-vim.html)。
<div align=center>
<img src="./Vim键盘图.png" width = "450" height = "300" />
<div align=left>  

<div align=center>
<img src="./Vim命令图解.png" width = "450" height = "300" />
<div align=left>  

### *0x02 Linux系统运维常用工具*
```sh
1 top
  1.1 系统运行时间和平均负载
  1.2 进程状态
  1.3 CPU状态
  1.4 内存使用
  1.5 各进程的状态监控
2 free
3 vmstat
4 slabtop
5 pmap
6 dmesg
7 lsof
```
***1、top***  
&emsp;&emsp;除了 top ，还可以使用 htop 命令，但是需要安装。
&emsp;&emsp;[top命令](https://www.cnblogs.com/mushang1hao/p/10767062.html)经常用来监控Linux的系统状况，比如cpu、内存的使用，命令如下：
```sh
top
```
<div align=center>
<img src="./top.png" width = "450" height = "300" />
<div align=left>  

***1.1、系统运行时间和平均负载***  

- top：当前时间
- up：系统已运行的时间
- user：当前登录用户的数量
- load average：相应最近5、10和15分钟内的平均负载，每隔5秒钟检查一次活跃的进程数。 

***1.2、进程状态***  
&emsp;&emsp;按"t"切换显示状态。  
- total：总共进程数
- running：运行中进程
- sleeping：休眠中进程
- stopped：停止中进程
- zombie：僵尸进程  

***1.3、CPU状态***  
&emsp;&emsp;按"1"显示所有CPU状态。 
- us / user： 用户空间占用CPU的百分比
- sy / system: 内核空间占用CPU的百分比
- ni / niced：改变过优先级的进程占用CPU的百分比
- id：空闲CPU百分比
- wa / IO wait: IO等待占用CPU的百分比
- hi：处理硬件中断占用CPU的百分比
- si: 处理软件中断占用CPU的百分比
- st：这个虚拟机被hypervisor偷去时间占用CPU的百分比（译注：如果当前处于一个hypervisor下的vm，实际上hypervisor也是要消耗一部分CPU处理时间的）。

***1.4、内存使用***  
&emsp;&emsp;按"m"切换显示状态。  
*内存区-Mem*  

- total：物理内存总量
- used：使用中的内存总量
- free：空闲内存总量
- buffers/cache：缓存的内存量

*交换分区-Swap*  

- total：交换区总量
- used：使用的交换区总量
- free：空闲交换区总量
- avail Mem：缓冲的交换区总量

***1.5、各进程的状态监控***  
&emsp;&emsp;按"f"可添加需要监控的状态变量，按"M"可按各进程内存占有百分比降序排列，按"P"可按各进程CPU占有百分比降序排列。  
- PID：进程ID，进程的唯一标识符
- USER：进程所有者的实际用户名。
- PR：进程的调度优先级。这个字段的一些值是'rt'。这意味这这些进程运行在实时态。
- NI：进程的nice值（优先级）。越小的值意味着越高的优先级。负值表示高优先级，正值表示低优先级
- VIRT：进程使用的虚拟内存。进程使用的虚拟内存总量，单位kb。VIRT=SWAP+RES
- RES：驻留内存大小。驻留内存是任务使用的非交换物理内存大小。进程使用的、未被换出的物理内存大小，单位kb。RES=CODE+DATA
- SHR：SHR是进程使用的共享内存。共享内存大小，单位kb
- S：这个是进程的状态。它有以下不同的值:
  - D：不可中断的睡眠态。
  - R：运行态
  - S：睡眠态
  - T：被跟踪或已停止
  - Z：僵尸态
- %CPU：自从上一次更新时到现在任务所使用的CPU时间百分比。
- %MEM：进程使用的可用物理内存百分比。
- TIME+：任务启动后到现在所使用的全部CPU时间，精确到百分之一秒。
- COMMAND：运行进程所使用的命令。进程名称（命令名/命令行）

***2、free***  
&emsp;&emsp;free 命令显示系统内存的使用情况，包括物理内存、交换内存(swap)和内核缓冲区内存，命令如下：  
```sh
# 最直接
free
# 更友好的输出结果
free -h
# 指定3s不间断更新
free -h -s 3
```
<div align=center>
<img src="./free.png" width = "450" height = "300" />
<div align=left>  

- Mem行：是内存的使用情况。
- Swap行：是交换空间的使用情况。
- total列：显示系统总的可用物理内存和交换空间大小。
- used列：显示已经被使用的物理内存和交换空间。
- free列：显示还有多少物理内存和交换空间可用使用。
- shared列：显示被共享使用的物理内存大小。
- buff/cache列：显示被 buffer 和 cache 使用的物理内存大小。
- available列：显示还可以被应用程序使用的物理内存大小。

***3、vmstat***  
&emsp;&emsp;vmstat命令可对操作系统的虚拟内存、进程、CPU活动进行监控，命令如下：  
```sh
# 时间间隔2s，采样10次
vmstat 2 10
```
<div align=center>
<img src="./vmstat.png" width = "450" height = "300" />
<div align=left>  

*进程-Procs*  
- r: 运行队列中进程数量
- b： 等待IO的进程数量

*内存-Memory*
- swpd: 使用虚拟内存大小
- free: 可用内存大小
- buff: 用作缓冲的内存大小
- cache: 用作缓存的内存大小

*交换分区-Swap*
- si: 每秒从交换区写到内存的大小
- so: 每秒写入交换区的内存大小

*IO*
- in: 每秒中断数，包括时钟中断。【interrupt】
- cs: 每秒上下文切换数。【count/second】

*CPU*
- us: 用户进程执行时间(user time)
- sy: 系统进程执行时间(system time)
- id: 空闲时间(包括IO等待时间),中央处理器的空闲时间 。以百分比表示。
- wa: 等待IO时间

***4、slabtop***  
&emsp;&emsp;Linux内核需要为临时对象如任务或者设备结构和节点分配内存，缓存分配器管理着这些类型对象的缓存。现代Linux内核部署了该缓存分配器以持有缓存，称之为片。不同类型的片缓存由片分配器维护。本文集中讨论slabtop命令，该命令显示了实时内核片缓存信息。
```sh
# slabtop排序方式设置为最常用的cache size
slabtop -sc
```
<div align=center>
<img src="./slabtop.png" width = "450" height = "300" />
<div align=left>  

***5、pmap***
&emsp;&emsp;pmap命令用于报告进程的内存映射关系，是Linux调试及运维一个很好的工具，这里自己写个代码来测试该工具：
```c
// 编译具有如下代码的test.cpp文件
#include <stdio.h>
#include <memory.h>
int main() {
    char *buf;
    buf = (char *)malloc(10 * sizeof(char));
    memset(buf, 0x55, 10 * sizeof(char));
    while(1);
}
```
&emsp;&emsp;编译完成后，使用如下命令运行：
```sh
# 在后台执行test程序
./test &
# 记录下后台运行时的程序PID，并使pmap工具查看
pmap "程序PID"
```

***6、dmesg***  
&emsp;&emsp;dmesg命令用于显示开机信息。  
```sh
# "-T"代表log打印出时间，"-d"代表log打印出两条指令之间的差值
dmesg -T -d
```

***7、lsof***  
&emsp;&emsp;lsof用于查看进程打开的文件或打开文件的进程:
```sh
lsof -p 1359    # 查看某个PID进程打开的所有文件
lsof -u root    # 查看某个用户打开的所有文件
lsof -u ^root   # 查看不是某个用户打开的文件，也就是取反，在用户名前加^
lsof /dev/null  # 查看某个文件被哪些进程打开使用
lsof -i:22      # 查看某个端口的使用情况
```

### *0x03 Linux系统开发常用工具*
```sh
1 日志读取-journalctl
2 进程服务管理-systemctl/service
3 核心转储-coredump
4 进程查询-ps + grep/pgrep/pidof/pstree
5 杀死进程-kill/killall/pkill
6 网络诊断-ping
7 硬件信息-dmidecode/uname + lspci
8 文件操作-cat/less/more/mv/cp/rm/chmod/ls+file+stat+du/grep/echo/find/locate/which/whereis/sed/ln
9 帮助指令-man
10 屏保设置-xset
11 超级用户-sudo/pkexec
12 文件内容操作-tail/wc/sort/uniq/paste
13 压缩文件-zip/rar/tar/xz
14 挂载-mount
15 分区信息-df/fdisk/lsblk/blkid
16 权限更改-chmod/chown/chroot/chattr/getfacl+setfacl
17 用户管理-useradd/userdel/usermod/groups
18 二进制文件分析-file/ldd/ltrace/strace/hexdump/strings
19 日志保存-sosreport
20 远程文件操作-scp/rsync
21 读取转换数据-dd
22 历史终端命令-history
23 终端代理-proxychains
24 打开文件-xdg-open
25 用户信息-who/loginctl/hostnamectl
26 密码过期设置-chage
27 环境变量-export/locale/env
28 编辑器-gedit/dedit
29 反汇编-objdump/strings
30 电源指令-poweroff/shutdown/reboot/Hibernate/suspend/logout/rtcwake
31 键鼠输入事件监听-libinput
32 窗口查看进程-xprop
33 多屏查询-xrandr
34 输入输出重定向
35 ssh免密码登录
36 计划任务-cron
37 网络配置-nmcli
```
***1、日志读取-journalctl***  
&emsp;&emsp;在Systemd出现之前，Linux系统及各应用的日志都是分别管理的，Systemd开始统一管理了所有Unit的启动日志，这样带来的好处就是可以只用一个 journalctl命令，查看所有内核和应用的日志。
```sh
# -----1、查看所有日志-----
sudo journalctl > "文件名"
# 查看本次启动的所有日志也可以使用
sudo journalctl -b > "文件名"

# -----2、查看指定时间内的日志-----
# --since代表某段时间之后，--until代表某段时间之前
journalctl --since="2018-09-21 10:21:00" --until="2018-09-21 10:22:00"

# -----3、实时查看并写入日志-----
journalctl -f |& tee -a '*.log'

# -----4、在程序中加入日志打印功能-----
# include <unistd.h>  //linux中的一些重要函数
system("echo `命令行内容` > '日志存放目录'")   //反引号内为需要执行的命令，然后用 > 输出日志到指定目录

# -----5、查看指定单元日志-----
# 查看systemd-logind日志
journalctl -u systemd-logind
```

***2、进程服务管理-systemctl/service***  
&emsp;&emsp;systemd对应的进程管理命令是systemctl。
```sh
# -----1、进程开启/关闭/重启-----
systemctl start "进程名"
systemctl stop "进程名"
systemctl restart "进程名"

# -----2、进程开机自启动-----
# systemctl可以处理/etc/init.d
systemctl enable "进程名"

# -----3、进程状态查看-----
systemctl status "进程名"

# -----4、进程/服务屏蔽(永远不能启动)-----
# 屏蔽
systemctl mask "进程名"
# 取消屏蔽
systemctl unmask "进程名"
```
&emsp;&emsp;服务管理命令使用的是service。
```sh
# 如果要开启ssh服务
service ssh start
# 或者
systemctl start ssh
```

***3、核心转储-coredump***  
&emsp;&emsp;当程序运行的过程中异常终止或崩溃，操作系统会将程序当时的内存状态记录下来，保存在一个文件中，这种行为就叫做Core Dump（中文有的翻译成“核心转储”)。我们可以认为 core dump 是“内存快照”，但实际上，除了内存信息之外，还有些关键的程序运行状态也会同时 dump 下来，例如寄存器信息（包括程序指针、栈指针等）、内存管理信息、其他处理器和操作系统状态和信息。core dump 对于编程人员诊断和调试程序是非常有帮助的，因为对于有些程序错误是很难重现的，例如指针异常，而 core dump 文件可以再现程序出错时的情景。
```sh
# 安装
sudo apt install systemd-coredump

# -----1、调整cmake为调试模式-----
# 纯调试模式
set(CMAKE_BUILD_TYPE Debug)
# 或者半调试模式
set(CMAKE_BUILD_TYPE RelWithDebInfo)

# -----2、开启coredump-----
# 查看是否开启coredump，返回0则表示没开启
ulimit -c
# 开启coredump
ulimit -c unlimited

# -----3、修改core生成路径-----
# proc/sys/kernel/core_pattern 可以控制corefile保存位置和文件名格式
# corefile的生成路径文件夹
mkdir /corefile
## 控制所产生的core文件存放到/corefile目录下，产生的文件名为core-命令名-pid-时间戳
echo "/corefile/core-%e%-p%-%t" > /proc/sys/kernel/core_pattern

# -----4、调试模式下生成corefile-----
gdb "可执行程序路径" "corefile路径"

# -----**5、常用调试手段-----
# 查看内存溢出的进程历史
coredumpctl list
# debug目标PID进程
coredumpctl debug "进程PID"
bt  # gdb列出调用栈
```

***4 进程查询-ps + grep/pgrep/pidof/pstree***  
&emsp;&emsp;ps指令能显示进程的消息，grep是Linux下的文本过滤工具，它俩是个组合工具。我们经常用如下命令查找进程：
```sh
# 首先可以用ps直接查询PID对应的进程
ps 'PID号'
# 或者用ll去查看PID对应的进程
ll '/proc/PID号'

# 查找所有进程，并过滤出有进程名字片段的所有进程
# "|"是管道命令。通常需要借助管道命令"|"多个命令的组合
# ------ ps -ef ------
# 是用标准的格式显示进程的
ps -ef | grep "进程名片段"

# ------ ps aux ------
# 是用BSD的格式来显示
ps aux | grep "进程名片段"

# 如果觉得上述命令麻烦，可以使用两个更简介的写法
pgrep/pidof 'PID号'

# 还能使用pstree打印进程树
pstree
```

***5、杀死进程-kill/killall/pkill***  
```sh
# kill能杀死指定的ID进程，需要在杀进程之前使用ps等命令再配合grep来查找进程
kill "参数" "进程ID"

# killall/pkill类似，用于杀死指定名字的进程
killall "参数" "进程名"
pkill "参数" "进程名"
```

***6、网络诊断-ping***  
```sh
# -----1、ping单个目标-----
# ping域名
ping www.baidu.com
# ping IP
ping 10.10.10.1


# -----2、ping多个目标-----
# %d ：表示变量的意思
# (1,1,255)：参数一代表起始值，参数二代表递增值，参数三代表末尾值。
for /L %d in（1,1,255） do ping 192.168.1.%d
```

***7、硬件信息-dmidecode + lspci***  
```sh
# -----1、所有硬件信息-----
dmidecode –q
# 或者
uname -a

# -----2、显卡信息-----
lspci | grep -i vga     # VGA设备
lspci | grep -i nvidia  # NVIDIA设备
```

***8、文件操作-cat/less/more/mv/cp/rm/chmod/ls+file+stat/grep/echo/find/locate/which/whereis/sed***  
```sh
# -----1、cat-----
# 用于连接文件并打印到标准输出
cat "文件路径"

# -----2、less-----
# 用于连接文件并打印到标准输出
less "文件路径"

# -----3、more-----
# 用于连接文件并打印到标准输出
more "文件路径"

# -----4、mv-----
# 将文件移动到目标路径
mv "文件路径" "目标路径"

# -----5、cp-----
# 将文件拷贝到目标路径
cp "文件路径" "目标路径"

# -----6、rm-----
# 删除文件
rm "文件路径"
# 删除文件夹
rm -R "文件夹路径"

# -----7、chmod-----
# 修改文件权限
chmod 777 "文件路径"
# 修改文件夹权限
chmod -R 777 "文件夹路径"

# -----8、ls+file+stat+du-----
# 显示当前目录下所有文件信息
ls
# 显示更详细的文件信息，包括隐藏文件
ls -lah
# 显示符合条件的文件信息
ls|grep "删选的字符串" 

# 查看文件类型
file "文件路径"

# 查看详细的文件信息
stat "文件路径"

# 查看文件夹下各文件大小并排序(搜索结果以M为单位)
du -sm "文件夹路径" | sort -nr 

# -----9、grep-----
# 查找某文件下包含某个字段的行号
# 举例：grep "data" *ts    //查找当前目录下后缀为ts的文件中包含"data"字段的行号
grep "查询字段" '文件'

# -----10、echo-----
# 打印出环境变量
echo $SHELL
# 打印自定义字符
echo "It is a test"

# -----11、find/locate/which-----
# *grep
# 遍历文件夹内的所有文件，寻找指定字符串，并将查询结果分割输出
grep -rn "happyexam" /usr/* | cut -d : -f 2 >/opt/findcode.txt

# find
# 打印目录路径下后缀名为 .c 的所有文件
find '目录路径' -name "*.c"
find '目录路径' -name "*name"
find '目录路径' -name "*name*"
find '目录路径' -name "name*"
# 将目前目录及其子目录下所有最近 20 天内更新过的文件列出
find . -ctime -20
# 将目前目录及其子目录下后缀名为 .py 且文件名中包含 'test' 的文件列出
find . -name '*.py' |grep test
# 将目前目录及其子目录下后缀名为 .py 且文件中包含某字符串的文件列出
find . -name '*.py' |xargs grep "筛选字符串"
# 让终端不打印无权限查看的文件
find '目录路径' -name "*.c" 2 > /dev/null

# locate
# 更加方便的定位工具
# 安装
sudo apt install locate
# locate命令无法搜索当天所创建的文件，因此可用下面命令更新一次数据库
sudo updatedb
# 查找目标文件
locate '文件名'

# which
# 主要用来查找二进制文件位置
which '程序名'

# whereis
# 主要用来查找系统默认安装目录的二进制文件位置
whereis '程序名'

# -----12、sed-----
# 在文件的第4行新增一段内容
sed -e 4a\'新的内容' '文件目录' 
# 数据的搜寻并替换
sed 's/要被取代的字串/新的字串/g'
# 如果要立即写入，则需加'-i'参数，不然sed命令只会在终端输出结果

# -----13、ln-----
# 软链接
# 为原文件创造一个新的指针，类似于Windows的快捷方式
ln -s '原文件路径' '快捷方式路径'

# 硬链接
# 硬链接文件完全等同于原文件，两个文件都指向相同物理地址
# 只有当删除文件的最后一个节点时，文件才能真正从磁盘消除
ln '原文件路径' '快捷方式路径'
```

***9、帮助指令-man***  
man命令可查看指令帮助、配置文件帮助和编程帮助等信息
```sh
# 打印man指令信息
man man
```

***10、屏保设置-xset***  

|           命令          |           功能           |
| ----------------------- | ---------------------------- |
| xset s off              | 禁用屏幕保护           |
| xset s 3600 3600        | 设置空闲时间为1小时 |
| xset -dpms              | 关闭 DPMS                  |
| xset s off -dpms        | 禁用 DPMS 并阻止屏幕进入空闲 |
| xset dpms force on      | 立即打开屏幕        |
| xset dpms force off     | 立即关闭屏幕        |
| xset dpms force standby | 强制屏幕进入待命状态 |
| xset dpms force suspend | 强制屏幕进入暂停状态 |
| xset -q                 | 查询xset状态        |

***11、超级用户-sudo/pkexec***  
&emsp;&emsp;root用户和非root用户正常执行命令时，使用的PATH配置文件为 /etc/environment
```sh
# -----1、sudo-----
# 非root用户，使用的PATH配置文件为 /etc/sudoers
sudo '命令'

# -----2、pkexec-----
# pkexec 也能以管理员身份运行指令，但不依赖于 /etc/sudoers
# 如果不小心修改了 /etc/sudoers 文件权限，会导致无法正常使用sudo指令。但可以用pkexec修改回权限
pkexec chomod 440 /etc/sudoers
```

***12、文件内容操作-tail/wc/sort/uniq/paste***  
&emsp;&emsp;tail 命令可用于查看文件的内容，有一个常用的参数 -f 常用于查阅正在改变的日志文件。
```sh
# 实时打印日志文件
tail -f '日志路径'

# 显示文件所有行数
wc -l '文件路径'

# 排序文件行并输出
#    -r 以相反的顺序来排序
#    -n依照数值的大小排序
#    k是指按照那一列进行排序
#    -t <分隔字符>指定排序时所用的栏位分隔字符。
sort -rnk 3 -t : /etc/passwd    

# 在文件每行旁边显示该行重复次数并输出
uniq -c '文件路径'

# 将每个文件以列对列的方式合并
paste '文件路径1' '文件路径2'
```

***13、压缩文件-zip/rar/tar/xz***  
**zip**  
```sh
# ====== 压缩文件 ======
#将test.jpg和test.png压缩成一个zip包
zip test.zip test.jpg test.png
#将所有.jpg的文件压缩成一个zip包
zip test.zip *.jpg

# ====== 压缩目录 ======
#将文件夹test压缩成一个zip包
zip -r test.zip test

# ======解压缩 ======
#将test.zip中的所有文件解压出来
unzip test.zip
#把/home目录下面的mydata.zip解压到mydatabak目录里面
unzip mydata.zip -d mydatabak
```

**rar**  
```sh
# ====== 压缩文件 ======
# 将test.jpg和test.png压缩成一个rar包
rar a test.rar test.jpg test.png
# 将所有.jpg的文件压缩成一个rar包
rar a test.rar *.jpg
# 将文件夹test压缩成一个rar包
rar a test.rar test

# ======解压缩 ======
# 将test.rar中的所有文件解压出来
unrar e test.rar
```

**tar**  
```sh
# ====== 压缩文件 ======
# --- tar ---
tar -cvf xxx.tar '目录路径'
# --- tar.gz ---
#z参数表示gz压缩，v参数表示显示执行过程
tar -zcvf xxx.tar.gz '目录路径'

# ======解压缩 ======
# --- tar ---
tar -xvf xxx.tar
# --- tar.gz ---
tar -zxvf xxx.tar.gz
```

**xz**  
```sh
# ====== 压缩文件 ======
# --- xz ---
xz -z '目录路径'
# --- tar.xz ---
# 用xz工具打包tar压缩包
xz -z xxx.tar

# ======解压缩 ======
# --- xz ---
xz -d xxx.xz
# --- tar.xz ---
xz -d xxx.tar.xz
tar -xvf xxx.tar
```

***14、挂载-mount***  
```sh
# ====== 挂载 ======
# 最简单的挂载方式
mount /dev/hda1 /mnt
# 读写权限的挂载方式
# '-w' 相当于 '-o rw' 
mount -w /dev/hda1 /mnt
# 重新挂载为可读写的方式
mount -o remount,rw /mnt

# ====== 取消挂载 ======
unmount /mnt
```

***15、分区信息-df/fdisk/lsblk/blkid***  
```sh
# ====== df ======
# 列出文件系统磁盘占用情况
df -h

# ====== fdisk ======
# 列出磁盘分区
fdisk -l

# ====== lsblk/blkid ======
# 列出所有可用块设备信息
# 还能看到对应磁盘的挂载点
lsblk
# 查看挂载的详细信息，能输出挂载UID
blkid
```

***16、权限更改-chmod/chown/chroot/chattr/getfacl+setfacl***  
```sh
# 文件权限分类
  读权限 r：允许查看文件内容，使用4表示
  写权限 w：允许修改文件内容，使用2表示
  可执行 x：允许运行程序，使用1表示
  无权限 -：使用0表示

  例如：
    d rwx r-x r-x  意思是一个权限为 755 的目录
    - rw- r-- r--  意思是一个权限为 644 的文件

# ====== chmod ======
# 更改文件权限，语法为 'chmod abc file'
# 其中a,b,c各为一个数字，分别表示User、Group、及Other的权限:
# r=4，w=2，x=1
chmod 777 file

# 强制位u+s
# 任何用户执行被设置强制位的文件时，都能拥有该文件所有者的权限
# 例如一个二进制程序属于root，则uos用户执行该程序时，其具有root的权限
# 由于脚本文件拥有权限会有较大隐患，因此Linux只认可二进制程序的强制位
chmod u+s '文件路径'

# ====== chown ======
# 修改文件的拥有者与组
# 例如将文件 file1.txt 的拥有者设为 runoob，群体的使用者 runoobgroup :
chown runoob:runoobgroup file1.txt

# ====== chroot ======
# 改变根目录
chroot /mnt/ls

# ====== chattr ======
# 可修改文件/文件夹的"隐藏权限"
## i:如果对文件设置 i 属性，那么不允许对文件进行删除、改名，也不能添加和修改数据;如果对目录设置 i 属性，那么只能修改目录下文件中的数据，但不允许建立和删除文件
## a:如果对文件设置 a 属性，那么只能在文件中増加数据，但是不能删除和修改数据；如果对目录设置 a 属性，那么只允许在目录中建立和修改文件，但是不允许删除文件
## u:设置此属性的文件或目录，在删除时，其内容会被保存，以保证后期能够恢复，常用来防止意外删除文件或目录
## s:和 u 相反，删除文件或目录时，会被彻底删除（直接从硬盘上删除，然后用 0 填充所占用的区域），不可恢复
chattr +i '文件路径' # 设置文件不可删除，不可修改

# ====== getfacl+setfacl ======
# 获取文件访问控制信息
getfacl '文件路径'

# setfacl 设置文件的acl
#         -m 修改文件的acl
#         -x 取消用户或组对文件的权限
setfacl –m u:用户名:权限 <文件名>  # 设置某用户名的访问权限
setfacl –m g:组名:权限 <文件名>    # 设置某个组的访问权限
setfacl –x u:用户名 <文件名>      # 取消某用户名的访问权限
setfacl –x g:组名 <文件名>        # 取消某个组的访问权限
```

***17、用户管理-useradd/userdel/usermod/groups***  
```sh
# 创建一般用户
# '-m'新建用户主目录 '-d'设置新用户主目录 
# '-g'设置新用户主组名
useradd -m -d '用户目录' -g '用户组' '用户名'

# 删除用户
userdel '用户名'

# 修改用户信息
# '-u'设置用户UID '-s'设置新用户的Shell
usermod -u 'UID(如2020)' -s 'Shell名(如/usr/sbin/nologin)' '用户名'

# 查看用户属组
groups '用户名'

# 查看用户信息
cat /etc/passwd
```

***18、二进制文件分析-file/ldd/ltrace/strace/hexdump/strings***  
&emsp;&emsp;参考[良许的文章](https://os.51cto.com/art/202005/616628.htm)，用 /bin/pwd 程序为例:
```sh
# -----1、file-----
# 首先使用 file 命令来分析文件的类型
file /bin/pwd

# -----2、ldd-----
# ldd 命令可以用于分析可执行文件的依赖
ldd /bin/pwd

# -----3、ltrace-----
# ltrace的功能是能够跟踪进程的库函数调用
ltrace /bin/pwd

# -----4、strace-----
# strace 命令可以用于追踪程序运行过程中的系统调用及信号
strace -f /bin/pwd

# -----5、hexdump-----
# hexdump 命令用来查看二进制文件的 16 进制编码
# 但实际它能查看任何文件，而不限于二进制文件
hexdump -C /bin/pwd | head

# -----6、strings-----
# strings 命令可以用来打印二进制文件中可显示的字符
strings /bin/pwd | head 
```

***19、日志保存-sosreport***  
&emsp;&emsp;快速保存所有日志的工具  
```sh
# 安装
sudo apt install sosreport -y

# 使用，执行下面命令后，一直回车
sudo sosreport
```

***20、远程文件操作-scp/rsync***  
&emsp;&emsp;scp用来做全量备份,每次都是完全拷贝,效率低下。rsync用来做增量备份,每次仅拷贝发生变化的文件,效率高。
```sh
# scp传输本地文件到目标主机文件目录
scp '本地文件目录' root@172.16.1.31:'目标文件目录'
# scp传输目标主机文件目录到本地文件目录
scp root@172.16.1.31:'目标文件目录' '本地文件目录'

# rsync传输本地文件到目标主机文件目录
rsync -avz '本地文件目录' root@172.16.1.31:'目标文件目录'
# rsync传输目标主机文件目录到本地文件目录
rsync -avz root@172.16.1.31:'目标文件目录' '本地文件目录'
```

***21、读取转换数据-dd***  
&emsp;&emsp;dd可从标准输入或文件中读取数据，根据指定的格式来转换数据，在输出到文件、设备或标准输出。比较典型的作用就是制作系统U盘:  
```sh
# dd制作系统U盘，bs参数代表同时设置读入/输出的块大小
dd if='.img镜像文件路径' of='U盘路径' bs=1440k

# dd还能磁盘克隆
dd if=/dev/sda of=/dev/sdb

# dd制作镜像
dd if=/dev/sda of=~/disk.img

# 观察dd制作镜像进度
watch -n 5 killall -USR1 dd
```

***22、历史终端命令-history***  
&emsp;&emsp;能够列出终端使用的历史命令记录。
```sh
# 列出历史3条命令
histoty -3
```

***23、终端代理-proxychains***  

***24、打开文件-xdg-open***  
```sh
xdg-open '文件路径'
```

***25、用户信息-who/loginctl/hostnamectl***  
```sh
# who查看当前用户
who
w

# loginctl查看所有用户
loginctl -a

# hostnamectl可用于修改用户名相关内容
hostnamectl set-hostname '用户名'
```

***26、密码过期设置-chage***  
```sh
# 用法  chage [选项] 用户名
# -m：密码可更改的最小天数。为零时代表任何时候都可以更改密码。
# -M：密码保持有效的最大天数。
# -w：用户密码到期前，提前收到警告信息的天数。
# -E：帐号到期的日期。过了这天，此帐号将不可用。
# -d：上一次更改的日期。
# -i：停滞时期。如果一个密码已过期这些天，那么此帐号将不可用。
# -l：例出当前的设置。由非特权用户来确定他们的密码或帐号何时过期。
```

***27、环境变量-export/locale/env***  
&emsp;&emsp;环境变量分为系统级变量和用户级环境变量。关于系统级变量的配置文件如下:  
```sh
# /etc/profile
# 在系统启动后第一个用户登录时运行
# 并从/etc/profile.d目录的配置文件中搜集shell的设置
# 使用该文件配置的环境变量将应用于登录到系统的每一个用户。

# /etc/bashrc（Ubuntu和Debian中是/etc/bash.bashrc）
# 在 bash shell 打开时运行(注意，只针对bash shell)，修改该文件配置的环境变量将会影响所有用户使用的bash shell。

# /etc/environment
# 在系统启动时运行，用于配置与系统运行相关但与用户无关的环境变量
# 修改该文件配置的环境变量将影响全局。
```
关于用户级变量的配置文件如下:  
```sh
# ~/.profile（推荐首选）
# 当用户登录时执行，每个用户都可以使用该文件来配置专属于自己使用的shell信息

# ~/.bashrc（不推荐）
当用户登录时以及每次打开新的shell时该文件都将被读取
不推荐在这里配置用户专用的环境变量，因为每开一个shell，该文件都会被读取一次，效率肯定受影响


# ~/.bash_profile 或 ~./bash_login - 
如果有其中的一个文件存在的话, 当启动的是一个 登录shell时，Bash 会执行该文件而不会执行~/.profile
如果两个文件都存在的话，Bash 将会优先执行~/.bash_profile 而不是~/.bash_login
然而, 默认情况下，这些文件不会影响图形会话

# ~/.bash_logout
当每次退出系统(退出bash shell)时执行该文件

# 总结
一般情况下，Linux加载环境变量配置文件的执行顺序为
==> /etc/profile
==> ~/.bash_profile | ~/.bash_login | ~/.profile
==> ~/.bashrc
==> /etc/bashrc
==> ~/.bash_logout
```
下面解释下，各个修改配置文件的命令和方法:  
```sh
# export
# 该命令用于设置或显示环境变量。但是export 的效力仅限于该次登陆操作
# 如果想每次登录都拥有该环境变量，则需在对应配置文件内添加上述命令，配置文件作用看上面描述
export PATH="$PATH:/opt/bin"

# locale
# 用于打印用户语言相关的环境变量
locale

# set
# 用于打印所有本地环境变量
set
# env
# 用于打印用户所有的环境变量
env
# export -p用于显示当前所有环境变量
export -p
```

***28、编辑器-gedit/dedit***  
```sh
# gconf-editor
gedit '文档路径'

# dconf-editor
dedit '文档路径'
```

***29、反汇编-objdump/strings***  
```sh
# 反汇编目标文件或者可执行文件的命令 - objdump
# 将二进制文件变得可读的方式展现
objdump -T -C '.so/.a/可执行程序路径'

# 在对象文件或二进制文件中查找可打印的字符串 - strings
strings '.so/.a/可执行程序路径'
```

***30、电源指令-poweroff/shutdown/reboot/Hibernate/suspend/logout/rtcwake***  
&emsp;&emsp;首先，介绍计算机电源状态S1~S5:  

| 状态               | 含义            | 对应字段 |
| ----------------- | ---------------- | ---------------- |
| S1  | 普通待机模式(suspend)   | standby |
| S2  | 冻结I/O设备    | freeze  |
| S3  | 待机到内存     | mem     |
| S4  | 待机到硬盘-休眠(hibernate) | disk    |
| S5  | 关机(poweroff/shutdown)          | off     |

&emsp;&emsp;当前计算机支持哪些状态都可以在/sys/power/state查到:
```sh
# 查阅当前系统支持的休眠模式
cat /sys/power/state
freeze standby mem disk
```
&emsp;&emsp;想实现进入对应状态，可用以下指令:
```sh
# 进入S1(可直接输入 suspend)
echo standby > /sys/power/state
# 进入S2
echo freeze > /sys/power/state
# 进入S3
echo mem > /sys/power/state
# 进入S4(可直接输入 hibernate)
echo disk > /sys/power/state
# 进入S5(可直接输入 poweroff或shutdown)
echo off > /sys/power/state
```
&emsp;&emsp;想实现进入电源状态后定时开机，可以使用rtcwake命令:  
```sh
# -m 代表需要进入的状态
# -s 代表需要唤醒的时间
# -v 可以看到更多的打印信息
sudo rtcwake -m mem -s 20 -v
```

***31、键鼠输入事件监听-libinput***   
```sh
# 安装
sudo apt install libinput-tools

# 监听键鼠事件
sudo libinput debug-events
```

***32、窗口查看进程-xprop***  
```sh
# 打开xprop，点击想要查看详情的窗口
xprop
```

***33、多屏查询-xrandr***

***34、输入输出重定向***  
&emsp;&emsp;标准输出指的就是显示器，使用">",">>","2>","&>"能够重新控制输出的设备:
```sh
# ">" 代表覆盖写入，">>"代表追加写入
echo "字符串" > '文件路径'

# "2>" 代表错误重定向，即将输出到显示器的错误信息重新写入别的文件
# 执行以下命令后，会将搜索结果存放到前个文件中，错误信息存放到后个文件中
find / -name "字符串" > '搜索结果存放文件路径' 2> '错误信息存放文件路径'

# "&>" 代表将正确和错误的输出都写入某个文件
# 执行以下命令后，会将所有结果都存入文件
find / -name "字符串" &> '文件路径'
```
&emsp;&emsp;输入重定向，有一个从键盘获取信息存入文件的例子，不是很懂
```sh
cat > ok << EOF	#交互式
123
456
EOF		#结束符
cat ok
```
&emsp;&emsp;管道符用于将前一个命令的执行结果作为后一个命令的执行参数
```sh
# 最常见的用法
cat /etc/passwd |grep "查找字符串"

# 管道符经常配合xargs使用
# 因为很多命令不支持"|"管道符来传递参数，而xargs恰好能将管道或标准输入数据转换成命令行参数，比如:
find /sbin -perm +700 |ls -l       #这个命令是错误的
find /sbin -perm +700 |xargs ls -l   #这样才是正确的
```

***35、ssh免密码登录***  
```sh
# server1:
ssh-keygen  一直回车
ssh-copy-id root@192.168.200.202
# server2验证
cat ~/.ssh/authorized_keys  server1的公钥已添加
# server1
ssh root@192.168.200.202    无密码可登录
```

***36、计划任务-cron***  
```sh
# 符号含义
#     *	表示该范围内的任意时间
#     ,	表示间隔的多个不连续时间点，例如，“1,2,5,7,8,9”
#     -	表示一个连续的时间范围，例如“2-6”表示“2,3,4,5,6”
#     /	指定间隔的时间频率，例如“0-23/2”表示每两小时执行一次
# 示例：
#     0  17  *  *  1-5	周一到周五每天17:00

# 添加计划任务
# 第一次使用'-e'指令的时候会选择编辑器
# 打开后写上需要执行的指令即可
crontab -e -u '添加任务的用户名'

# 查看某用户的计划任务列表
crontab -l '添加任务的用户名'
```

***37、网络配置-nmcli***  
```sh
# 网络设备信息
# 可简写为nmcli d show/status
nmcli device show    # 详细信息
nmcli device status  # 粗略信息

# 网络连接信息
# 可简写为nmcli c show
nmcli connection show

# 网络设备开启/断开
nmcli device connect '设备名'     # 连接设备
nmcli device disconnect '设备名'  # 断开设备

# 网络连接启动/停止
nmcli connection up '连接配置名'    # 连接配置
nmcli connection down '连接配置名'  # 断开配置

# 添加网络连接配置
# type类型 ethernet以太网卡，con-name 配置文件名字，ifname 设备名字，connection.autoconnect自动连接，可加可不加，一般都加上
nmcli connection add type 'ethernet' con-name 'ens33' ifname 'ens33' connection.autoconnect 'yes'

# 修改网络连接配置
# +ipv4.dns代表添加一个备选的DNS地址
nmcli connection modify ens33 ipv4.method manual ipv4.addresses 192.168.200.201/24 ipv4.gateway 192.168.200.2 ipv4.dns 114.114.114.114 +ipv4.dns 20.106.0.20 connection.autoconnect yes

# 修改网络连接配置-一个网卡多添加一个ip地址
nmcli connection modify ens33 ipv4.method manual +ipv4.addresses 10.0.0.1/24

# 重启网络服务
systemctl restart NetworkManager

# 临时配置网络IP地址
# 用这个方法恢复 nmcli c down '连接配置名'，再次up
ifconfig '连接配置名' 192.168.200.201/24
```

### *0x04 Linux系统日志系统*
***常见日志文件解析***  

| 地址               | 功能            |
| ------------------ | ---------------- |
| /var/log/message  | 系统启动后的信息和错误日志 |
| /var/log/secure   | 与安全相关的日志信息                     |
| /var/log/maillog  | 与邮件相关的日志信息                     |
| /var/log/cron     | 与定时任务相关的日志信息               |
| /var/log/spooler  | 与UUCP和news设备相关的日志信息          |
| /var/log/boot.log | 守护进程启动和停止相关的日志消息   |
| /var/log/wtmp     | 永久记录每个用户登录、注销及系统的启动、停机的事件 |
| /var/run/utmp     | 记录当前正在登录系统的用户信息      |
| /var/log/btmp     | 记录失败的登录尝试信息                  |
| ~/.xession-error  | 记录登录桌面失败的信息                  |

***历史记录***  

| 命令                | 功能            |
| ------------------ | ---------------- |
| last `|` grep reboot | 查看重启的命令 |
| history            | 历史终端操作 |
| history -c         | 删除历史终端操作 |


***查看文件***  

| 命令                | 功能            |
| ------------------ | ---------------- |
| tail -f /var/log/*   | 实时查看那个文件 |
| cat /var/log/message | 查看那个文件 |
