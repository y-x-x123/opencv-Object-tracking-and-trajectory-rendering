import cv2
import os

# 生成文件夹
def ensure_dir(dir_path):
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError:
            pass

#录制视频，并保存视频名为'video.mp4'
def videocapture():
    cap = cv2.VideoCapture(0)  # 生成读取摄像头对象
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取视频的宽度
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取视频的高度
    fps = cap.get(cv2.CAP_PROP_FPS)  # 获取视频的帧率
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))  # 视频的编码
    # 定义视频对象输出
    writer = cv2.VideoWriter("video.mp4", fourcc, fps, (width, height))
    while cap.isOpened():
        ret, frame = cap.read()  # 读取摄像头画面
        cv2.imshow('Frame', frame)  # 显示画面
        # 1秒24帧
        key = cv2.waitKey(24)
        writer.write(frame)  # 视频保存
        # 按Q退出
        if key == 27:
            break
    cap.release()  # 释放摄像头
    cv2.destroyAllWindows()  # 释放所有显示图像窗口

#间隔1秒保存一张图片并以jgp格式保存
def video2image(video_dir,save_dir):
    ensure_dir('./image/')
    cap = cv2.VideoCapture(video_dir) #生成读取视频对象
    n = 1   #计数
    fps = cap.get(cv2.CAP_PROP_FPS)    #获取视频的帧率
    i = 0
    timeF = int(fps)     #视频帧计数间隔频率
    while cap.isOpened():
        ret,frame = cap.read() #按帧读取视频
        #到视频结尾时终止
        if ret is False :
            break
        #每隔timeF帧进行存储操作
        if (n % timeF == 0) :
            i += 1
            print('正在保存第 %s 张图像' % i)
            save_image_dir = os.path.join(save_dir,'%s.jpg' % i)
            print('save_image_dir: ', save_image_dir)
            cv2.imwrite(save_image_dir,frame) #保存视频帧图像
        n = n + 1
        cv2.waitKey(1) #延时1ms
    cap.release() #释放视频对象

#图像直方图批量均衡化
def imageHist(path):
    for curDir, dirs, files in os.walk(path):
        for file in files:
            img=cv2.imread(path+file,1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #转灰度
            dst = cv2.equalizeHist(gray)  #直方图均衡化
            ensure_dir('./imhist/')  #创建文件夹
            cv2.imwrite('./imhist/'+file,dst) #保存处理过后的图片

if __name__ == '__main__':
    path='./image/'
    videocapture()
    video2image('video.mp4',path)
    imageHist(path)

