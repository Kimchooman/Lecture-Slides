from image_modules import ImageChanges
import time
import cv2

FILE_NAME = "video.mp4"
REMOVE_TRESH = 50
START_BUFFER = 10

AREA_OF_INTEREST = []

def display_image(frame, AOI, title):
	frame = cv2.rectangle(frame, AOI[0], AOI[1], (255,0,0), 1)
	cv2.imshow(title, frame)

def mouseClicked(event, x, y, flags, param):

	if event == cv2.EVENT_LBUTTONDOWN:
		AREA_OF_INTEREST.append((x, y))

	elif event == cv2.EVENT_RBUTTONDOWN:

		for p in AREA_OF_INTEREST:

			_x, _y = p

			if abs(x - _x) < REMOVE_TRESH and abs(y- _y) < REMOVE_TRESH:
				AREA_OF_INTEREST.remove(p)
				break 

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", mouseClicked)
capture = cv2.VideoCapture(FILE_NAME)

if capture.isOpened() == False:
  print("Error, capture not open")

else:

	ret, frame = capture.read()

	cv2.imwrite("temp.jpg", frame)

	while len(AREA_OF_INTEREST) < 2:

		image = cv2.imread("temp.jpg")
		cv2.imshow("Frame", image)

		if cv2.waitKey(25) & 0xFF == ord('q'):
			break

	cv2.destroyAllWindows()


	x, y = AREA_OF_INTEREST[0]
	x1, y1 = AREA_OF_INTEREST[1]

	subimage = frame[y:y1, x:x1,:]

	changeManager = ImageChanges(subimage)

	saved_count = 0

	while capture.isOpened(): # Area of interest has been calibrated

		ret, frame = capture.read()

		#display_image(frame, AREA_OF_INTEREST, "Frame")

		x, y = AREA_OF_INTEREST[0]
		x1, y1 = AREA_OF_INTEREST[1]

		subimage = frame[y:y1, x:x1,:]

		changeManager.frame = subimage

		bw_change = changeManager.eval_change(frame_skip=30, BWthresh=True)

		if bw_change == True:
			cv2.imwrite(f"{saved_count}.jpg", subimage)
			saved_count += 1

		cv2.imshow("Subimage", subimage)

		#time.sleep(0.25)

		if cv2.waitKey(25) & 0xFF == ord('q'):
			break


capture.release()
cv2.destroyAllWindows()
