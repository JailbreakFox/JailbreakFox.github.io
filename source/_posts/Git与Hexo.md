---
title: Git与Hexo
tags: 计算机技术
date: 2018-07-20 20:03:00
grammar_cjkRuby: true
---

### *0x00 引言*
&emsp;&emsp;记录一下我自己的[Git + Github搭建](https://www.cnblogs.com/liuxianan/p/build-blog-website-by-hexo-github.html)细节，顺便记录Git、Hexo与MarkDown的相关知识。
<div align=center>
<img src="git命令速查表.png" width = "700" height = "400" />
<div align=left>

### *0x01 Git*
&emsp;&emsp;Git是目前世界上最先进的分布式版本控制系统，其安装方法这里就不再赘述，主要介绍一些常用的指令。
```sh
1 配置
  1.1 用户与邮箱
  1.2 CRLF与LF
  1.3 SSH key
  1.4 添加远程仓库
2 远程主仓库、远程分仓库与本地仓库
  2.1 clone
  2.2 fork
  2.3 remote
3 分支推送
  3.1 add
  3.2 commit
  3.3 push
4 分支更新
  4.1 fetch
  4.2 pull
5 分支合并
  5.1 rebase
  5.2 merge
6 解决冲突
7 回溯
  7.1 本地修改清理
  7.2 查看历史
  7.3 版本回溯
8 打标签
9 堆栈暂存
10 清理历史记录
11 问责
12 提交拣取
13 工作区代码管理
14 常用操作命令
```
***1、配置***
*1.1、用户与邮箱*
```sh
#配置全局用户名与邮箱名，如果不是全局的则去掉--global
git config --global user.name "your name"
git config --global user.email "your email"

#查询当前用户名和邮箱
git config user.name
git config user.email
```
*1.2、CRLF与LF*  
&emsp;&emsp;CRLF, LF 是用来表示文本换行的方式，具体设置方式请查阅[CRLF与LF](https://jailbreakfox.github.io/2019/08/29/CRLF%E4%B8%8ELF/)。  

*1.3、SSH key*  
&emsp;&emsp;由于Git使用过程中直接传输帐号密码会不太安全，另外也很不方便(每次使用都要输帐号密码)，因此可以考虑为Git帐号添加SSH key。  

*1.4、添加远程仓库*  
&emsp;&emsp;默认clone下来的库，其名称均为origin，如果想重新给远程仓库起名字，则用以下代码:
```sh
git remote add <仓库名> <仓库地址>
#举例
git remote add upstream git@github.com:wuhan2020/wuhan2020.git
```

***2、远程主仓库、远程分仓库与本地仓库***  
&emsp;&emsp;我们创建的git仓库都是寄存在github服务器的，因此远程主仓库就是指某一项目最早被保存在github服务器内的哪个版本。有的时候我们需要多人合作，因此需要将主仓库fork下来，用于自行修改，但也保存在github服务器内，这种仓库叫做远程分仓库。  
*2.1、clone*  
&emsp;&emsp;克隆远程仓库可以用如下命令：
```sh
# 假设要克隆user1的myRepository仓库
git clone https://github.com/user1/myRepository.git
# 给你的远程仓库取名，可以使用"-o"参数
git clone "仓库地址" -o "仓库名"

# 远程仓库clone下来默认的仓库名是 origin ，可以用如下方式查看
git remote -v
# 输出如下
#origin https://github.com/user1/myRepository.git (fetch)
#origin https://github.com/user1/myRepository.git (push)
# 如果不喜欢这个名字，则可以删除重新添加
git remote rm origin
git remote add "仓库名" "仓库地址"
```
*2.2、fork*  
&emsp;&emsp;fork即所谓的派生远程主仓库，其过程如下图
<div align=center>
<img src="fork.png" width = "550" height = "350" />
<div align=left>

*2.3、remote*  
&emsp;&emsp;本地仓库的分支维护，需要用到remote方法:
```sh
# 查看所有分支信息
git branch –a

# 查看当前所有远程仓库名
git remote -v

# 查看关于远程的一些信息
git remote show '仓库名'

# 如果远程仓库已经删除了某些分支，但是本地仍然存在这些分支，可用以下命令删除干净
git remote prune '仓库名'
```

***3、分支推送***  
*3.2、commit*  
```sh
# -m参数可直接打提交名
git commit -m "提交名"
# 追加提交
# 如果远程仓库已经push了一次提交，然而并不满意又不想分成两次提交，--amend参数可在此次提交之上追加一次提交，并将两次提交合并。
git commit --amend
```
*3.3、push*  
&emsp;&emsp;向远程仓库推送本地仓库的代码，用如下命令：
```sh
# 完整的推送代码
# git push "远程主机名" "本地分支名":"远程分支名"
git push origin master:master

# 也可以省略远程分支名
# 如果同名远程分支存在则推送到该分支；如果该远程分支不存在，则该远程分支会被新建
git push origin master

# 如果省略本地分支，则代表删除该名远程分支
git push origin :master
```

***4、分支拉取***  
&emsp;&emsp;分支拉取方式由fetch与pull两种，他们的区别如下图:
<div align=center>
<img src="分支拉取.jpg" width = "550" height = "250" />
<div align=left>

*4.1、fetch*  
&emsp;&emsp;git fetch是将远程主机的最新内容拉到本地，用户在检查了以后决定是否合并到本地分支中。
```sh
#fetch更新，缺省参数相当于git fetch origin/master
git fetch
#取回更新后，会返回一个FETCH_HEAD
#输入以下代码检查区别
git log -p FETCH_HEAD
```

*4.2、pull*  
&emsp;&emsp;git pull是将远程主机的最新内容拉下来后直接合并，即：git pull = git fetch + git merge，这样可能会产生冲突，需要手动解决。
```sh
#pull更新，缺省参数相当于git pull origin/master
git pull
#其实际运行过程相当于
#git fetch origin/master
#git merge FETCH_HEAD

# 完整的拉取代码
# git pull "远程主机名" "远程分支名":"本地分支名"
git pull origin master:master
```

***5、分支合并***  
&emsp;&emsp;分支合并有rebase与merge两种方式。切记主分支内别用rebase，因为无法回溯到某个参与者提交的那次commit，[查阅博客](https://www.jianshu.com/p/4079284dd970)，有一个[网站](https://www.bilibili.com/video/av48190059)做了两者的使用实验。  
*5.1、rebase*  
&emsp;&emsp;rebase会把你当前分支的commit放到公共分支的最后面,所以叫变基。
<div align=center>
<img src="rebase.jpg" width = "400" height = "200" />
<div align=left>

```sh
# rebase
git pull --rebase "远程主仓库" "分支名"
# push到自己的fork仓库
git push "远程fork仓库" "分支名" -f
```

*5.2、merge*  
&emsp;&emsp;merge 会把公共分支和你当前的commit合并在一起，形成一个新的commit提交。
<div align=center>
<img src="merge.jpg" width = "400" height = "200" />
<div align=left>

*6、解决冲突*  
&emsp;&emsp;B站上有[大佬](https://www.bilibili.com/video/av48278991)已经很详细地讲述了解决冲突的两种办法。
*6.1、冲突文件内解决*  
&emsp;&emsp;解决冲突的时候可以先合并分支，这样如果两分支代码没有冲突就能直接合并，假如有冲突，就需要直接修改显示冲突的文件(其内部已经用一些符号显示冲突位置)。
```sh
# 先合并分支
git rebase/merge

# 如果分支有冲突，则修改显示所有冲突的文件
git diff .
# 或者单独显示某个文件
git diff "文件路径"
# 又或者显示某个文件与某个hash下的该文件差异
git diff "hash" "文件路径"

# 然后继续之前的合并命令
git rebase/merge --continue
```
```sh
# 如果分支有双方修改的冲突
# 可以选择全部接收对方的修改
git checkout --theirs
# 也可以全部接收自己的修改
git checkout --ours
```

*6.2、补丁文件显示冲突*  
&emsp;&emsp;打补丁的方法比前面一种显得更加简洁，在合并之前，先测试被合并分支打的patch。
```sh
# 切换到被合并的分支
# 制作一个补丁,N表示生成几个patch,默认是一笔commit一个patch
# "-N"代表需要打的补丁数量，默认为1
git format-patch -N

# 切换到需要合并的分支
# 打上补丁，PATCH_NAME为上步操作得到的patch名
git am PATCH_NAME

# 如果存在冲突，则会显示冲突补丁文件名
# 强制应用补丁，假如冲突补丁文件名为".git/rebase-apply/0001"
# 如果有冲突，则会显示出冲突内容
git apply --reject PATCH_NAME
# 可以打开冲突结果文件查看冲突内容
vim "冲突文件名".rej

# 可以用Vim打开此patch，并对比着修改冲突，Vim命令如下
:e PATCH_NAME
```

*7、回溯*  
*7.1、本地修改清理*  
```sh
# 放弃本地所有修改，代码与远程master一致
git fetch origin
git checkout master
git reset --hard origin/master
```  
*7.2、查看历史*  
```sh
# 每个提交在一行内显示
git log --oneline
# 在所有提交日志中搜索包含 [homepage] 的提交
git log --all --grep='homepage'
# 获取某人的提交日志
git log --author="xuyanghe"
```  
*7.3、本地版本回溯*  
```sh
# 获取所有操作历史
git reflog
# 重置到相应提交，回退一个版本
git reset HEAD@{1}
# 或者重置到某一提交版本
git reset --hard "提交的哈希值"
```  
*7.4、远程版本回溯*  
```sh
# 将版本回退提交到远程仓库
git reset HEAD@{1}
git push --force
```  

*8、打标签*  
&emsp;&emsp;版本号用于标记比较特殊的版本:
```sh
# 列出所有tag
git tag

# 为当前代码添加一个tag
git tag "tag名"
# 添加带备注的tag，-a参数后面跟tag名和提交的哈希值，-m参数后面跟tag备注
git tag -a "tag名" "提交的哈希值" -m "tag备注"
# 删除某个分支
git tag -d "tag名"

# 显示某一tag下的备注信息
git show "tag名"

# 推送某个标签
git push "仓库名" "tag名"
# 推送所有标签
git push origin --tags

# 切换到某个标签下的代码
git checkout "tag名"
```

*9、堆栈暂存*
&emsp;&emsp;stash命令可以将修改的内容保存至堆栈区:
```sh
# 保存至堆栈
git stash

# 列出堆栈中所有的存储内容
git stash list
# 显示堆栈中某次存储内容
git stash show stash@{"list中的num"}

# 从堆栈中得到存储内容(同时删除stash中的存储内容)
# 默认得到栈顶的存储
git stash pop stash@{"list中的num"}
# 从堆栈中得到存储内容(不删除stash中的存储内容)
git stash apply stash@{"list中的num"}

# 丢弃堆栈中某个存储内容
git stash drop stash@{"list中的num"}
# 丢弃堆栈中所有存储内容
git stash clear
```

*10、清理历史记录*  
&emsp;&emsp;.git文件会记录所有的提交历史，删除所有提交记录，可采用如下措施:
```sh
# 1.删除.git
rm -rf .git/
# 2.重新添加.git
git init
# 3.缓存所有文件
git add .
# 4.提交跟踪过的文件
git commit -m "add all again"
# 5.添加远程仓库链接
git remote add orgin "远程仓库名"
# 6.强制提交到远程master分支
git push -f orgin master:master
```

*11、问责*  
```sh
# 查询某个文件的修改历史事件
git blame "文件名"
```

*12、提交拣取*  
&emsp;&emsp;如果在B分支内想获取A分支的某些提交，则可以使用commit拣取 cherry-pick :
```sh
# 查询A分支下的某个提交hash值
# 例如查询结果为 0dedsaf

# 切换到B分支下
git cherry-pick "提交的hash值(0dedsaf)"
```

*13、工作区代码管理*  
```sh
# 添加已被跟踪文件的修改到这次commit中
git add .
git add '文件路径'

# 放弃此次已被跟踪文件的修改
git checkout .
git checkout '文件路径'

# 清理未被跟踪的所有文件及文件夹
git clean -df
```

*14、常用操作命令*  
```sh
# 创建分支
git branch "分支名"
# 删除分支
git branch -D "分支名"

# 切换分支
git checkout "分支名"
# 创建并切换分支
git checkout -b "分支名"

# 查看当前分支，"-a"参数能显示尽量具体的分支内容
git branch -a
# 更加详细的分支信息
git show-branch -a

# 查看提交历史
git log

# 查看历史提交信息
git show "提交hash值"
```

### *0x02 MarkDown*
&emsp;&emsp;Markdown是一种可以使用普通文本编辑器编写的标记语言，git博客的编辑语言默认为Markdown。这里记录一下与Markdown语言有关的一些教程。  
```sh
1 Linux-Atom下部署MarkDown
  1.1 下载MarkDown代码增强
  1.2
2 MarkDown基本语法
```

### *0x03 Hexo及主题*
&emsp;&emsp;Hexo提供了快速方便的一键部署功能，让您只需一条命令就能将网站部署到服务器上。  
```sh
1 Hexo命令
2 主题与配置
  2.1 Yilia
    2.1.1 安装与配置
    2.1.2
```
***1、Hexo命令***
&emsp;&emsp;这里记录几个Hexo常用的命令:
```sh
#---新建一个网站---
#如果没有设置文件夹爱，Hexo 默认在目前的文件夹建立网站
hexo init [folder]

#---新建一篇文章---
hexo new "文章名"

#---效果测试三连---
#清除缓存文件
hexo clean
#生成网站静态文件
#hexo generate
hexo g
#启动本地服务器
#hexo server
hexo s

#---自动生成网站静态文件，并部署到设定的仓库---
#hexo deploy
hexo d
```

***2、主题与配置***  
&emsp;&emsp;这里写一些我自己用的主题，以及其配置。  
*2.1、Yilia*  
*2.1.1、安装与配置*  
```sh
#---安装Yilia---
#并将其放入theme/文件夹下
git clone https://github.com/litten/hexo-theme-yilia.git
#---配置主题为Yilia---
#修改hexo根目录下的_config.yml为theme: yilia
#---修改Yilia的配置---
#修改themes/Yilia/_config.yml
#包括样式、图片等私人订制内容。如果有图片，放到/source/assets/下
```


### *0x04 Git与Hexo搭建博客*
```sh
1 Git安装与配置
  1.1 配置全局用户与邮箱
  1.2 新建github.io仓库
2 Nodejs与npm安装
3 Hexo安装与配置
```
***1、Git安装与配置***
&emsp;&emsp;Git安装方法这里就不再赘述，主要讲用于部署Hexo的配置。  
*1.1、配置全局用户与邮箱*  
&emsp;&emsp;由于将Hexo部署到Github过程中需要校验用户，因此请确保全局用户与邮箱配置正确(配置方法在0x00->1.1)。  
*1.2、新建github.io仓库*   
&emsp;&emsp;每个Github帐号能够申请一个github.io仓库，用于链接自己的博客主页。  
&emsp;&emsp; 需要注意的是，Repository name中必须输入[用户名].github.io，具体的操作如下图所示：  
<div align=center>
<img src="博客仓库.png" width = "600" height = "500" />
<div align=left>

***2、Nodejs与npm安装***  
&emsp;&emsp;Nodejs[安装方法](https://github.com/JailbreakFox/Ubuntu16.04-LTS-sh/blob/master/Ubuntu16.04配置sh包/Nodejs.sh)这里就不再赘述;npm是一款包管理工具，安装方法也不再赘述。  

***3、Hexo安装与配置***  
&emsp;&emsp;在安装完Node.js与npm之后，就可以很方便地安装Hexo了:
```sh
#安装Hexo
sudo npm install -g hexo

#将目标文件夹初始化为博客存放点
sudo hexo init

#修改权限
sudo chmod 777 -R 博客初始化文件夹

#直接三连，分别是清除、生成和部署
hexo clean
hexo g
hexo s

#登录 http://localhost:4000/ 查看效果
```

### ***0x05 引用文献***
