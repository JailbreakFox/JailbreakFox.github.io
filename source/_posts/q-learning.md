---
title: Q-learning算法
tags: 强化学习，算法
date: 2018-11-26 20:41:00
grammar_cjkRuby: true
---

### *0x00 引言*
&emsp;&emsp; 强化学习是机器学习的一个分支，目前应用比较广泛的强化学习方法有AHC、TD以及Q-learning、sarsa、H-learning、DQN等<sup>[1]</sup>。
&emsp;&emsp;连接主义学习理论是心理学学习理论的一种，其将学习的方式分类为有监督学习、无监督学习和强化学习。
&emsp;&emsp;监督学习是人工标记输出,并反馈修改神经网络权值的学习方法。无监督学习需要机器对给定的输入自行聚类。而强化学习则是机器主动做出试探动作，并根据环境的反馈来修改行为的学习方式。
&emsp;&emsp;本文主要介绍在强化学习中使用最多的基础算法，即Q-learning。
### *0x01 Q-learning算法*
&emsp;&emsp;q-learning算法<sup>[2]</sup>包含两个最主要的概念，即状态S（state）和动作A（action），每次通过选择动作更新状态时，要同时按照图中的最优值函数Q计算公式更新Q表。其中参数α称为学习率，其决定这次的误差有多少是要被学习的, 且α是一个小于1 的数。γ为折扣率，是对未来 reward 的衰减值，值在[0,1]选择。
<div align=center>![q-learning](Q-learning.jpg)<div align=left>
&emsp;&emsp;在强化学习中，如果已经估计出最优值函数Q，则有三种动作选择方式<sup>[1]</sup>：贪婪动作选择策略（greedy）、ε-贪婪动作策略（ε-greedy）和softmax策略。第一种策略总是选择最高Q值的下步动作，第二种策略有ε的概率选择最高Q值，（1-ε）的概率任意选择动作，第三种策略根据各动作的Q值权重来选择动作。
&emsp;&emsp;在了解基础的算法以后，分析一个[实际问题](http://mnemstudio.org/path-finding-q-learning-tutorial.htm)<sup>[3]</sup>，例子描述了如何利用q-learning来学习未知环境并训练agent。
### *0x02 实例分析*
&emsp;&emsp;现在分析一下[莫烦视频](https://www.bilibili.com/video/av16921335/?p=6)<sup>[4]</sup>中的代码段，[代码](https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/blob/master/contents/1_command_line_reinforcement_learning/treasure_on_right.py)<sup>[5]</sup>可从github上获得。该例子的内容，是移动一个圆点，使其学会以最快的速度从左侧移动至右侧。
```python
def build_q_table(n_states, actions):
    table = pd.DataFrame(
        np.zeros((n_states, len(actions))),
        columns=actions,
    )
    return table
```
&emsp;&emsp;函数build_q_table旨在新建一个6行2列的Q值表，行代表状态，列代表左右移动。
```python
def choose_action(state, q_table):
    state_actions = q_table.iloc[state, :]
    if (np.random.uniform() > EPSILON) or ((state_actions == 0).all()): 
        action_name = np.random.choice(ACTIONS)
    else:
        action_name = state_actions.idxmax()
    return action_name
```
&emsp;&emsp;该例子采用ε-greedy策略来选择动作，choose_action即根据ε值选择下一步的实际动作，有90%的机率选择最大的Q值动作，其余10%的机率随机选择其他动作
```python
def get_env_feedback(S, A):
    if A == 'right': 
        if S == N_STATES - 2:
            S_ = 'terminal'
            R = 1
        else:
            S_ = S + 1
            R = 0
    else: 
        R = 0
        if S == 0:
            S_ = S 
        else:
            S_ = S - 1
    return S_, R
```
&emsp;&emsp;函数get_env_feedback的作用是假设按照已选择完成的动作行动，则下一状态的环境是否到达最左或最右，若是，则采取相应措施，若不是，则判断可安全执行。
```python
def rl():
    q_table = build_q_table(N_STATES, ACTIONS)
    for episode in range(MAX_EPISODES):
        step_counter = 0
        S = 0
        is_terminated = False
        update_env(S, episode, step_counter)
        while not is_terminated:

            A = choose_action(S, q_table)
            S_, R = get_env_feedback(S, A) 
            q_predict = q_table.loc[S, A]
            if S_ != 'terminal':
                q_target = R + GAMMA * q_table.iloc[S_, :].max()
            else:
                q_target = R 
                is_terminated = True 

            q_table.loc[S, A] += ALPHA * (q_target - q_predict)
            S = S_ 

            update_env(S, episode, step_counter+1)
            step_counter += 1
    return q_table
```
&emsp;&emsp;函数update_env是在搭建环境，这里不赘述。函数rl则是执行函数，循环做选择动作、判断环境、更新Q表以及实际运行动作的过程。
### *0x03 引用文献*
[1]强化学习方法及其应用研究
[2]https://morvanzhou.github.io/tutorials/machine-learning/reinforcement-learning/2-2-A-q-learning/
[3]http://mnemstudio.org/path-finding-q-learning-tutorial.htm
[4]https://www.bilibili.com/video/av16921335/?p=6
[5]https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/blob/master/contents/1_command_line_reinforcement_learning/treasure_on_right.py 