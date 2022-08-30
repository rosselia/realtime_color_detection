import numpy as np
import cv2


input_video = cv2.VideoCapture('1.mp4')
hedefx = 400
hedefy = 300

while(1):
	_, imageFrame = input_video.read()
	hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
	

	red_lower = np.array([136, 87, 111], np.uint8)
	red_upper = np.array([180, 255, 255], np.uint8)
	red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

	kernal = np.ones((5, 5), "uint8")

	red_mask = cv2.dilate(red_mask, kernal)
	res_red = cv2.bitwise_and(imageFrame, imageFrame,
							mask = red_mask)
	
	contours, hierarchy = cv2.findContours(red_mask,
										cv2.RETR_TREE,
										cv2.CHAIN_APPROX_SIMPLE)
	
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 300):
			x, y, w, h = cv2.boundingRect(contour)
			imageFrame = cv2.rectangle(imageFrame, (x, y),
									(x + w, y + h),
									(0, 0, 255), 2)

			cv2.putText(imageFrame, "red", (x, y),
					cv2.FONT_HERSHEY_SIMPLEX, 1.0,
						(0, 0, 255))	

			
			# DRAWING CIRCLE IN THE CENTER ------------>

			centerx = int(x+(w/2))
			centery = int(y+(h/2))
			cv2.circle(imageFrame,((centerx),centery),4,(0,255,0),-1)

			cv2.circle(imageFrame,((hedefx),hedefy),10,(255,0,0),-1)


			# DY DX LINES

			cv2.line(imageFrame,(hedefx,hedefy),(hedefx,int(y+(h/2))),(0,255,0),2)
			cv2.line(imageFrame,(hedefx,int(y+(h/2))),(centerx,centery),(0,255,0),2)

			dy = y+h/2 -hedefy
			dx = x+w/2 -hedefx

			cv2.putText(imageFrame, "dy", (hedefx, int(hedefy+dy/2)),
					cv2.FONT_HERSHEY_SIMPLEX, 1.0,
						(0, 255,0))	
			

			cv2.putText(imageFrame, "dx", (int(hedefx+dx/2), centery),
					cv2.FONT_HERSHEY_SIMPLEX, 1.0,
						(0, 255,0))	




	cv2.imshow("Red Detection", imageFrame)
	if cv2.waitKey(10) & 0xFF == ord('q'):
		
		cv2.destroyAllWindows()
		break



