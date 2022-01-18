# -*- coding: utf-8 -*-
#导入库
import cv2
import time
import datetime
from collections import deque
import math
import numpy as np
import os

# 生成文件夹
def ensure_dir(dir_path):
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError:
            pass

#初始化追踪点的列表
mybuffer = 15
pts = deque(maxlen=mybuffer)

#打开摄像头，设置帧率为30
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)

#显示摄像头尺寸
print("width = %.2f" % (cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
print("height = %.2f" % (cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

avg = None


#拼接视频图像
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

#空列表方面储存入侵物体的各个数据
Point=[]     #储存入侵物体边缘轮廓点的个数
Areas=[]     #储存入侵物体边缘轮廓点的面积
Time=[]      #储存当前时间
Speed=[]     #储存入侵物体的速度
j=1
while (True):
    # 逐帧获取图像
    ret, frame = cap.read()
    if not ret:
        break
    # 对每帧图像进行操作
    img = cv2.resize(frame, (100, 100))  # 调整大小
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 变成灰色图像
    imgBlur = cv2.GaussianBlur(imgGray, (21, 21), 0)  # 高斯滤波

    if avg is None:
        avg = imgBlur.copy().astype("float")
        continue
    cv2.accumulateWeighted(imgBlur, avg, 0.5)
    # 计算当前帧与第一帧的区别
    frameDelta = cv2.absdiff(imgBlur, cv2.convertScaleAbs(avg))
    # 填充孔洞
    thresh = cv2.threshold(frameDelta, 35, 240, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    # 查找轮廓
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    #显示文字各个窗口表示的信息
    cv2.putText(frame, "Track and Outline", (10, 25),
                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
    cv2.putText(thresh, "thresh", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
    cv2.putText(imgGray, "imgGray", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
    cv2.putText(imgBlur, "imgBlur", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
    # pts.clear()

    #如果有轮廓
    if len(contours)>0:
        c = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(c)
        imgRGB = frame.copy()
        Areas.append(area)    #储存入侵物体面积
        # 计算轮廓的边界框，在当前帧中画出该框
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.drawContours(frame, c, -1, (255, 0, 255), 7)
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        Point.append(len(approx))       #储存入侵物体边缘点个数
        x, y, w, h = cv2.boundingRect(approx)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)

         # 初始化物体的轮廓质心
        center = None
        # 计算轮廓的矩
        M = cv2.moments(c)
        # 计算质心
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # 把质心添加到pts中，并且是添加到列表左侧
        pts.appendleft(center)

        imgcrop=imgGray[y:(y + h), x:(x + w)]

        imgRGB=imgRGB[y:(y + h), x:(x + w),:]

        # path = './imgRGB/'
        # ensure_dir(path)
        # cv2.imwrite(os.path.join(path, '%s.jpg' % j),imgRGB) #保存视频帧图像
        # j=j+1
        # Canny边缘检测，角点提取
        imgCanny = cv2.Canny(imgcrop, 23, 20)
        dst = cv2.cornerHarris(imgcrop, 2, 23, 0.04)
        imgRGB[dst > 0.01 * dst.max()] = [0,0,255]
        # 实时显示入侵物体角点和Canny边缘检测窗口
        cv2.imshow('corners', imgRGB)
        cv2.imshow('imgCanny',imgCanny)
        #储存当前时间
        nowTime=datetime.datetime.now()
        Time.append(str(nowTime))

    # 遍历追踪点，分段画出轨迹
    for i in range(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue
        # 画出小线段
        cv2.circle(frame,pts[i], 5, (255,255,0), -1)
        cv2.line(frame, pts[i - 1], pts[i], (255,255,0), 2)
        p1, p2 = pts[i - 1], pts[i]
        if len(contours)==0:
            print('当前时间为：',datetime.datetime.now(),' 速度： 0 cm/s')
            Speed.append(0)
        else:
            speed=round(math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))/64,1)
            print('当前时间为：{} 速度: {} cm/s'.format(datetime.datetime.now(),speed))
            Speed.append(speed)
            cv2.putText(frame, "Speed: " + str(speed) + " cm/s", (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 1)
            cv2.putText(frame, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
                        (0, 255, 0), 2)
            cv2.putText(frame, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)
    # cv2.imshow('Frame',frame)
    cv2.imshow('Result', stackImages(0.8, ([frame, thresh],[imgGray,imgBlur])))
#按‘esc’键退出
    if cv2.waitKey(1) & 0xFF == 27:
        break

#销毁窗口
cap.release()
cv2.destroyAllWindows()

#模拟上传上层管理系统（将入侵物体入侵的时间，边角点个数以及面积大小写入文本）
#写入文件
f=open("入侵日志.txt","w") #创建文件
f.writelines('---------------入侵日志-----------------')
f.writelines('\n')
for i in range(len(Time)):
    f.writelines('时间：'+str(Time[i])+'  边角点个数：'+str(Point[i])\
                 +'  面积：'+str(Areas[i])+' 速度：'+str(Speed[i])+' cm/s'+'\n')






