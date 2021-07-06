---
title: Linux进程防杀
tags: 计算机技术，Linux
date: 2021-07-05 17:22:14
grammar_cjkRuby: true
---

### *0x00 引言*
&emsp;&emsp;本文主要研究Linux下如果防止进程被kill的方法。  
&emsp;&emsp;系统实现杀死进程一般是通过调用 kill(或tkill、pkill) 来终止进程（内核也可以自行终止进程，如 Ctrl-C 时发送的 SIGINT 或内存不足杀手发送的 SIGKILL。某些信号可能是其他系统调用如 ptrace的结果)。  
&emsp;&emsp;当 kill 被调用时，这一切都发生在内核中。如果要实现进程防杀，只有使内核代码介于发送信号的进程和接收信号的进程之间。  
&emsp;&emsp;Linux系统下，要实现系统防杀可以从[两个角度](https://unix.stackexchange.com/questions/483913/is-there-a-way-to-prevent-sigkill-to-reach-a-process)<sup>[1]</sup>考虑，控制接收kill流程与控制被kill进程的状态。

### *0x01 控制接收kill流程*
```
1 LD_PRELOAD注入程序
  1.1 简单使用
  1.2 防止递归调用
  1.3 进程防杀示例
2 其他方法
```

***1、LD_PRELOAD注入程序***  
&emsp;&emsp;这里主要叙述的是[LD_PRELOAD注入程序](https://rafalcieslak.wordpress.com/2013/04/02/dynamic-linker-tricks-using-ld_preload-to-cheat-inject-features-and-investigate-programs/)<sup>[2]</sup>这个方法。如果杀手进程是链接动态库的，就可以通过修改LD_PRELOAD(是个环境变量，用于动态库的加载)注入拒绝杀死指定PID的代码，并替换 kill 系统调用(您可能需要对 tkill或pkill执行相同的操作，具体取决于杀手实际发送信号的方式)。  
***1.1、简单使用***  
&emsp;&emsp;首先写一个任意生成十个数字random.cpp文件(注意进程可以用.cpp或.c做后缀):
```c++
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
 
int main(){
  srand(time(NULL));
  int i = 10;
  while(i--) printf("%d\n",rand()%100);
  return 0;
}
```
&emsp;&emsp;然后进行编译:
```sh
gcc random.cpp -o random
```
&emsp;&emsp;然后写一个用于注入为动态库的源文件unrandom.c文件(*注意进程不可以用.cpp做后缀，必须用.c，原因未知):
```c++
int rand(){
    return 42;
}
```
&emsp;&emsp;然后生成动态库:
```sh
gcc -shared -fpic unrandom.c -o unrandom.so
```
&emsp;&emsp;然后执行如下命令，发现生成随机数均为42，且已经链接到unrandom.so上了
```sh
# 方法一
$ LD_PRELOAD=$PWD/unrandom.so ./random
# 可以观察链接的库
LD_PRELOAD=$PWD/unrandom.so ldd random

# 方法二
$ export LD_PRELOAD=$PWD/unrandom.so
$ ./random
# 可以观察链接的库
ldd random
```

***1.2、防止递归调用***  
&emsp;&emsp;假如我们要封装一个open函数的动态库，很明显open函数将被递归调用:
```sh
int open(const char *pathname, int flags){
  return open(pathname,flags);
}
```
&emsp;&emsp;我们将使用dlfcn.h的dlsym函数来解决递归问题，修改后的注入源码如下:
```c++
#define _GNU_SOURCE // 指示编译器启用一些非标准
#include <dlfcn.h>
#include <stdio.h>

// 函数指针
typedef int (*orig_open_f_type)(const char *pathname, int flags);

int open(const char *pathname, int flags, ...)
{
    // 此处可加注入的程序
    printf("The victim used open(...) to access '%s'!!!\n", pathname); 

    orig_open_f_type orig_open;
    // RTLD_DEFAULT是在当前库中查找函数，而RTLD_NEXT则是在当前库之后查找第一次出现的函数
    orig_open = (orig_open_f_type)dlsym(RTLD_NEXT, "open");
    return orig_open(pathname,flags);
}
```
&emsp;&emsp;然后生成动态库(注意使用dlsym需要添加 '-ldl' 编译属性):
```sh
gcc -shared -fpic injectopen.c -o injectopen.so -ldl
```
&emsp;&emsp;新建一个调用open()函数的.cpp源文件:
```c++
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>

int main(int argc, char *argv[])
{
    int fd;

    if(2 != argc) {
        printf("Usage: ./opener + 'file path' \n");
        return 1;
    }

    errno = 0;
    fd = open(argv[1], O_RDONLY | O_CREAT, S_IRWXU);

    if(-1 == fd) {
        printf("open() failed with error [%s]\n",strerror(errno));
        return 1;
    } else {
        printf("open() Successful.\n");
    }

    return 0;
}
```
&emsp;&emsp;然后进行编译:
```sh
gcc opener.cpp -o opener
```
&emsp;&emsp;注入与不注入动态库的输出结果如下:
```sh
# 注入动态库
$ ./opener test.md
open() Successful.

# 不注入动态库
$ LD_PRELOAD=$PWD/inspect_open.so ./opener test.md
The victim used open(...) to access 'test.md'!!!
open() Successful.
```

***1.3、进程防杀示例***  
&emsp;&emsp;接下来记录一个完整的[防杀示例](https://www.52coder.net/post/ld-preload)<sup>[3]</sup>，能够记录下杀手进程终端、杀手进程、被杀进程的详细信息。首先，实现注入进程的源码injectkill.c :
```c++
#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <dlfcn.h>

typedef int (*KILL)(pid_t pid, int sig);

#define TMP_BUF_SIZE 256

/* 获取进程命令行参数 */
void get_cmd_by_pid(pid_t pid, char *cmd)
{
    char buf[TMP_BUF_SIZE];
    int i = 0;

    snprintf(buf, TMP_BUF_SIZE, "/proc/%d/cmdline", pid);
    FILE* fp = fopen(buf, "r");
    if(fp == NULL)
        return;

    memset(buf, 0, TMP_BUF_SIZE);
    size_t ret = fread(cmd, 1, TMP_BUF_SIZE - 1, fp);

    for (i = 0; ret != 0 && i < ret - 1; i++) {
        if (cmd[i] == '\0')
            cmd[i] = ' ';
    }

    fclose(fp);
    cmd[TMP_BUF_SIZE - 1] = '\0';
}

int kill(pid_t pid, int sig)
{
    static KILL orign_kill = NULL;

    //接收kill命令的进程信息
    char buf_des[TMP_BUF_SIZE] = {0};
    get_cmd_by_pid(pid, buf_des);

    //获取当前进程信息
    char buf_org[TMP_BUF_SIZE] = {0};
    get_cmd_by_pid(getpid(), buf_org);

    //获取父进程信息
    char buf_porg[TMP_BUF_SIZE] = {0};
    get_cmd_by_pid(getppid(), buf_porg);

    printf("hook kill(sig:%d): [%s(%d) -> %s(%d)] -> [%s(%d)]\n",
           sig, buf_porg, getppid(), buf_org, getpid(), buf_des, pid);
out:
    if(!orign_kill)
        orign_kill = (KILL)dlsym(RTLD_NEXT, "kill");

    return orign_kill(pid, sig);
}
```
&emsp;&emsp;然后生成动态库(注意使用dlsym需要添加 '-ldl' 编译属性):
```sh
gcc -shared -fpic injectkill.c -o injectkill.so -ldl
```
&emsp;&emsp;为了验证kill注入程序有起到作用，需要先写一个被杀的进程killed.cpp:
```c++
#include<stdio.h>
#include<signal.h>
#include<unistd.h>

void sig_handler(int signo)
{
  if (signo == SIGINT)
    printf("received SIGINT\n");
}

int main(void)
{
  if (signal(SIGINT, sig_handler) == SIG_ERR)
  printf("\ncan't catch SIGINT\n");

  while(1)
    sleep(1);
  return 0;
}
```
&emsp;&emsp;然后进行编译:
```sh
gcc killed.cpp -o killed
```
&emsp;&emsp;最后来验证一下注入效果:
```sh
# 运行被杀进程
$ ./killed

# 观察被杀进程PID
$ ps -ef |grep killed
xyh        9169   8440  0 13:53 pts/8    00:00:00 ./killed

# 运行kill / pkill / tkill方法
# 可观察到杀手进程是bash(9118)下运行的kill(9173)，被杀进程是killed(9169)
$ LD_PRELOAD=$PWD/injectkill.so /bin/kill 9169
hook kill(sig:15): [-bash(9118) -> /bin/kill 9169(9173)] -> [./killed(9169)]
```

***2、其他方法***  
&emsp;&emsp;如果是为了防止一个关键进程(例如一个用于支持根文件系统的进程)在关机时被杀死，大多数 init 系统将有一种方法来防止给定的进程受到 killall5 或类似功能的影响。参见某些版本的 Debian 中的 /run/sendsigs.omit.d，或者例如 systemd 的 killmode。  
&emsp;&emsp;要杀死进程，无论如何都必须确定要杀死哪个进程。如果它基于存储在文件中的受害者的 PID(如 /run/victim.pid)，那么可以更改该文件，如果它基于进程名称(/proc/pid/task/tid/comm)，那么也可以更改(例如通过附加调试器并调用 prctl(PR_SET_NAME))，对于 arg 列表(ps -f 显示的 /proc/pid/cmdline)也是如此。 

### *0x02 控制被kill进程状态*
&emsp;&emsp;还可以从被kill进程的状态角度出发来实现防杀。  
```
1 简单的Unix权限
2 基础知识构建
3 源码打包方法
4 非源码打包方法
```
***1、简单的Unix权限***  
&emsp;&emsp;引用 Linux 上的 kill(2) 手册页：
```sh
一个进程要有发送信号的权限，它要么是有root用户（Linux下：在目标进程的用户命名空间中具有CAP_KILL能力），要么发送进程的真实或有效用户ID必须等于真实或保存的目标进程的 set-user-ID。

# 实际实现方法
以与杀手进程不同的用户身份运行被杀死的进程（假设杀手不是以 root 身份运行）
```

***2、Linux安全模块***  
```sh
LSM 可以（至少对 Smack、SELinux 和 apparmor 可以）过滤可能向什么发送信号的内容。

# 实际实现方法
使用 LSM。 例如，当使用 Smack（以 security=smack 作为内核参数启动）时，为受害进程设置不同的标签就足以让其他进程无法看到它，更不用说杀死它了。
sudo zsh -c 'echo unkillable > /proc/self/attr/current && exec sleep 1000'
上述操作会在unkillable域中运行 sleep（名称可以是任何东西，关键是目前没有定义的规则允许以任何方式干扰该域），甚至以相同 uid 运行的进程也无法杀死它，root用户也一样。
```

***3、一些进程对杀戮免疫***  
```sh
Linux上id为1（init）的进程就是这种情况。其他子命名空间的根进程也不受其命名空间中其他进程发送的信号的影响。内核任务也不受信号影响。

# 实际实现方法
# 以终端为例
$ sudo unshare -p --fork --mount-proc zsh
$ kill -s KILL "$$"
```

***4、内核检测机制(未仔细研究)***  
&emsp;&emsp;还有类似于 SystemTap 使用的内核检测机制，它允许您影响内核的行为，在这里可以用来劫持信号传递。
```sh
SystemTap 可以在这里使用。 但是请注意，您需要内核符号（Debian 上的 linux-image-<version>-dbgsym）才能使用它，并且 SystemTap 或您的 stap 脚本将挂钩的内部内核函数可能会发生变化。 所以可能不是最稳定的选择。 Guru 模式也应该小心使用（不要尝试做任何太花哨的事情）。
使用 stap，您可以在正在运行的内核中的不同点注入代码。 例如，您可以挂钩处理 kill() 或 tkill() 系统调用的内核函数，并告诉它当 pid 是您的受害者时将信号更改为 0（无害）。
stap -ge 'probe kernel.function("sys_kill") { if ($pid == 12345) $sig = 0; }'
（这里对于任何信号，如果您只想覆盖 SIGKILL，您也可以检查 $sig == 9）。 现在，当使用 tkill() 或使用受害者的进程组 ID 调用 kill() 时，这不起作用，因此我们需要扩展它。 这不包括信号由内核本身发送的情况。
但是我们也可以查看内核代码，看看我们是否可以在内核检查发送信号权限的地方钩住自己。
stap -ge 'probe kernel.function("check_kill_permission").return {
           if (@entry($t->pid) == 12345) $return = -1; }'
我们返回 -1 (-EPERM) ，当请求的 pid 是我们目标的 pid 时（这里以 12345 为例），它还有一个好处是让杀手知道它的 kill() 失败了。
~$ sleep 1000 &
[1] 8508
~$ sudo stap -ge 'probe kernel.function("check_kill_permission").return {
  if (@entry($t->pid) == '"$!"') $return = -1; }' &
[2] 8510
~$ kill -s KILL 8508
kill: kill 8508 failed: operation not permitted
它也适用于内核自行发送信号的某些情况，但不是全部。 为此，我们需要深入到内核代码中进行信号传递的最底层函数：__send_signal()（至少在当前版本的 Linux 内核中）。
一种方法是挂钩 __send_signal() 在开始时调用的 prepare_signal() 函数（如果返回 0 则退出）；
stap -ge 'probe kernel.function("prepare_signal").return {
  if (@entry($p->pid) == 12345) $return = 0; }'
然后，只要该 stap 进程存在，pid 12345 将是不可杀死的。
请注意，内核通常假设 SIGKILL 会起作用，因此在某些极端情况下，上述内容可能会产生意想不到的副作用（例如，如果 oom-killer 继续选择无法杀死的受害者，则它会变得无效）。
```

### *0x03 引用文献*
[1]https://unix.stackexchange.com/questions/483913/is-there-a-way-to-prevent-sigkill-to-reach-a-process
[2]https://rafalcieslak.wordpress.com/2013/04/02/dynamic-linker-tricks-using-ld_preload-to-cheat-inject-features-and-investigate-programs/
[3]https://www.52coder.net/post/ld-preload