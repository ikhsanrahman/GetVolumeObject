import cv2
import numpy as np 
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the input image")
# ap.add_argument("-m", "--method", required=True, help="Sorting method")
args = vars(ap.parse_args())

data = cv2.imread(args["image"])

bluelow = 150
greenlow = 150
redlow = 240
blueup = 255
greenup = 255
redup = 255


lower = np.array([bluelow,greenlow,redlow]) #lower limit of BGR values of the laser line
upper= np.array([blueup,greenup,redup]) #upper limit of BGR values of the laser line
mask = cv2.inRange(data, lower, upper) #create a mask within the specified values of RED
output_img = data.copy() #a copy of the main frame is created
output_img[np.where(mask==0)] = 0 #where the mask value is 0, make those coordinates black
output_img[np.where(mask>100)] =255 #The target points, or the points which belong to the laser line are displayed in white
gray = cv2.cvtColor(output_img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)

thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.erode(thresh, None, iterations=1)
thresh = cv2.dilate(thresh, None, iterations=1)

#finding the contours with RED colour
cnts, hierarchy  = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if imutils.is_cv2() else cnts[1]
print (cnts)
print(len(cnts))
for i in range(len(cnts)):
	c=cnts[i]
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	x , y , w, h = cv2.boundingRect(approx)
	print('x', x, 'y', y, 'w', w, 'h', h,  'i', i)

	cv2.drawContours(output_img, [c], -1, (0, 255, 255), 2) #Draw all the contours with a red background
	a = cv2.rectangle(output_img, (x,y), (x+w, y+h), (0,255,0),3)
	cv2.putText(output_img, "{}min pixel:".format(i) + str(np.min(c)), (x + 20, y + 10), cv2.FONT_HERSHEY_COMPLEX, .7, (0,255,0), 2)
	cv2.putText(output_img, "{}max pixel:".format(i) + str(np.max(c)), (x + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, .7, (0,255,0), 2)


cv2.imshow('image',output_img)
# cv2.imshow('origin', data)

cv2.waitKey(0)
cv2.destroyAllWindows()


