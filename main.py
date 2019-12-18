import cv2
import numpy as np
from sort_countour import sort_contours, draw_contour



cap = cv2.VideoCapture(2)

# setup
bluelow = 150
greenlow = 150
redlow = 240
blueup = 255
greenup = 255
redup = 255
result = None
a = 0
while True:
	ret, frame = cap.read()
	key = cv2.waitKey(1)
	lower = np.array([bluelow,greenlow,redlow]) #lower limit of BGR values of the laser line
	upper= np.array([blueup,greenup,redup]) #upper limit of BGR values of the laser line
	mask = cv2.inRange(frame, lower, upper) #create a mask within the specified values of RED
	output_img = frame.copy() #a copy of the main frame is created
	output_img[np.where(mask==0)] = 0 #where the mask value is 0, make those coordinates black
	output_img[np.where(mask>100)] =255 #The target points, or the points which belong to the laser line are displayed in white
	gray = cv2.cvtColor(output_img, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	kernel = np.ones((5,5), np.uint8) 
	thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.erode(thresh, kernel, iterations=1)
	thresh = cv2.dilate(thresh, kernel, iterations=1)

	#finding the contours with RED colour
	cnts, hierarchy  = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	# cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	# print(len(cnts))
	cnts, boundingBoxes = sort_contours(cnts, method='top-to-bottom')
	

	if len(cnts) == 5:
		if key == ord('s'):
			print('get volume')
			cv2.imwrite('gambar{}.jpg'.format(a), output_img)
			a+=1
		# for i, c in enumerate(cnts):
			

		for i, c in enumerate(cnts):
			result = draw_contour(output_img, c, i)
			c=cnts[i]
			print(c)
			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, 0.1 * peri, True)
			x , y , w, h = cv2.boundingRect(approx)
			cv2.drawContours(output_img, [c], -1, (0, 255, 255), 1) #Draw all the contours with a red background
			cv2.rectangle(output_img, (x,y), (x+w, y+h), (0,255,0),3)
			if i == 0:
				cv2.putText(output_img, "ymaxpix:" + str(h), (x + 10, y+10), cv2.FONT_HERSHEY_COMPLEX, .5, (0,255,0), 2)
			if i == 4:
				cv2.putText(output_img, "yminpix:" + str(y), (x + 15, y + 40), cv2.FONT_HERSHEY_COMPLEX, .5, (0,255,0), 2)
			if i == 1:
				cv2.putText(output_img, "xmaxpix:" + str(w), (x + 30, y + 30), cv2.FONT_HERSHEY_COMPLEX, .5, (0,255,0), 2)
			if i == 2:
				cv2.putText(output_img, "xminpix:" + str(x), (x + 10, y + 30), cv2.FONT_HERSHEY_COMPLEX, .5, (0,255,0), 2)
			# cv2.putText(output_img, "{}minpix:".format(i) + str(np.min(c)), (x + 10, y + 20), cv2.FONT_HERSHEY_COMPLEX, .5, (0,255,0), 2)
			# cv2.putText(output_img, "maxpix:" + str(np.max(c)), (x + 10, y + 35), cv2.FONT_HERSHEY_COMPLEX, .5, (0,255,0), 2)


	cv2.imshow('image',output_img)

	cv2.imshow('frame', frame)

	

	
	if key == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()