import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.feature import local_binary_pattern

img = cv2.imread("spoof.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.Sobel(img,cv2.CV_8U,1,1,ksize = 5)
# cv2.normalize(realImg, realImg, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
radius = 5
lbp = local_binary_pattern(img, radius*8, radius, method='ror')

cv2.imshow("lbp", lbp)
cv2.imshow("Laplacian", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

plt.hist(img.ravel(),256,[0,256]); 
plt.show()
