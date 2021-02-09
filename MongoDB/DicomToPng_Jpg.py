import os
import pydicom
import glob
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt

inputdir = './dicom/'
outdir = './Png_Jpg/'

## 파일 확인 ##



test_list = [os.path.basename(x) for x in glob.glob(inputdir + './*.dicom')]
#glob.glob(inputdir + './*.dcm')
for f in test_list:

    ds = pydicom.read_file(inputdir + f) # read dicom image

    ## Lut 적용된 배열을 np.uint8으로 변경
    img = pydicom.pixel_data_handlers.util.apply_voi_lut(ds.pixel_array, ds)

    ## Voi 를 그레이스케일로 변환
    if ds.PhotometricInterpretation == "MONOCHROME1":
        img = np.amax(img) - img

    img = img - np.min(img)
    img = img / np.max(img)
    img = (img * 255).astype(np.uint8)

    ### PIL
    img_mem = Image.fromarray(img) # Creates an image memory from an object exporting the array interface
    img_mem.save(outdir + f.replace('.dicom', '.jpg'))

    ### OpenCV
    # cv2.imwrite(outdir + f.replace('.dicom', '.png'), img)

# img = cv2.imread('0005e8e3701dfb1dd93d53e2ff537b6e.png')
# cv2.namedWindow('image')  # OpenCV에서 지원하는 창을 생성하는 명령어
# cv2.rectangle(img, (932, 567), (197, 896), (0, 0, 255), 2)
# cv2.imshow('image', img)
# cv2.waitKey()            # 키보드입력을 누를떄까지 보여줌
# cv2.destroyAllWindows()
# kernel = np.array([[0, -1, 0],
#                    [-1, 5,-1],
#                    [0, -1, 0]]) # 커널을 만듭니다.
#
# # 이미지를 선명하게 만듭니다.
# image_sharp = cv2.filter2D(img, -1, kernel)
# plt.imshow(image_sharp, cmap="gray"), plt.axis("off") # 이미지 출력
# plt.show()