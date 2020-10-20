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
        self.mainPage_init()
        self.date = str(time.localtime(time.time()).tm_year) + '-' + str(time.localtime(time.time()).tm_mon) + '-' \
                    + str(time.localtime(time.time()).tm_mday) + ' ' + str(time.localtime(time.time()).tm_hour) + ':' \
                    + str(time.localtime(time.time()).tm_min) + ':' + str(time.localtime(time.time()).tm_sec)
        self.playOrPause = True  # True: play; False: pause
        self.updating_flag = False
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
        t1 = Thread(target=self.updating_frame)
        t1.setDaemon(True)
        t1.start()

    def mainPage_init(self):
        self.mainPage = Frame(self.root, )
        self.mainPage.pack()
        self.movieLabel = Label(self.mainPage)
        self.movieLabel.pack(padx=10, pady=10)
        self.examine = Button(master=self.mainPage, text='查看', command=self.examine_init)
        self.examine.pack()
        self.project = Button(master=self.mainPage, text='项目', command=self.project_init)
        self.project.pack()
        self.captureVideoButton = Button(master=self.mainPage, text='开始录像', command=self.save_video)
        self.captureVideoButton.pack()
        self.captureVideoButton = Button(master=self.mainPage, text='停止录像', command=self.stop_video)
        self.captureVideoButton.pack()
        self.captureButton = Button(master=self.mainPage, text='截图', command=self.save_pic)
        self.captureButton.pack()
        self.quit_button = Button(master=self.mainPage, text='退出', command=self.quit)
        self.quit_button.pack()

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
            pass

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
            if self.playOrPause:
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
                current_image = Image.fromarray(img).resize((540, 320))
                imgtk = ImageTk.PhotoImage(image=current_image)
                self.movieLabel.imgtk = imgtk
                self.movieLabel.config(image=imgtk)
                self.movieLabel.update()


webcam = WebcamApp(0)
# webcam = WebcamApp('rtsp://admin:admin@192.168.10.183/11')
webcam.root.mainloop()

