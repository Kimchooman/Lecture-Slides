import cv2
import numpy as np

class ImageChanges:

	NODE_DISTANCE = 10
	NODE_CHANGE_THRESH = 1

	BLACKWHITE_DELTA_TRESH = 100

	def __init__(self, frame):

		self.frame = frame

		self.prev_node_ls = []

		self.prev_bw_frame = None

	def full_frame_bw_comparison(self):

		thresh_exceeded = False

		gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
		#blurred = cv2.GaussianBlur(gray, (7,7), 0)
		T, threshInv = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

		if  self.prev_bw_frame != None:

			change_count = 0

			for r in range(len(self.prev_bw_frame)):
				for p in range(self.prev_bw_frame[r]):

					if self.prev_bw_frame[r][p] != threshInv[r][p]:
						change_count += 1

			if change_count >= BLACKWHITE_DELTA_TRESH:
				thresh_exceeded = True

		else:
			self.prev_bw_frame = threshInv

		return thresh_exceeded

	def node_change_perc(self):

		thresh_exceeded = False

		if self.prev_node_ls != []:

			pixel_delta = (0, 0, 0)
			count = 0
			for r in range(len(self.frame)): 
				for p in range(0, len(self.frame[r]), ImageChanges.NODE_DISTANCE):

					if p != 0:

						prev_r, prev_g, prev_b = self.prev_node_ls[r][p]
						curr_r, curr_g, curr_b = self.frame[r][p]

						print(prev_r, prev_g, prev_b)
						print(curr_r, curr_g, curr_b)

						delta_r = abs(prev_r - curr_r)
						delta_g = abs(prev_g - curr_g)
						delta_b = abs(prev_b - curr_b)

						r, g, b = pixel_delta

						pixel_delta = (r + delta_r, g + delta_g, b + delta_b)

						self.prev_node_ls[r][p] = self.frame[r][p]
						count += 1

			r_total, g_total, b_total = pixel_delta

			r = r_total / count
			g = g_total / count
			b = b_total / count

			if r >= NODE_CHANGE_THRESH:
				thresh_exceeded = True

			elif g >= NODE_CHANGE_THRESH:
				thresh_exceeded = True

			elif b >= NODE_CHANGE_THRESH:
				thresh_exceeded = True

		else:
			count = 0
			for r in range(len(self.frame)):

				self.prev_node_ls.append([])
				for p in range(0, len(self.frame[r])):


					if count == ImageChanges.NODE_DISTANCE:
						self.prev_node_ls[r].append(self.frame[r][p])
						count = 0

					else:
						count += 1
						self.prev_node_ls[r].append(False)

		return thresh_exceeded

	def eval_change(self, NODES=False, BWthresh=False):

		if NODES == True:
			node_bool = self.node_change_perc()

		if BWthresh == True:
			bw_comp_bool = self.full_frame_bw_comparison()