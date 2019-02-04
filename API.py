#Loading relevant libraries
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
 
## Class for fixing the orientation getting image class
## I have used one class as classifctaion iteself can be done based on detection of Facial Landmark
class OrientationClassifier(object):
	# Initializing the face detector
	detector = dlib.get_frontal_face_detector()

	def __init__(self, args):
		"""
		construct the argument parser and parse the arguments
		args: parsed arguments
		"""
		try:
			# reading the first image
			self.image = cv2.imread(args["image"])
			# creating another copy of first image for comparison. After the facial detector has been applied, if the image exist in correct orientation,
			# it will have a bounding box and hence would be different. Else, it would be the same image
			self.image2 = cv2.imread(args["image"])
			# using predictor for identification of facial landmarks in the face
			self.predictor = dlib.shape_predictor(args["shape_predictor"])
			self.imageResize()
		except:
			raise Exception

	def imageResize(self):
		"""
		Construct for resizing the image
		"""
		self.image = imutils.resize(self.image, width=500)
		self.image2 = imutils.resize(self.image2, width=500)

	def getDifference(self):
		"""
		Construct for detection of facial landmark and thus identifying if the imaghe is in correct orientation not
		"""
		try:
			# using the dlib detector. This is a general detector used for detection of regid objects.
			rects = self.detector(self.image, 1)

			for (i, rect) in enumerate(rects):
			# determine the facial landmarks for the face region, then
			# convert the facial landmark (x, y)-coordinates to a NumPy
			# array
				shape = self.predictor(self.image, rect)
				shape = face_utils.shape_to_np(shape)
	 
				# convert dlib's rectangle to a OpenCV-style bounding box
				# [i.e., (x, y, w, h)], then draw the face bounding box
				(x, y, w, h) = face_utils.rect_to_bb(rect)
				cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
	 
				# show the face number
				cv2.putText(self.image, "Face #{}".format(i + 1), (x - 10, y - 10),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
	 
				# loop over the (x, y)-coordinates for the facial landmarks
				# and draw them on the image
				for (x, y) in shape:
					cv2.circle(self.image, (x, y), 1, (0, 0, 255), -1)
	 		# Getting difference between altered images and initial image to see if there is a bounding box present. 
	 		#If bounding box is present, the image is in correct oreintation
			difference = cv2.subtract(self.image2, self.image)
			b, g, r = cv2.split(difference)
			if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
				return 1
			else:
	 			return 0
	 	except:
	 		# This is because even a non image file can be read, however, it would raise an error when applying a detector
	 		print('Please check the image entered and provide a valid image')
	 		return -1

 			
	def fixOrientation(self):
		"""
		construct for fixing orientation and identifying the class
		"""
		count = 1
		classV = 0
		# we loop through 0 to  360 until the facial landmarks are detecting in the image
		for angle in np.arange(0, 360, 90):
			count += 1
			# rotating both images because we want to have both images similar and the only difference to be the presence
			# or absense of facial landmarks
			self.image = imutils.rotate_bound(self.image, angle)
			self.image2 = imutils.rotate_bound(self.image2, angle)
			self.imageResize()
			val = self.getDifference()
			if val == 0:
				if count == 2:
					classV = 4
				elif count ==3:
					classV = 3
				elif count == 4:
					classV = 2
				return self.image2, classV


if __name__ == "__main__":
#detect face in the image
	ap = argparse.ArgumentParser()
	ap.add_argument("-p", "--shape-predictor", required=True,
		help="shape_predictor_68_face_landmarks.dat")
	ap.add_argument("-i", "--image", required=True,
		help="images/F1.jpg")
	try:
		#extracting the arguments
		args = vars(ap.parse_args())
		name = str(args["image"])
	except :
		print('Please checked the provided arguments') 
		exit()
	try:
		# Calling the class
		cv = OrientationClassifier(args)
	except:
		print('Please pass the correct file')
		exit()
	classV = 1
	# Getting the difference in the loaded images
	value = cv.getDifference()
	if value == 1:
		# Fixing the orientation and saving edited file
		newName = name.split('/')
		name = newName[0]+'/'+'Fixed'+newName[1]
		image, classV = cv.fixOrientation()
		print('Image written to the folder')
		print('Name:', name, ', Class:',  str(classV))
		cv2.imwrite(name, image)
	elif value == 0:
		print('File exists in correct orientation')

