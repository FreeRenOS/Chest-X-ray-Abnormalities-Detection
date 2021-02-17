import os
from pymongo import MongoClient
from PIL import Image
import cv2
from glob import glob
import io
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import time
import gridfs
import zstandard as zstd

### 자신의 mongodb uri 설정 아이디 비번 dbname 입력
cloud_URI = "mongodb+srv://oss:<password>@cluster0.9shzh.mongodb.net/<dbname>?retryWrites=true&w=majority"
# cloud_URI = "mongodb+srv://아이디:비번@cluster0.9shzh.mongodb.net/디비이름?retryWrites=true&w=majority&compressors=zstd"
# cloud = MongoClient(cloud_URI)
cloud = MongoClient(cloud_URI)

host = "localhost"
port = "27017"
mongo = MongoClient(host, int(port))

### 로컬 or 클라우드
# db = mongo.test_db
db = cloud.test_db
collect = db.collect

## 이미지 저장 경로
PngJpgdir = './Png_Jpg/'
Dicomdir = './dicom/'
downloaddir = './downloadimage/'
primary_dir = './'
train_csv = pd.read_csv(primary_dir +'train.csv')
# for dirname, _, filenames in os.walk('./dicom'):
#     for filename in filenames:


def uploadJpgimage(path, collect):
    image_list = [os.path.basename(x) for x in glob(path + './*.jpg')] ## 경로 안 파일의 이름만 리스트로 넣음
    for f in image_list:
        im = Image.open(path + f)
        image_bytes = io.BytesIO() ## io.BytesIO 객체 생성
        im.save(image_bytes, format='jpeg') ## 이미지 변환해서 byte형태로 넣기
        train_id = train_csv[train_csv.image_id == f[:-4]] ## csv에서 이미지파일 이름과 같은 image_id만 뽑기
        count = 0

        for i in train_id['class_id']: ## 한 행씩 정보 넣기
            x_min = train_id['x_min'].iloc[count]
            x_max = train_id['x_max'].iloc[count]
            y_min = train_id['y_min'].iloc[count]
            y_max = train_id['y_max'].iloc[count]
            class_name = train_id['class_name'].iloc[count]
            class_id = train_id['class_id'].iloc[count]
            rad_id = train_id['rad_id'].iloc[count]

            upquery = {'image_id': f[:-4]}
            upimage = {'$push': {'class_name': class_name,
                                 'class_id': class_id.item(),
                                 'rad_id': rad_id,
                                 'x_min': x_min,
                                 'y_min': y_min,
                                 'x_max': x_max,
                                 'y_max': y_max}
                       }
            ## mongodb에 업데이트함, upsert 옵션으로 도큐먼트가 없으면 새롭게 만듬
            collect.update_one(upquery, upimage, upsert=True)
            print(upimage)
            count += 1
        upquery = {'image_id': f[:-4]}
        upimage = {'$set': {'data': image_bytes.getvalue()}
                   }
        collect.update_one(upquery, upimage)
    print("Done")

def downloadJpgimage(path, collect):
    for image in collect.find(): ## collection에 있는 문서 하나씩 가져옴
        pil_img = Image.open(io.BytesIO(image['data'])) ## 'data' 필드에 있는 Byte 가져옴
        img_name = image['image_id']
        pil_img.save(f'{path}{img_name}.jpg', 'jpeg') ##원하는 경로와 이름으로 저장
    print("Done")

def uploadPngimage(path, collect):
    image_list = [os.path.basename(x) for x in glob(path + './*.png')] ## 경로 안 파일의 이름만 리스트로 넣음
    for f in image_list:
        im = Image.open(path + f)
        image_bytes = io.BytesIO() ## io.BytesIO 객체 생성
        im.save(image_bytes, format='png') ## 이미지 변환해서 byte형태로 넣기
        train_id = train_csv[train_csv.image_id == f[:-4]] ## csv에서 이미지파일 이름과 같은 image_id만 뽑기
        count = 0

        for i in train_id['class_id']: ## 한 행씩 정보 넣기
            x_min = train_id['x_min'].iloc[count]
            x_max = train_id['x_max'].iloc[count]
            y_min = train_id['y_min'].iloc[count]
            y_max = train_id['y_max'].iloc[count]
            class_name = train_id['class_name'].iloc[count]
            class_id = train_id['class_id'].iloc[count]
            rad_id = train_id['rad_id'].iloc[count]

            upquery = {'image_id': f[:-4]}
            upimage = {'$push': {'class_name': class_name,
                                 'class_id': class_id.item(),
                                 'rad_id': rad_id,
                                 'x_min': x_min,
                                 'y_min': y_min,
                                 'x_max': x_max,
                                 'y_max': y_max}
                       }
            ## mongodb에 업데이트함, upsert 옵션으로 도큐먼트가 없으면 새롭게 만듬
            collect.update_one(upquery, upimage, upsert=True)
            print(upimage)
            count += 1
        upquery = {'image_id': f[:-4]}
        upimage = {'$set': {'data': image_bytes.getvalue()}
                   }
        collect.update_one(upquery, upimage)
    print("Done")

def downloadPngimage(path, collect):
    for image in collect.find(): ## collection에 있는 문서 하나씩 가져옴
        pil_img = Image.open(io.BytesIO(image['data'])) ## 'data' 필드에 있는 Byte 가져옴
        img_name = image['image_id']
        pil_img.save(f'{path}{img_name}.png', 'png') ##원하는 경로와 이름으로 저장
    print("Done")

### OpenCV 용
# def CVuploadimage(path, collect):
#     image_list = [os.path.basename(x) for x in glob(path + './*.jpg')]
#     for f in image_list:
#         im = cv2.imread(path + f)
#         _, image_bytes = cv2.imencode('.jpg', im) ## 이미지를 메모리버퍼형으로 변환
#         image_bytes = image_bytes.tobytes() ##  버퍼를 byte형태로 변환
#         train_id = train_csv[train_csv.image_id == f[:-4]]  ## csv 파일 읽고 파일 이름과 같은 image_id만 찾기
#         count = 0
#         for i in train_id['class_id']:
#             x_min = train_id['x_min'].iloc[count]
#             x_max = train_id['x_max'].iloc[count]
#             y_min = train_id['y_min'].iloc[count]
#             y_max = train_id['y_max'].iloc[count]
#             class_name = train_id['class_name'].iloc[count]
#             class_id = train_id['class_id'].iloc[count]
#             rad_id = train_id['rad_id'].iloc[count]
#
#             upquery = {'image_id': f[:-4]}
#             upimage = {'$push': {'class_name': class_name,
#                                  'class_id': class_id.item(),
#                                  'rad_id': rad_id,
#                                  'x_min': x_min,
#                                  'y_min': y_min,
#                                  'x_max': x_max,
#                                  'y_max': y_max}
#                        }
#             ## mongodb에 업데이트 upsert 옵션으로 도큐먼트가 없으면 새롭게 만듬
#             collect.update_one(upquery, upimage, upsert=True)
#             print(upimage)
#             count += 1
#         upquery = {'image_id': f[:-4]}
#         upimage = {'$set': {'data': image_bytes}
#                    }
#         collect.update_one(upquery, upimage)
#     print("Done")
#
# def CVdownloadimage(path, collect):
#     for image in collect.find():
#         img_str= image['data']
#         np_img= np.frombuffer(img_str, dtype=np.uint8)
#         cv_img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
#         img_name = image['image_id']
#         cv2.imwrite(f'{path}{img_name}.jpg', cv_img)
#     print("Done")


### 대용량저장 GridFS로 dicom 업다운로드
def UpGridFSDicom(path, db):
    fs = gridfs.GridFSBucket(db)
    image_list = [os.path.basename(x) for x in glob(path + './*.dicom')]
    for f in image_list:
        with open(path + f, 'rb') as dicom:
            f_id=fs.upload_from_stream(f, dicom)
        print(f'{f_id} {f}')
    print('Done')


def DownGridFSDicom(path, db):
    fs = gridfs.GridFSBucket(db)
    for data in db.fs.files.find({}, {'filename':True}):
        filename = data['filename']
        with open(path + filename, 'wb') as dicom:
            fs.download_to_stream_by_name(data['filename'], dicom)
    print('Done')

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

### 콜렉션안 데이터 모두 삭제하기
collect.delete_many({})

### gridFS 사용하면 콜렉션이 2개 생긴다 둘다 삭제한다
# db.fs.chunks.delete_many({})
# db.fs.files.delete_many({})

### 메인 실행
start = time.time() ## 시작 시간 저장
uploadJpgimage(PngJpgdir, collect) ## 사진 업로드
print("Upload time :", time.time() - start) ## 현재시각 - 시작시간 = 실행 시간

start = time.time()
downloadJpgimage(downloaddir, collect)  ## 사진 다운로드
print("Download time :", time.time() - start)

# start = time.time()
# UpGridFSDicom(Dicomdir, db)
# print("Upload time :", time.time() - start)
#
# start = time.time()
# DownGridFSDicom(downloaddir, db)
# print("Download time :", time.time() - start)




