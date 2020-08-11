import cv2
from skimage.measure import compare_ssim

imageA = cv2.imread('0_gt_color.png')
imageB = cv2.imread('0_out_color.png')

grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

(score, diff) = compare_ssim(grayA, grayB, full=True)
diff = (diff * 255).astype("uint8")

# cv2.imwrite('0_diff.png',diff)

import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

cm = plt.get_cmap('jet')

colored_image = cm(diff)

Image.fromarray((colored_image[:, :, :3] * 255).astype(np.uint8)).save('0_diff.png')
