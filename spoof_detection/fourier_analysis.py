import os
import cv2
import numpy as np

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

def hfd(magnitude, thresh_freq):
	mag_size = np.int32(np.array(np.shape(magnitude)))
	mag_h_size = np.int32(mag_size/2)
	max_freq = np.sqrt(np.sum(np.square(mag_h_size)))

	high_mag = 0
	total_mag = 0
	cutoff_freq = 2*max_freq/3
	for i in range(0, mag_size[0]):
		for j in range(0, mag_size[1]):
			freq = np.sqrt(np.sum(np.square([i-mag_h_size[0], j-mag_h_size[1]])))
			val = magnitude[i, j]
			if freq >= cutoff_freq and val >= thresh_freq:
				high_mag = high_mag + val
			total_mag = total_mag + val

	return 10*high_mag/(total_mag-np.max(np.max(magnitude[:]))), total_mag

def checkSpoofImage(img, thresh_freq, thresh_hfd):
	magnitude = apply_fourier(img)
	hfd_mag, total_mag = hfd(magnitude, thresh_freq)

	if hfd_mag >= thresh_hfd:
		print("LIVE")
	else:
		print("SPOOF")
	
def checkSpoofTemporal(video, n, thresh_freq, thresh_hfd, thresh_fdd):
	key = 0
	text = ""
	count = 0
	hfd_arr = [0]*n
	total_mag = [0]*n
	magnitude_arr = []

	ret, inputImg = video.read()
	xo, xb, yo, yb = setROI(inputImg.shape, 300, 300)
	inputImg = inputImg[xo:xb, yo:yb]
	img = cv2.cvtColor(inputImg, cv2.COLOR_RGB2GRAY)

	while key!=27:
		ret, inputImg = video.read()
		inputImg = inputImg[xo:xb, yo:yb]

		if key==99:
			for index in range(n+2):
				index = index%n
				
				ret, inputImg = video.read()
				inputImg = inputImg[xo:xb, yo:yb]
				img = cv2.cvtColor(inputImg, cv2.COLOR_RGB2GRAY)

				magnitude = apply_fourier(img)
				if count == 0:
					magnitude_arr = [[[0]*np.size(img, 1)]*np.size(img, 0)]*n
					magnitude_arr[index] = magnitude
					count = 1
				else:
					magnitude_arr[index] = magnitude

				hfd_arr[index], total_mag[index] = hfd(magnitude_arr[index], thresh_freq)
				if np.median(hfd_arr)>=thresh_hfd and np.std(total_mag)>=thresh_fdd:
					text = "LIVE"
				else:
					text = "SPOOF"

				cv2.imshow("image1", img)
				cv2.waitKey(30)

		inputImg = cv2.putText(inputImg, text, (50, 50), 0, 1.0, (0, 255, 0), 2) 
		print(hfd_arr)

		cv2.imshow("image", inputImg)
		key = cv2.waitKey(1)

	video.release()