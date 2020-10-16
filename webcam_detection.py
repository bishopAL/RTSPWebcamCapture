import cv2
from tkinter import *
from PIL import Image, ImageTk
from threading import Thread
import time


class WebcamApp:
    def __init__(self, address=0):
        # Tkinter Initialization
        self.root = Tk()
        self.root.title('Webcam')
        self.movieLabel = Label(self.root)
        self.movieLabel.pack(padx=10, pady=10)
        self.playOrPauseButton = Button(master=self.root, text='暂停/播放', command=self.pp_convert)
        self.playOrPauseButton.pack()
        self.captureVideoButton = Button(master=self.root, text='开始/停止录像', command=self.save_video)
        self.captureVideoButton.pack()
        self.captureButton = Button(master=self.root, text='截图', command=self.save_pic)
        self.captureButton.pack()
        self.quit_button = Button(master = self.root, text='退出', command=self.quit)
        self.quit_button.pack()
        self.date = str(time.localtime(time.time()).tm_year) + '-' + str(time.localtime(time.time()).tm_mon) + '-' \
                    + str(time.localtime(time.time()).tm_mday) + ' ' + str(time.localtime(time.time()).tm_hour) + ':' \
                    + str(time.localtime(time.time()).tm_min) + ':' + str(time.localtime(time.time()).tm_sec)
        self.playOrPause = True  # True: play; False: pause
        self.GO_FLAG = False
        self.saveVideoFlag = False
        self.quit_flag = False

        # Webcam Initialization
        self.cap = cv2.VideoCapture(address)
        ret, test_frame = self.cap.read()
        self.width = test_frame.shape[1]
        self.height = test_frame.shape[0]
        # Thread Initialization
        t0 = Thread(target=self.webcam_read)
        t0.setDaemon(True)
        t0.start()

    def webcam_read(self):
        while 1:
            if self.playOrPause:
                ret, self.frame = self.cap.read()
                self.GO_FLAG = True

    def pp_convert(self):
        if self.playOrPause:  # play -> pause
            self.playOrPause = not self.playOrPause
            self.GO_FLAG = False
        else:
            self.playOrPause = not self.playOrPause
            self.GO_FLAG = True

    def save_video(self):
        if not self.saveVideoFlag:
            self.date = str(time.localtime(time.time()).tm_year) + '-' + str(time.localtime(time.time()).tm_mon) + '-' \
                        + str(time.localtime(time.time()).tm_mday) + ' ' + str(
                time.localtime(time.time()).tm_hour) + ':' \
                        + str(time.localtime(time.time()).tm_min) + ':' + str(time.localtime(time.time()).tm_sec)
            fourcc = cv2.VideoWriter_fourcc(*'H264')
            self.video = cv2.VideoWriter(self.date + '.avi', fourcc, 20.0, (self.width, self.height), True)
            self.saveVideoFlag = not self.saveVideoFlag
        else:
            self.video.release()
            self.saveVideoFlag = not self.saveVideoFlag

    def save_pic(self):
        self.date = str(time.localtime(time.time()).tm_year) + '-' + str(time.localtime(time.time()).tm_mon) + '-' \
                    + str(time.localtime(time.time()).tm_mday) + ' ' + str(
            time.localtime(time.time()).tm_hour) + ':' \
                    + str(time.localtime(time.time()).tm_min) + ':' + str(time.localtime(time.time()).tm_sec)
        cv2.imwrite(self.date + '.jpg', self.frame)

    def quit(self):
        self.quit_flag = True
        self.root.destroy()


webcam = WebcamApp(0)
# webcam = WebcamApp('rtsp://admin:admin@192.168.10.183/11')

while not webcam.quit_flag:
    if webcam.GO_FLAG:
        if webcam.saveVideoFlag:
            webcam.video.write(webcam.frame)
        img = cv2.cvtColor(webcam.frame, cv2.COLOR_BGR2RGBA)
        current_image = Image.fromarray(img).resize((540, 320))
        imgtk = ImageTk.PhotoImage(image=current_image)
        webcam.movieLabel.imgtk = imgtk
        webcam.movieLabel.config(image=imgtk)
        webcam.movieLabel.update()
