import os
from pymongo import MongoClient
from PIL import Image
import cv2
import glob
import io
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

cloud_URI = "mongodb+srv://oss:oss1234@cluster0.9shzh.mongodb.net/<dbname>?retryWrites=true&w=majority"
cloud = MongoClient(cloud_URI)

host = "localhost"
port = "27017"
mongo = MongoClient(host, int(port))

### 로컬 or 클라우드
# db = mongo.test_db
db = cloud.test_db
collect = db.collect

# 이미지 저장
inputdir = './Png_Jpg/'
downlodedir = './downlodeimage/'

def uplodeimage(path, collect):
    image_list = [os.path.basename(x) for x in glob.glob(path + './*.jpg')]
    for f in image_list:
        im = Image.open(path + f)
        image_bytes = io.BytesIO()
        im.save(image_bytes, format='jpeg')
        image = {
            'image_id': f[:-4],
            'data': image_bytes.getvalue()
        }
        image_id = collect.insert_one(image).inserted_id
        print("Done")

def downlodeimage(path, collect):
    for image in collect.find():
        pil_img = Image.open(io.BytesIO(image['data']))
        img_name = image['image_id']
        pil_img.save(f'{path}{img_name}.jpg', 'jpeg')
        print("Done")


### OpenCV 용
def CVuplodeimage(path, collect):
    image_list = [os.path.basename(x) for x in glob.glob(path + './*.jpg')]
    for f in image_list:
        im = cv2.imread(path + f)
        _, image_bytes = cv2.imencode('.jpg', im)
        image_bytes = image_bytes.tobytes()
        image = {
            'image_id': f[:-4],
            'data': image_bytes
        }
        image_id = collect.insert_one(image).inserted_id
        print("Done")

def CVdownlodeimage(path, collect):
    for image in collect.find():
        img_str= image['data']
        np_img= np.frombuffer(img_str, dtype=np.uint8)
        cv_img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        img_name = image['image_id']
        cv2.imwrite(f'{path}{img_name}.jpg', cv_img)
        print("Done")


# 이미지 출력

# image = collect.find_one()

### PIL
# pil_img = Image.open(io.BytesIO(image['data'])).convert('RGB')
# pil_img = Image.open(io.BytesIO(image['data']))
# img_name = image['image_id']
# pil_img.save(f'{img_name}.jpg', 'jpeg')

### Opencv
# img_str=io.BytesIO(image['data'])
# img_str=img_str.read()
#-------------------------------------
# img_str= image['data']
# np_img= np.frombuffer(img_str, dtype=np.uint8)
# cv_img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
# img_name = image['image_id']
# cv2.imwrite(f'{img_name}.jpg', cv_img)

### 이미지 보기
# plt.imshow(pil_img, cmap=plt.cm.bone)
# plt.imshow(pil_img, cmap='gray')
# plt.show()

### 메인 실행
# uplodeimage(inputdir, collect)
# downlodeimage(downlodedir, collect)

### 콜렉션안 데이터 모두 삭제하기
# collect.delete_many({})

# CVuplodeimage(inputdir, collect)
CVdownlodeimage(downlodedir, collect)