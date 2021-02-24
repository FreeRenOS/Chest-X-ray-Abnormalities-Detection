## 개발환경

### microdicom-3.8.1-x64

### PyCharm 2020.3.2 (Community Edition)
### Build #PC-203.6682.179, built on December 31, 2020
### Runtime version: 11.0.9.1+11-b1145.63 amd64
### VM: OpenJDK 64-Bit Server VM by JetBrains s.r.o.
### Windows 10 10.0
### GC: ParNew, ConcurrentMarkSweep
### Memory: 949M
### Cores: 12

+ install list
  - pydicom
  - pillow
  - pip install opencv-contrib-python
  - matplotlib
  - pymongo
  - pandas
  - pip install pymongo[srv]

+ MongoDB Compass
  - Version 1.25.0

## MongoDB에 Dicom, Png, Jpg 업로드 다운로드

## DicomRead.py
	- Dicom 파일과 csv 파일을 읽어 들여서 병명과 부위 그려서 jpg파일로 저장
	
## DicomToPng_Jpg.py
	- Dicom 파일을 읽어 들여서 Png, Jpg 파일로 저장
	
## MongDB.py
	- pymongo를 이용해 클라우드나 로컬서버를 연결 후 Dicom, Png, Jpg 파일을 도큐먼트에 업로드 및 다운로드 함
	- 보안인증설정되어있으면 몽고DB 아이디 비번 입력해야됨
