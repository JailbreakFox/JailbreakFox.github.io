---
title: PAM模块
date: 2020-09-21 14:22:17
tags: Linux
---

### *0x00 引言*
&emsp;&emsp;PAM(Pluggable Authentication Modules)是一个系统级用户认证框架，在Linux中进行身份或是状态的验证程序是由PAM来进行的。  
&emsp;&emsp;Linux-PAM使本地系统管理员可以随意选择程序的认证方式。换句话说，不用(重新编写)重新编译一个包含PAM功能的应用程序，就可以改变它使用的认证机制，这种方式下，就算升级本地认证机制,也不用修改程序。

### *0x01 PAM配置文件*
&emsp;&emsp;/etc/pam.d/目录专门用于存放 PAM 配置，用于为具体的应用程序设置独立的认证方式。应用程序通过调用相应配置文件的方式，从而调用本地的认证模块。

```sh
1 PAM配置文件简介
2 PAM配置内容格式
  2.1 模块类型
  2.2 控制标记
  2.3 模块路径
  2.4 模块参数
```

***1、PAM配置文件简介***  
&emsp;&emsp;system-auth文件是PAM模块的重要配置文件，它主要负责用户登录系统的身份认证工作，不仅如此，其他的应用程序或服务可以通过include接口来调用它（该文件是system-auth-ac的软链接）。此外password-auth配置文件也是与身份验证相关的重要配置文件，比如用户的远程登录验证(SSH登录)就通过它调用。而在Ubuntu、SuSE Linux等发行版中，PAM主要配置文件是common-auth、common-account、common-password、common-session这四个文件，所有的应用程序和服务的主要PAM配置都可以通过它们来调用。  
&emsp;&emsp;其他多以服务名来命名，比如/etc/pam.d/vsftpd，/etc/pam.d/login等。

***2、PAM配置内容格式***  
```sh
[root@centos6-test06 ~]# cat /etc/pam.d/sshd
#%PAM-1.0
auth       required     pam_sepermit.so
auth       include      password-auth
account    required     pam_nologin.so
account    include      password-auth
password   include      password-auth
# pam_selinux.so close should be the first session rule
session    required     pam_selinux.so      close
session    required     pam_loginuid.so
# pam_selinux.so open should only be followed by sessions to be executed in the user context
session    required     pam_selinux.so      open env_params
session    required     pam_namespace.so
session    optional     pam_keyinit.so      force revoke
session    include      password-auth
```
&emsp;&emsp;根据pam模块文件内容看，可以将pam配置文件分为四列:
- 第一列代表模块类型
- 第二列代表控制标记
- 第三列代表模块路径
- 第四列代表模块参数

***2.1、模块类型***  

| 管理方式 | 说明                                                                         |
| -------- | ------------------------------------------------------------------------------ |
| auth     | 表示鉴别类接口模块类型用于检查用户和密码，并分配权限 |
| account  | 表示账户类接口，主要负责账户合法性检查，确认帐号是否过期，是否有权限登录系统等 |
| session  | 会话类接口。实现从用户登录成功到退出的会话控制          |
| password | 口令类接口。控制用户更改密码的全过程，也就是有些资料所说的升级用户验证标记 |

***2.2、控制标记***  

| 控制标记 | 说明                                                                         |
| -------- | ------------------------------------------------------------------------------ |
| required     | 表示即使某个模块对用户的验证失败，也要等所有的模块都执行完毕后，PAM才返回错误信息。这样做是为了不让用户知道被哪个模块拒绝。如果对用户验证成功，所有的模块都会返回成功信息 |
| requisite  | 与required相似，但是如果这个模块返回失败，则立刻向应用程序返回失败，表示此类型失败，不再进行同类型后面的操作 |
| sufficient  | 表示如果一个用户通过这个模块的验证，PAM结构就立刻返回验证成功信息（即使前面有模块验证失败了，也会把失败结果忽略），把控制权交回应用程序。后面的层叠模块即使使用requisite或者required控制标志，也不再执行。如果验证是失败，sufficient与optional作用相同          |
| optional | 表示即使本行指定的模块验证失败，也允许用户接收应用程序提供的服务，一般返回PAM_IGNORE |
| include | 表示在验证过程中调用其他的PAM配置文件 |

***2.3、模块路径***  
&emsp;&emsp;即要调用模块的位置，比如/lib/security/、/lib64/security/

***2.4、模块参数***  
&emsp;&emsp;即传递给模块的参数，如果参数有多个，则中间用空格分开，如:open env_params

### *0x02 常用PAM模块*
| PAM模块        | 结合管理类型            | 说明                                                                                                               |
| ---------------- | ----------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| pam_unix.so      | auth                          | 提示用户输入密码,并与/etc/shadow文件相比对.匹配返回0                                              |
|                  | account                       | 检查用户的账号信息(包括是否过期等).帐号可用时,返回0.                                          |
|                  | password                      | 修改用户的密码. 将用户输入的密码,作为用户的新密码更新shadow文件                           |
| pam_shells.so    | auth/account                  | 如果用户想登录系统，那么它的shell必须是在/etc/shells文件中之一的shell                        |
| pam_deny.so      | auth/account/password/session | 该模块可用于拒绝访问                                                                                       |
| pam_permit.so    | auth/account/password/session | 模块任何时候都返回成功.                                                                                   |
| pam_securetty.so | auth                          | 如果用户要以root登录时,则登录的tty必须在/etc/securetty之中.                                        |
| pam_listfile.so  | auth/account/password/session | 访问应用程的控制开关                                                                                       |
| pam_cracklib.so  | password                      | 这个模块可以插入到一个程序的密码栈中,用于检查密码的强度.                                  |
| pam_limits.so    | session                       | 定义使用系统资源的上限，root用户也会受此限制，可以通过/etc/security/limits.conf或/etc/security/limits.d/*.conf来设定 |

### *0x03 PAM模块工作原理*
&emsp;&emsp;下面以/etc/pam.d/system-auth配置文件为例(system-auth是一个非常重要的pam配置文件，主要负责用户登录系统的认证工作。该文件是系统安全的总开关和核心的pam配置文件)，来说明PAM模块的工作原理。  

```sh
1 auth部分
2 account部分
3 password部分
4 session部分
```

下面是/etc/pam.d/system-auth文件的全部内容:
```sh
[root@centos6-test06 ~]# grep -v ^# /etc/pam.d/system-auth
auth        required      pam_env.so
auth        sufficient    pam_unix.so nullok try_first_pass
auth        requisite     pam_succeed_if.so uid >= 500 quiet
auth        required      pam_deny.so
 
account required          pam_unix.so
account sufficient        pam_succeed_if.so uid < 500 quiet
account required          pam_permit.so
 
password    requisite     pam_cracklib.so try_first_pass retry=3 type=
password    sufficient    pam_unix.so sha512 shadow nullok try_first_pass use_authtok
password    required      pam_deny.so
 
session     optional      pam_keyinit.so revoke
session     required      pam_limits.so
session     [success=1 default=ignore] pam_succeed_if.so service in crond quiet use_uid
session     required      pam_unix.so
```

***1、auth部分***  
&emsp;&emsp;当用户登录的时候，首先会通过auth类接口对用户身份进行识别和密码认证。所以在该过程中验证会经过几个带auth的配置项。  
&emsp;&emsp;第一步是通过pam_env.so模块来定义用户登录之后的环境变量， pam_env.so允许设置和更改用户登录时候的环境变量，默认情况下，若没有特别指定配置文件，将依据/etc/security/pam_env.conf进行用户登录之后环境变量的设置。  
&emsp;&emsp;第二步是通过pam_unix.so模块来提示用户输入密码，并将用户密码与/etc/shadow中记录的密码信息进行对比，如果密码比对结果正确则允许用户登录，而且该配置项的使用的是“sufficient”控制位，即表示只要该配置项的验证通过，用户即可完全通过认证而不用再去走下面的认证项。不过在特殊情况下，用户允许使用空密码登录系统，例如当将某个用户在/etc/shadow中的密码字段删除之后，该用户可以只输入用户名直接登录系统。  
&emsp;&emsp;第三步是通过pam_succeed_if.so对用户的登录条件做一些限制，表示允许uid大于500的用户在通过密码验证的情况下登录，在Linux系统中，一般系统用户的uid都在500之内，所以该项即表示允许使用useradd命令以及默认选项建立的普通用户直接由本地控制台登录系统。  
&emsp;&emsp;第四步是通过pam_deny.so模块对所有不满足上述任意条件的登录请求直接拒绝，pam_deny.so是一个特殊的模块，该模块返回值永远为否，类似于大多数安全机制的配置准则，在所有认证规则走完之后，对不匹配任何规则的请求直接拒绝。

***2、account部分***  
&emsp;&emsp;该部分的三个配置项主要表示通过account账户类接口来识别账户的合法性以及登录权限。  
&emsp;&emsp;第一步仍然使用pam_unix.so模块来声明用户需要通过密码认证。  
&emsp;&emsp;第二步承认了系统中uid小于500的系统用户的合法性。  
&emsp;&emsp;第三步对所有类型的用户登录请求都开放控制台。  

***3、password部分***  
&emsp;&emsp;该部分通过password口令类接口来确认用户使用的密码或者口令的合法性。  
&emsp;&emsp;第一步配置项表示需要的情况下将调用pam_cracklib来验证用户密码复杂度。如果用户输入密码不满足复杂度要求或者密码错，最多将在三次这种错误之后直接返回密码错误的提示，否则期间任何一次正确的密码验证都允许登录。需要指出的是，pam_cracklib.so是一个常用的控制密码复杂度的pam模块，关于其用法举例我们会在之后详细介绍。  
&emsp;&emsp;之后带pam_unix.so和pam_deny.so的两行配置项的意思与之前类似。都表示需要通过密码认证并对不符合上述任何配置项要求的登录请求直接予以拒绝。不过用户如果执行的操作是单纯的登录，则这部分配置是不起作用的。

***4、session部分***  
&emsp;&emsp;该部分主要将通过session会话类接口为用户初始化会话连接。  
&emsp;&emsp;第一步使用pam_keyinit.so表示当用户登录的时候为其建立相应的密钥环，并在用户登出的时候予以撤销。不过该行配置的控制位使用的是optional，表示这并非必要条件。  
&emsp;&emsp;第二步通过pam_limits.so限制用户登录时的会话连接资源，相关pam_limit.so配置文件是/etc/security/limits.conf，默认情况下对每个登录用户都没有限制。