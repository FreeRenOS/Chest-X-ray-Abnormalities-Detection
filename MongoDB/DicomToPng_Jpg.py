import os
import pydicom
from glob import glob
from PIL import Image
import cv2
import numpy as np


inputdir = './dicom/'
outdir = './Png_Jpg/'

# 파일 확인 ##

def DicomToJpg(inputdir, outdir):
    test_list = [os.path.basename(x) for x in glob(inputdir + '*.dicom')]
    for f in test_list:
        ds = pydicom.read_file(inputdir + f) # read dicom image
        ## Voi Lut가 있으면 np.uint8으로 변경 없으면 변환없이 반환
        img = pydicom.pixel_data_handlers.util.apply_voi_lut(ds.pixel_array, ds)
        ## dicom 속성에 MONOCHROME1이 있으면 Voi 그레이스케일로 변환
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
    print("Done")

def DicomToPng(inputdir, outdir):
    test_list = [os.path.basename(x) for x in glob(inputdir + '*.dicom')]
    for f in test_list:
        ds = pydicom.read_file(inputdir + f) # read dicom image
        ## Voi Lut가 있으면 np.uint8으로 변경, 없으면 변환없이 반환
        img = pydicom.pixel_data_handlers.util.apply_voi_lut(ds.pixel_array, ds)
        ## dicom 속성에 MONOCHROME1이 있으면 Voi 그레이스케일로 변환
        if ds.PhotometricInterpretation == "MONOCHROME1":
            img = np.amax(img) - img
        img = img - np.min(img)
        img = img / np.max(img)
        img = (img * 255).astype(np.uint8)

        ### PIL
        img_mem = Image.fromarray(img) # Creates an image memory from an object exporting the array interface
        img_mem.save(outdir + f.replace('.dicom', '.png'))

        ### OpenCV
        # cv2.imwrite(outdir + f.replace('.dicom', '.png'), img)
    print("Done")

## 메인 실행
DicomToJpg(inputdir, outdir)