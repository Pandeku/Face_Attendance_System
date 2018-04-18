# -*- coding:UTF-8 -*-
from aip import AipFace

APP_ID = '10924752'
API_KEY = 'rcnNzw3lty5tIj0qSqjGKjMu'
SECRET_KEY = 'DcBm8pAuyaD6QaXAWOMyGCS7tFt7gdAy'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)
image = []
groupId = []
uid = []
userInfo = []


""" 调用人脸检测 """
client.detect(image);
""" 调用人脸比对 """
images = [
 #   get_file_content('example0.jpg'),
 #   get_file_content('example1.jpg'),
]
client.match(images);
""" 调用人脸识别 """
client.identifyUser(groupId, image);
""" 调用人脸认证 """
client.verifyUser(uid, groupId, image);
""" 调用M:N 识别 """
client.multiIdentify(groupId, image);


""" 调用人脸注册 """
client.addUser(uid, userInfo, groupId, image);


""" 调用人脸更新 """
client.updateUser(uid, userInfo, groupId, image);
""" 调用人脸删除 """
client.deleteUser(uid);
""" 调用用户信息查询 """
client.getUser(uid);





# BaiDu AI   接口详细说明

### 人脸检测 ###
""" 调用人脸检测 """
client.detect(image);
""" 如果有可选参数 """
options = {}
options["max_face_num"] = 2  # 最多处理人脸数目，默认值1
options["face_fields"] = "age"
""" 带参数调用人脸检测 """
client.detect(image, options)


### 人脸比对 ###
images = [
 #   get_file_content('example0.jpg'),
 #   get_file_content('example1.jpg'),
]
""" 调用人脸比对 """
client.match(images);
""" 如果有可选参数 """
options = {}
options["ext_fields"] = "qualities"
options["image_liveness"] = ",faceliveness" # 活检
options["types"] = "7,13"
""" 带参数调用人脸比对 """
client.match(images, options)


### 人脸识别 ###
#用于计算指定组内用户，与上传图像中人脸的相似度。识别前提为您已经创建了一个人脸库
# 典型应用场景：如人脸闸机，考勤签到，安防监控等。
""" 调用人脸识别 """
client.identifyUser(groupId, image);
""" 如果有可选参数 """
options = {}
options["ext_fields"] = "faceliveness"
options["user_top_num"] = 3
""" 带参数调用人脸识别 """
client.identifyUser(groupId, image, options)


### 人脸认证 ###
#用于识别上传的图片是否为指定用户，即查找前需要先确定要查找的用户在人脸库中的id。
#典型应用场景：如人脸登录，人脸签到等
""" 调用人脸认证 """
client.verifyUser(uid, groupId, image);
""" 如果有可选参数 """
options = {}
options["top_num"] = 3
options["ext_fields"] = "faceliveness"
""" 带参数调用人脸认证 """
client.verifyUser(uid, groupId, image, options)


### M:N 识别 ###
#待识别的图片中，存在多张人脸的情况下，支持在一个人脸库中，一次请求，同时返回图片中所有人脸的识别结果
""" 调用M:N 识别 """
client.multiIdentify(groupId, image);
""" 如果有可选参数 """
options = {}
options["ext_fields"] = "faceliveness"
options["detect_top_num"] = 3
options["user_top_num"] = 2
""" 带参数调用M:N 识别 """
client.multiIdentify(groupId, image, options)


### 人脸注册 ###
#用于从人脸库中新增用户，可以设定多个用户所在组，及组内用户的人脸图片，
#典型应用场景：构建您的人脸库，如会员人脸注册，已有用户补全人脸信息等。
""" 调用人脸注册 """
client.addUser(uid, userInfo, groupId, image);
""" 如果有可选参数 """
options = {}
options["action_type"] = "replace"
""" 带参数调用人脸注册 """
client.addUser(uid, userInfo, groupId, image, options)


### 人脸更新 ###
#用于对人脸库中指定用户，更新其下的人脸图像。
""" 调用人脸更新 """
client.updateUser(uid, userInfo, groupId, image);
""" 如果有可选参数 """
options = {}
options["action_type"] = "replace"
""" 带参数调用人脸更新 """
client.updateUser(uid, userInfo, groupId, image, options)


### 人脸删除 ###
#用于从人脸库中删除一个用户。
uid = "user1"
""" 调用人脸删除 """
client.deleteUser(uid);
""" 如果有可选参数 """
options = {}
options["group_id"] = "group1"
""" 带参数调用人脸删除 """
client.deleteUser(uid, options)



### 用户查询 ###
uid = "user1"
""" 调用用户信息查询 """
client.getUser(uid);
""" 如果有可选参数 """
options = {}
options["group_id"] = "group1"
""" 带参数调用用户信息查询 """
client.getUser(uid, options)

###用户信息查询###
###组列表查询###
###组内用户列表查询###
###组间复制用户###
###组内删除用户###