import cv2
from tkinter import *
from PIL import Image, ImageTk
from threading import Thread
import numpy as np
import time


class WebcamApp:
    def __init__(self, address=0):
        # Tkinter Initialization
        self.windows_width = 1800
        self.windows_height = 1000
        self.resolution = [1440, 800]
        self.root = Tk()
        self.root.title('幕墙安全巡检机器人')
        self.root.geometry(str(self.windows_width)+'x'+str(self.windows_height))
        self.root.resizable(0, 0)
        self.startBtn = PhotoImage(file='./icon/start.png')
        self.snapBtn = PhotoImage(file='./icon/snap.png')
        self.stopBtn = PhotoImage(file='./icon/stop.png')
        self.quitBtn = PhotoImage(file='./icon/quit.png')
        self.mainPage_init()
        self.date = str(time.localtime(time.time()).tm_year) + '-' + str(time.localtime(time.time()).tm_mon) + '-' \
                    + str(time.localtime(time.time()).tm_mday) + ' ' + str(time.localtime(time.time()).tm_hour) + ':' \
                    + str(time.localtime(time.time()).tm_min) + ':' + str(time.localtime(time.time()).tm_sec)

        self.playOrPause = False  # True: play; False: pause
        self.updating_flag = False
        self.saveVideoFlag = False
        self.quit_flag = False
        self.connect2cam_flag = False

        # Thread Initialization
        t0 = Thread(target=self.webcam_read)
        t0.setDaemon(True)
        t0.start()
        t1 = Thread(target=self.updating_frame)
        t1.setDaemon(True)
        t1.start()

    def mainPage_init(self):
        self.mainPage = Frame(self.root, )
        self.mainPage.place(x=0, y=0, width=self.windows_width, height=self.windows_height, )
        # row 0 y=0:330
        self.movieLabel = Label(self.mainPage)
        self.movieLabel.place(x=self.resolution[0]/2+10, y=self.resolution[1]/2+10, anchor='center')
        current_image = Image.fromarray(np.zeros((self.resolution[1], self.resolution[0])))
        imgtk = ImageTk.PhotoImage(image=current_image)
        self.movieLabel.imgtk = imgtk
        self.movieLabel.config(image=imgtk)
        self.movieLabel.update()

        # row 1
        self.lb = Label(master=self.mainPage, text='摄像头IP地址：')
        self.lb.place(x=self.resolution[0]/2-130, y=900, anchor='center')
        v = StringVar(self.mainPage, value='rtsp://admin:admin@192.168.10.183/11')
        self.IP_entry = Entry(master=self.mainPage, textvariable=v)
        self.IP_entry.place(x=self.resolution[0]/2+10, y=900, width=270, anchor='center')
        self.connect2camButton = Button(master=self.mainPage, text='连接', command=self.connect2cam)
        self.connect2camButton.place(x=self.resolution[0]/2+260, y=900, anchor='center')

        # row 2
        self.captureVideoButton = Button(master=self.mainPage, image=self.startBtn, command=self.save_video)
        self.captureVideoButton.place(x=1530, y=300, anchor='center')
        self.captureVideoButton = Button(master=self.mainPage, image=self.stopBtn, command=self.stop_video)
        self.captureVideoButton.place(x=1670, y=300, anchor='center')
        self.captureButton = Button(master=self.mainPage, image=self.snapBtn, command=self.save_pic)
        self.captureButton.place(x=1530, y=500, anchor='center')
        self.quit_button = Button(master=self.mainPage, image=self.quitBtn, command=self.quit)
        self.quit_button.place(x=1670, y=500, anchor='center')

        # row 3
        self.start_label = Label(master=self.mainPage, text='开始录像')
        self.start_label.place(x=1530, y=380, anchor='center')
        self.stop_label = Label(master=self.mainPage, text='停止录像')
        self.stop_label.place(x=1670, y=380, anchor='center')
        self.snap_label = Label(master=self.mainPage, text='拍照')
        self.snap_label.place(x=1530, y=580, anchor='center')
        self.quit_label = Label(master=self.mainPage, text='退出')
        self.quit_label.place(x=1670, y=580, anchor='center')

        # row 4
        self.examine = Button(master=self.mainPage, text='查看', command=self.examine_init)
        self.examine.place(x=1600, y=730, anchor='center')
        self.project = Button(master=self.mainPage, text='项目', command=self.project_init)
        self.project.place(x=1600, y=780, anchor='center')

    def examine_init(self):
        self.playOrPause = False
        self.updating_flag = False
        self.mainPage.destroy()
        self.examinePage = Frame(self.root, )
        self.examinePage.pack()
        btn_back = Button(self.examinePage, text='查看返回', command=self.examinePage2mainPage)
        btn_back.pack()

    def examinePage2mainPage(self):
        self.examinePage.destroy()
        self.mainPage_init()
        self.playOrPause = True

    def project_init(self):
        self.playOrPause = False
        self.updating_flag = False
        self.mainPage.destroy()
        self.projectPage = Frame(self.root, )
        self.projectPage.pack()
        btn_back = Button(self.projectPage, text='项目返回', command=self.projectPage2mainPage)
        btn_back.pack()

    def projectPage2mainPage(self):
        self.projectPage.destroy()
        self.mainPage_init()
        self.playOrPause = True

    def pp_convert(self):
        if self.playOrPause:  # play -> pause
            self.playOrPause = not self.playOrPause
            self.GO_FLAG = False
        else:
            self.playOrPause = not self.playOrPause
            self.GO_FLAG = True

    def connect2cam(self):
        if not self.connect2cam_flag:
            # Webcam Initialization
            self.cap = cv2.VideoCapture(str(self.IP_entry.get()))
            ret, test_frame = self.cap.read()
            self.width = test_frame.shape[1]
            self.height = test_frame.shape[0]
            self.playOrPause = True
            self.connect2cam_flag = True
        else:
            self.cap.release()
            self.cap = cv2.VideoCapture(str(self.IP_entry.get()))
            ret, test_frame = self.cap.read()
            self.width = test_frame.shape[1]
            self.height = test_frame.shape[0]
            self.playOrPause = True
            self.connect2cam_flag = True

    def save_video(self):
        if self.connect2cam_flag:
            if not self.saveVideoFlag:
                self.date = str(time.localtime(time.time()).tm_year) + '-' + str(time.localtime(time.time()).tm_mon) + '-' \
                            + str(time.localtime(time.time()).tm_mday) + ' ' + str(
                    time.localtime(time.time()).tm_hour) + ':' \
                            + str(time.localtime(time.time()).tm_min) + ':' + str(time.localtime(time.time()).tm_sec)
                fourcc = cv2.VideoWriter_fourcc(*'H264')
                self.video = cv2.VideoWriter(self.date + '.avi', fourcc, 20.0, (self.width, self.height), True)
                self.saveVideoFlag = not self.saveVideoFlag
            else:
                pass
        else:
            print('请先点击连接以连接摄像头。')

    def stop_video(self):
        if self.saveVideoFlag:
            self.video.release()
            self.saveVideoFlag = not self.saveVideoFlag
        else:
            print("视频尚未开始录制，请先点击开始录像。")

    def save_pic(self):
        self.date = str(time.localtime(time.time()).tm_year) + '-' + str(time.localtime(time.time()).tm_mon) + '-' \
                    + str(time.localtime(time.time()).tm_mday) + ' ' + str(
            time.localtime(time.time()).tm_hour) + ':' \
                    + str(time.localtime(time.time()).tm_min) + ':' + str(time.localtime(time.time()).tm_sec)
        cv2.imwrite(self.date + '.jpg', self.frame)

    def quit(self):
        self.quit_flag = True
        self.root.destroy()

    def webcam_read(self):
        while not self.quit_flag:
            if self.playOrPause and self.connect2cam_flag:
                ret, temp_frame = self.cap.read()
                if ret:
                    self.frame = temp_frame
                    self.updating_flag = True

    def updating_frame(self):
        while not self.quit_flag:
            if self.updating_flag and self.playOrPause:
                if self.saveVideoFlag:
                    self.video.write(self.frame)
                img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
                current_image = Image.fromarray(img).resize((self.resolution[0], self.resolution[1]))
                imgtk = ImageTk.PhotoImage(image=current_image)
                self.movieLabel.imgtk = imgtk
                self.movieLabel.config(image=imgtk)
                self.movieLabel.update()


# webcam = WebcamApp(0)
webcam = WebcamApp()
webcam.root.mainloop()

