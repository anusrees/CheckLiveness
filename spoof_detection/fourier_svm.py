import cv2
import glob
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import normalize
from sklearn.svm import SVC
from sklearn.externals import joblib

def setROI(inputImg_size, roiwidth, roiheight):
	w = inputImg_size[0]
	h = inputImg_size[1]
	xo = 0
	yo = 0
	xb = w
	yb = h
	if w>roiwidth:
		xo = int(w/2 - roiwidth/2)
		xb = int(xo + roiwidth)
	if h>roiheight:
		yo = int(h/2 - roiheight/2)
		yb = int(yo + roiheight)

	return xo, xb, yo, yb

def apply_fourier(img):
	f = np.fft.fft2(img)
	fshift = np.fft.fftshift(f)
	return np.abs(fshift)

def calc_fourier_features(fourier):
	jump = 1
	fsize = np.array(fourier.shape)
	h_fsize = np.int32(fsize/2)
	max_radius = np.min(h_fsize)
	radii_size = int(max_radius/jump)
	feature_count = np.array([0]*radii_size)
	feature_fourier = np.array([0]*radii_size)

	for i in range(fourier.shape[0]):
		for j in range(fourier.shape[1]):
			curr_radius = np.sqrt(np.sum(np.square([i-h_fsize[0], j-h_fsize[1]])))
			if curr_radius < max_radius:
				index = int(curr_radius/jump)
				feature_fourier[index] += fourier[i, j]
				feature_count[index] += 1

	for i in range(radii_size):
		feature_fourier[i] /= feature_count[i]
	feature_fourier[0] = 0

	return feature_fourier

def train_feature(folder_real, folder_spoof):
	#spoof:1 and real:0
	x = []
	y = []
	for filename in glob.glob(folder_real):
		img = cv2.imread(filename, 0)
		cv2.imshow("image", img)
		cv2.waitKey(30)
		x.append(apply_fourier(img))
		y.append(2)

	for filename in glob.glob(folder_spoof):
		img = cv2.imread(filename, 0)
		cv2.imshow("image", img)
		cv2.waitKey(30)
		x.append(apply_fourier(img))
		y.append(3)
	cv2.destroyAllWindows()
	print(len(x[0]))

	list_size = len(x)
	feature_fourier = []

	for i in range(list_size):
		feature_fourier.append(calc_fourier_features(x[i]))
		print("fourier %d calculated ......."%i)

	feature_fourier = normalize(feature_fourier, 'l2', 1, True, False)
	clf = SVC()
	clf.fit(feature_fourier, y)

	joblib.dump(clf, "fourierSVMmodel.pkl")
	print("fourier feature based SVM model created ........")

def visualize_fourier():
	key = 0
	cap = cv2.VideoCapture(0)
	ret, img = cap.read()
	xo, xb, yo, yb = setROI(img.shape, 300, 300)

	while key != 27:
		ret, img = cap.read()
		img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
		img = img[xo:xb, yo:yb]
		cv2.imshow("image", img)
		fourier = apply_fourier(img)
		fimg = cv2.normalize(np.log(fourier), img, 0, 1, cv2.NORM_MINMAX, cv2.CV_32F)
		cv2.imshow("fourier", fimg)
		key = cv2.waitKey(30)

	cap.release()

def predict(clf_file, img):
	clf = joblib.load(clf_file)
	class_ = clf.predict(calc_fourier_features(apply_fourier(img)).reshape(1, -1))
	print(class_)

# train_feature("real/*.jpg", "spoof/*.jpg")
img = cv2.imread("spoof1.jpg", 0)
# xo, xb, yo, yb = setROI(img.shape, 300, 300)
# img = img[xo:xb, yo:yb]
predict("fourierSVMmodel.pkl", img)