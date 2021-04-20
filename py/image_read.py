# ==============================================================
# AUTHOR:   MITCH ALVES
# DATE:     2021-01-18
# DESC:     cv2 image read
# ==============================================================

import argparse
from cv2 import cv2

parser = argparse.ArgumentParser()
parser.add_argument("path_image", help="path to input image to be displayed")
args = parser.parse_args()

image = cv2.imread(args.path_image)
args = vars(parser.parse_args())
image2 = cv2.imread(args["path_image"])

cv2.imshow("loaded image", image)
cv2.imshow("loaded image with args", image2)

cv2.waitKey(0)
cv2.destroyAllWindows()

#end
