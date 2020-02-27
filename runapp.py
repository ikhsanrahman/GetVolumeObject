import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import numpy as np
import os
from sort_countour import sort_contours, draw_contour
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
serReadMass = serial.Serial('/dev/ttyACM1', 9600)
 
class App:
    def __init__(self, window, window_title, video_source=2):
        self.bluelow = 150
        self.greenlow = 150
        self.redlow = 240
        self.blueup = 255
        self.greenup = 255
        self.redup = 255

        self.lower = np.array([self.bluelow, self.greenlow, self.redlow])
        self.upper = np.array([self.blueup, self.greenup, self.redup])
        
        self.mass = None
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.volume = None
 
         # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width=840, height=640)
        self.canvas.pack()
        
        self.labelVol = tkinter.Label(window, text='Volume')
        self.labelVol.config(font=('helvetica', 10))
        self.labelVol.pack(anchor=tkinter.CENTER, expand=True)
        self.vol = tkinter.Entry (window)
        self.vol.pack(anchor=tkinter.CENTER, expand=True)

        # read mass of object
        self.labelMas = tkinter.Label(window, text='Object Mass')
        self.labelMas.config(font=('helvetica', 10))
        self.labelMas.pack(anchor=tkinter.CENTER, expand=True)
        self.mas = tkinter.Entry (window)
        self.mas.pack(anchor=tkinter.CENTER, expand=True)

        # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="Capture", width=50, command=self.capture)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        # Button that lets the user capture a image and get volume
        self.btn_vol=tkinter.Button(window, text="get volume", width=50, command=self.setVolume)
        self.btn_vol.pack(anchor=tkinter.CENTER, expand=True)

        # Button that lets the user get mass of object
        self.btn_mass=tkinter.Button(window, text="get mass", width=50, command=self.setMass)
        self.btn_mass.pack(anchor=tkinter.CENTER, expand=True)

        # start motor
        self.btn_startMotor=tkinter.Button(window, text="start", width=50, command=self.setStartMotor)
        self.btn_startMotor.pack(anchor=tkinter.CENTER, expand=True)

        # stop motor
        # self.btn_stopMotor=tkinter.Button(window, text="stop", width=50, command=self.setStopMotor)
        # self.btn_stopMotor.pack(anchor=tkinter.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.displayFrame()

        self.window.mainloop()

    def capture(self):
        # Get a frame from the video source
        ret, output_img, capture_img = self.vid.get_frame()
        ymax = 0
        ymin = 0
        xmax = 0
        xmin = 0
        center = 0

        if ret:
            cv2.imwrite("data/frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", capture_img)
            
            # self.mask = cv2.inRange(capture_img, self.lower, self.upper)
            # capture_img[np.where(self.mask==0)] = 0 #where the mask value is 0, make those coordinates black
            # capture_img[np.where(self.mask>100)] =255 #The target points, or the points which belong to the laser line are displayed in white
            # gray = cv2.cvtColor(capture_img, cv2.COLOR_BGR2GRAY)
            # gray = cv2.GaussianBlur(gray, (5, 5), 0)
            # kernel = np.ones((5,5), np.uint8) 
            # thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
            # thresh = cv2.erode(thresh, kernel, iterations=1)
            # thresh = cv2.dilate(thresh, kernel, iterations=1)

            # #finding the contours with RED colour
            # cnts, hierarchy  = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            
            # cnts, boundingBoxes = sort_contours(cnts, method='top-to-bottom')
            # for i, c in enumerate(cnts):
            #     result = draw_contour(capture_img, c, i)
            #     c=cnts[i]
            #     peri = cv2.arcLength(c, True)
            #     approx = cv2.approxPolyDP(c, 0.1 * peri, True)
            #     x , y , w, h = cv2.boundingRect(approx)
            #     cv2.drawContours(capture_img, [c], -1, (0, 255, 255), 1) #Draw all the contours with a red background
            #     cv2.rectangle(capture_img, (x,y), (x+w, y+h), (0,255,0),3)
            #     if i == 0:
            #         ymax = h
            #         cv2.putText(capture_img, "ymaxpix:" + str(h), (x + 10, y+10), cv2.FONT_HERSHEY_COMPLEX, .5, (0,255,0), 2)
                
            #     if i == 1:
            #         xmax = w
            #         cv2.putText(capture_img, "xmaxpix:" + str(w), (x + 30, y + 30), cv2.FONT_HERSHEY_COMPLEX, .5, (0,255,0), 2)
                
            #     if i == 3:
            #         center = w/2
            #         cv2.putText(capture_img, "xmaxpix:" + str(w/2), (x + 30, y + 30), cv2.FONT_HERSHEY_COMPLEX, .5, (0,255,0), 2)

            #     if i == 2:
            #         xmin = x
            #         cv2.putText(capture_img, "xminpix:" + str(x), (x + 10, y + 30), cv2.FONT_HERSHEY_COMPLEX, .5, (0,255,0), 2)
            #     if i == 4:
            #         ymin = y
            #         cv2.putText(capture_img, "yminpix:" + str(y), (x + 15, y + 40), cv2.FONT_HERSHEY_COMPLEX, .5, (0,255,0), 2)
            
            # width = ymax-ymin
            # length = xmax - xmin 
            # height = (center-xmax) * 0.5

            # self.volume = width * length * height

            cv2.imwrite("dataContour/frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", capture_img)

    def setVolume(self):
        volume = None
        self.vol.delete(0, 'end')
        if self.vid.start == True:
            volume = self.vid.readVolume()
            self.vol.insert(tkinter.END, str(volume))
            self.vol.pack()

        if volume:
            self.setMoveBigMotor()
        # self.canvas.create_window(200, 230, window=self.vol)

    def setStartMotor(self):
        self.vid.startMotor()

    def setStopMotor(self):
        self.vid.stopMotor()

    def setMass(self):
        self.mas.delete(0, 'end')
        self.mass = self.vid.readMass()
        # self.mass = self.mass.decode("utf-8").rstrip()
        self.mas.insert(tkinter.END, str(self.mass))
        self.mas.pack()
        # self.canvas.create_window(240, 240, window=self.mas)
        # return self.mass

    def setMoveBigMotor(self):
        self.vid.moveBigMotor()

    def displayFrame(self):
        # Get a frame from the video source
        ret, output_img, capture_img = self.vid.get_frame()
        output_img = cv2.resize(output_img, (840, 640))
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(output_img))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.window.after(self.delay, self.displayFrame)


class MyVideoCapture:
    def __init__(self, video_source=1):
        self.bluelow = 150
        self.greenlow = 150
        self.redlow = 240
        self.blueup = 255
        self.greenup = 255
        self.redup = 255

        self.start = False
        self.idMotorUp = 0

        self.mass = None
        self.lower = np.array([self.bluelow, self.greenlow, self.redlow])
        self.upper = np.array([self.blueup, self.greenup, self.redup])
        
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            ymax = 0
            ymin = 0
            center = 0
            xmax = 0
            xmin = 0
            while ret:
                self.mask = cv2.inRange(frame, self.lower, self.upper)
                output_img = frame.copy()
                capture_img = frame.copy()

                capture_img[np.where(self.mask==0)] = 0
                capture_img[np.where(self.mask>100)] = 255                

                gray_ = cv2.cvtColor(capture_img, cv2.COLOR_BGR2GRAY)
                gray_ = cv2.GaussianBlur(gray_, (5, 5), 0)

                kernel = np.ones((5,5), np.uint8)

                thresh_ = cv2.threshold(gray_, 45, 255, cv2.THRESH_BINARY)[1]
                thresh_ = cv2.erode(thresh_, kernel, iterations=1)
                thresh_ = cv2.dilate(thresh_, kernel, iterations=1)

                cnts_, hierarchy_  = cv2.findContours(thresh_.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

                for i, c in enumerate(cnts_):
                    c=cnts_[i]
                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.1 * peri, True)
                    x , y , w, h = cv2.boundingRect(approx)
                    cv2.drawContours(capture_img, [c], -1, (0, 255, 255), 1) #Draw all the contours with a red background
                
                #image with no rectangle of contour
                output_img[np.where(self.mask==0)] = 0
                output_img[np.where(self.mask>100)] = 255
                gray = cv2.cvtColor(output_img, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (5, 5), 0)

                thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
                thresh = cv2.erode(thresh, kernel, iterations=1)
                thresh = cv2.dilate(thresh, kernel, iterations=1)

                cnts, hierarchy  = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                
                cnts, boundingBoxes = sort_contours(cnts, method='top-to-bottom')
                        

                for i, c in enumerate(cnts):
                    result = draw_contour(output_img, c, i)
                    c=cnts[i]
                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.1 * peri, True)
                    x , y , w, h = cv2.boundingRect(approx)
                    cv2.drawContours(output_img, [c], -1, (0, 255, 255), 1) #Draw all the contours with a red background
                    cv2.rectangle(output_img, (x,y), (x+w, y+h), (0,255,0),3)
                    if i == 0:
                        ymin = h
                        cv2.putText(output_img, "yminpix:" + str(h), (x + 10, y+10), cv2.FONT_HERSHEY_COMPLEX, .5, (0,255,0), 2)
                    if i == 4:
                        ymax = y
                        cv2.putText(output_img, "ymaxpix:" + str(y), (x + 15, y + 40), cv2.FONT_HERSHEY_COMPLEX, .5, (0,255,0), 2)
                    if i == 3:
                        center = x+w/2
                        cv2.putText(output_img, "center:" + str(x+w/2), (x + 30, y + 30), cv2.FONT_HERSHEY_COMPLEX, .5, (0,255,0), 2)
                    if i == 1:
                        xmin = w
                        cv2.putText(output_img, "xminpix:" + str(w), (x + 30, y + 30), cv2.FONT_HERSHEY_COMPLEX, .5, (0,255,0), 2)
                    if i == 2:
                        xmax = x
                        length = xmax - xmin  
                        cv2.putText(output_img, "xmaxpix:" + str(x), (x + 10, y + 30), cv2.FONT_HERSHEY_COMPLEX, .5, (0,255,0), 2)

                width = ymax-ymin
                length = xmax - xmin 
                height = (center-xmax) * 0.5 # distance multiple tan teta

                self.volume = width * length * height

                return (ret, output_img, capture_img)

            else:
                return (ret, None)
        else:
            return (ret, None)

    def startMotor(self):
        #send signal to move camera
        self.start = True
        ser.write(b'0')
        
    def readVolume(self):
        if self.start == True:
            return self.volume
            self.start = False
        return None

    def readMass(self):
        # if self.start == True:
            time.sleep(0.3)
            while serReadMass.inWaiting() > 0:
                self.mass = serReadMass.readline()
            # BytesAvailable=ser.inWaiting()
            # SerialReadData=ser.readline(BytesAvailable)
            # self.mass = SerialReadData.decode("utf-8")
            # print(self.mass.decode("utf-8").rstrip())
            return self.mass
        # return None

    def stopMotor(self):
        #send signal to move camera
        self.start = False
        result = ser.write(b'1')

    def moveBigMotor(self):
        #majukan big stepper motor
        ser.write(b'2')
        time.sleep(3)
        #mundurkan big stepper motor
        ser.write(b'3')

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")

