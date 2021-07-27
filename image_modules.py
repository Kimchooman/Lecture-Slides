import cv2
import numpy as np

class ImageChanges:

	CHUNK_PADDING = 20
	CHUNCK_MARGIN = 10
	CHUNK_SIZE = 5
	CHUNK_CHANGE_THRESH = 1

	BLACKWHITE_DELTA_TRESH = 200

	def __init__(self, frame):

		self.frame = frame

		self.prev_node_ls = []

		self.prev_bw_frame = None

		self.frame_skip_count = 0
		
	def full_frame_bw_comparison(self):

		thresh_exceeded = False

		gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
		#blurred = cv2.GaussianBlur(gray, (7,7), 0)
		T, threshInv = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

		if  type(self.prev_bw_frame) != type(None):

			change_count = 0

			for r in range(len(self.prev_bw_frame)):
				for p in range(len(self.prev_bw_frame[r])):

					if self.prev_bw_frame[r][p] != threshInv[r][p]:
						change_count += 1

			if change_count >= ImageChanges.BLACKWHITE_DELTA_TRESH:
				thresh_exceeded = True

			self.prev_bw_frame = threshInv

			cv2.imshow("threshInv", threshInv)

		else:
			self.prev_bw_frame = threshInv

		return thresh_exceeded

	def chunk_change_perc(self):
		thresh_exceeded = False
		return thresh_exceeded

	def view_new_image(self):
		return self.frame

	def eval_change(self, frame_skip=10,NODES=False, BWthresh=False):

		bw_comp_bool = None
		node_bool = None

		if self.frame_skip_count >= frame_skip:

			if NODES == True:
				node_bool = self.chunk_change_perc()

			if BWthresh == True:
				bw_comp_bool = self.full_frame_bw_comparison()

			self.frame_skip_count = 0

		else:
			self.frame_skip_count += 1

		return bw_comp_bool
