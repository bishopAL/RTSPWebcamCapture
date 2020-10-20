# RTSPWebcamCapture
A RTSP webcam capture program
## 1. Environment
The programme requires python with opencv and tkinter. If you haven't installed any python interpreter, Anaconda is strongly recommaned. You may download it from https://www.anaconda.com.
After download and install Anaconda or python, you may have to install opencv package in terminal by:
```
pip install opencv-python
```
## 2. Usage
All usage can be obtained from webcam_detection.py. If you want to use USB camera, you may change it like:
```
webcam = WebcamApp(0)
```
If you want to use rtsp address, you may do it like:
```
webcam = WebcamApp('rtsp://admin:admin@192.168.10.183/11')
```
Replace it with your own ip address.
