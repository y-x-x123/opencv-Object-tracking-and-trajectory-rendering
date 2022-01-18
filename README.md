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
其中Code2中测试结果视频为：videoResult_5.mp4和videoResult_6.mp4   可以直接查看
其中Code3中测试结果视频为：Result.mp4  可直接查看
代码窗口整合部分借鉴地址：
视频地址：https://www.youtube.com/watch?v=Fchzk1lDt7Q
代码地址：https://github.com/murtazahassan/OpenCV-Python-Tutorials-for-Beginners/blob/master/Intermediate/RealTime_Shape_Detection_Contours.py

