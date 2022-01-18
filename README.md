# 要求来自我的课程设计如下说明
基于计算机视觉技术的入侵检测通过设计图像处理方法实现对某一动态场景的实时观测，并在场景存在外来入侵情况时向上层管理系统发送入侵检测结果；要求独立编写具有以下功能模块的程序源码，
1．	通过手机/个人笔记本内置摄像机连续观测某一动态场景；
2．	获取摄像机实时视频流数据，并以一定时间间隔以jpg/bmp/png形式保存图片至本地；
3．	至少对图像进行一种预处理，如高斯平滑、直方图均衡化等；
4．	场景存在入侵时，检测入侵物体，显示入侵物体图像；
5．	至少以三种不同特征形式显示入侵物体，如沃罗诺伊图、边缘、角点等；
6．	显示物体在图像上的移动轨迹；
7．	预测物体的移动速度，精度不低于60%；
8．	将物体的属性信息，如形状、大小、移动速度等模拟发送至上层管理系统。

# 代码使用说明
# opencv-
使用python-opencv进行显示入侵物体与轨迹绘制 opencv-Object tracking and trajectory rendering
使用之前先安装以下库：
import cv2
import time
import datetime
from collections import deque
import math
import numpy as np
import os

Code1：录制视频并对提取视频帧并以png格式保存图片，对图片进行预处理（使用之前最好删除image和imhist文件夹）
Code2:  读取视频文件，检测入侵物体
Code3：调用摄像头实时检测入侵物体

课设结果录频：
其中Code2中测试结果视频为：运行代码即可查看结果
其中Code3中测试结果视频为：运行代码即可查看结果
代码窗口整合部分借鉴地址：
视频地址：https://www.youtube.com/watch?v=Fchzk1lDt7Q
代码地址：https://github.com/murtazahassan/OpenCV-Python-Tutorials-for-Beginners/blob/master/Intermediate/RealTime_Shape_Detection_Contours.py

