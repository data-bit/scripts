# ==============================================================
# AUTHOR:   MITCH ALVES
# DATE:     2021-01-18
# DESC:     cv2 image write
# ==============================================================

import argparse
from cv2 import cv2

parser = argparse.ArgumentParser()
parser.add_argument("path_image_input", help="patth to input image to be displayed")
parser.add_argument("path_image_output", help="patth to input image to be saved")

#store args in dictionary
args = vars(parser.parse_args())

#load and display an image
image_input = cv2.imread(args["path_image_input"])
cv2.imshow("loaded image", image_input)

#convert to grayscale an display
gray_image = cv2.cvtColor(image_input, cv2.COLOR_BAYER_BG2GRAY)
cv2.imshow("gray image", image_input)

#write gray image to disk
cv2.imwrite(args["path_image_output"], gray_image)

cv2.waitKey(0)
cv2destroyAllWindows()





