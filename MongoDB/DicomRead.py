from matplotlib import pyplot as plt
import matplotlib.patches as patches
import glob
import pydicom ### to conver dicom to png images
from pydicom.pixel_data_handlers.util import apply_voi_lut ### don't know why???
import cv2 ## OpenCV package
# from skimage import exposure ###  some preprocess like equalize histogram.
import numpy as np
import pandas as pd
import os

# ### imports for the bbox section
# from PIL import Image
# from sklearn import preprocessing
# import random
# from random import randint

for dirname, _, filenames in os.walk('./dicom'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

primary_dir = './'
train_csv = pd.read_csv(primary_dir +'train.csv')
print(train_csv.columns)

def dicom2array(path, voi_lut=True, fix_monochrome=True):
    dicom = pydicom.read_file(path)
    # VOI LUT (if available by DICOM device) is used to
    # transform raw DICOM data to "human-friendly" view
    if voi_lut:
        data = apply_voi_lut(dicom.pixel_array, dicom)
    else:
        data = dicom.pixel_array
    # depending on this value, X-ray may look inverted - fix that:
    if fix_monochrome and dicom.PhotometricInterpretation == "MONOCHROME1":
        data = np.amax(data) - data
    data = data - np.min(data)
    data = data / np.max(data)
    data = (data * 255).astype(np.uint8)
    '''
    new_shape = tuple([int(x / downscale_factor) for x in data.shape])
    data = cv2.resize(data, (new_shape[1], new_shape[0]))
    '''
    return data

for dirname, _, filenames in os.walk('./dicom'):
    for filename in filenames:
        img = dicom2array(os.path.join(dirname, filename))
        image_id = filename.split('.')
        train_id = train_csv[train_csv.image_id == image_id[0]]
        print(train_id['class_id'])
        count = 0
        cv2.imwrite('./image/' + str(image_id[0]) + '.jpg', img)
        img2 = cv2.imread('./image/' + str(image_id[0]) + '.jpg')
        for i in train_id['class_id']:
            if i != 14:
                x_min=train_id['x_min'].iloc[count]
                x_max = train_id['x_max'].iloc[count]
                y_min = train_id['y_min'].iloc[count]
                y_max = train_id['y_max'].iloc[count]
                class_name = train_id['class_name'].iloc[count]
                cv2.putText(img2,class_name,(int(x_min),int(y_min)),cv2.FONT_ITALIC,5,(0,0,0),4)
                cv2.rectangle(img2, (int(x_min),int(y_min)), (int(x_max),int(y_max)), (0,0,255), 3)
            count += 1
        cv2.imwrite('./image/' + str(image_id[0]) + '.jpg', img2)