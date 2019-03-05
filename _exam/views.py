# -*- coding: UTF-8 -*-
import datetime
import time
import os

from .models import Login
from .models import User
from django.shortcuts import render, redirect
import base64
from aip import AipFace

# 正式key
APP_ID = '11155090'
API_KEY = "rG3P2789bywKHfGN0OnEwAgg"
SECRET_KEY = "yTjcZQ92dwGBl3zDY1yWzEz9fb4FeYMc"

client = AipFace(APP_ID, API_KEY, SECRET_KEY)


def all_students(request):
    if request.session.get('is_login', None):
        if request.method == "POST":
            Group_Id = request.session.get('exam_id')
            names = User.objects.all().filter(Exam_Site=Group_Id)
        return render(request, '_exam/all_students.html', locals())
    return redirect("/_exam/exam_login")


def exam_login(request):
    # if request.session.get('is_login', None):
    if request.method == "POST":
        Exam_Name = request.POST.get("Exam_Name")
        Password = request.POST.get("Exam_passed")
        # noinspection PyBroadException
        try:
            Exam_Site = Login.objects.get(Exam_Site=Exam_Name)
            if Exam_Site.Exam_password == Password:
                request.session['is_login'] = True
                request.session['is_exam'] = True
                request.session['is_teacher'] = False
                request.session['exam_id'] = Exam_Name
                message = "Successfully entered the examination room！"
                return render(request, '_exam/sign_in.html', locals())
            else:
                message = "Incorrect password!"
        except:
            message = "Exam site does not exist!"
        return render(request, '_exam/exam_login.html', locals())
    return render(request, '_exam/exam_login.html', locals())


def sign_in(request):
    if request.session.get('is_login', None):
        if request.method == "POST":
            time1 = time.clock()
            Face_Img = request.POST.get('Face')
            image = base64.b64decode(Face_Img.split(',')[-1])
            # 将照片保存下来
            # options = {
            #     "ext_fields": "faceliveness",
            #     "detect_top_num": 3,  # 检测多少个人脸进行比对，默认值1（最多返回10个）
            #     "user_top_num": 1  # 返回识别结果top人数”当同一个人有多张图片时，只返回比对最高的1个分数
            # }
            group_id = request.session.get('exam_id')
            # """ 带参数调用人脸识别 1:n """
            # time2 = time.clock()
            # options = {
            #     "ext_fields": "faceliveness",
            #     "user_top_num": 1
            # }
            # res = client.identifyUser(group__id, image, options)
            # time3 = time.clock()

            """ 带参数调用人脸识别 m:n """
            time2 = time.clock()
            options = {
                "ext_fields": "faceliveness",
                "detect_top_num": 10,  # 检测多少个人脸进行比对，默认值1（最对返回10个）
                "user_top_num": 1  # 返回识别结果top人数”当同一个人有多张图片时，只返回比对最高的1个分数
            }
            res = client.multiIdentify(group_id, image, options)
            time3 = time.clock()
            # """ 带参数调用人脸搜索 """
            # client.multiIdentify(group_id, image, options)
            # 时间戳
            un_time = time.mktime(datetime.datetime.now().timetuple())
            print(res)

            # 保存测试图片
            # un_time = time.mktime(datetime.datetime.now().timetuple())
            # path = "images_high_score"
            # file = open(os.path.join(path, str(un_time) + ".PNG"), 'wb')
            # file.write(image)
            # file.close()

            time4 = time.clock()

            if 'error_msg' in res:
                message = "face not found!"
                path = "err_pic"
                file = open(os.path.join(path, str(un_time) + ".PNG"), 'wb')
                file.write(image)
                file.close()
                # 将记录写进文件里
                txt1 = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "\n"
                path = "score_log"
                with open(os.path.join(path, "wrong_result_time.txt"), 'a') as f:
                    f.write(txt1)
                return render(request, '_exam/sign_in.html', locals())
            else:
                # if float(res['ext_info']['faceliveness']) < 0.0000003241:
                #     message = 'Error: face biopsy failed. Please take photos again!'
                # else:
                for i in range(res['result_num']):
                    uid = res['result'][i]['uid']
                    if res['result'][i]['scores'][0] > 80:  # 人脸识别分数
                        User.objects.filter(User_Id=uid).update(Is_Attend='已签到')
                        try:
                            user =  User.objects.get(User_Id=uid)
                            print (user)
                        except:
                            message = "user not exist!"
                            return render(request, '_exam/sign_in.html', locals())

                        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                        User.objects.filter(User_Id=uid).update(Attend_Time=nowTime)
                        message = "Success in attendance!"
                        # 成功识别保存.
                        un_time = time.mktime(datetime.datetime.now().timetuple())
                        path = "images_high_score"
                        file = open(os.path.join(path, str(uid) + "_" + str(un_time) + ".PNG"), 'wb')
                        file.write(image)
                        file.close()
                    else:
                        # msg = str(res['result'][i]['uid'])
                        # 其他保存
                        path = "images_low_score"
                        file = open(os.path.join(path, str(uid) + "_" + str(un_time) + ".PNG"), 'wb')
                        file.write(image)
                        file.close()
                        message = "face recognition score is too low! "

                    time5 = time.clock()
                    # 将记录写进文件里
                    info = str(res['result'][i]['uid']) + "," + str(res['result'][i]['group_id']) + "," + str(
                            res['result'][i]['scores']) + "\n"
                    txt2 = str(time1) + "," + str(time2) + "," + str(time3) + "," + str(time4) + "," + str(
                            time5) + "," + info
                    path = "score_log"
                    with open(os.path.join(path, "right_result_time_ues.txt"), 'a') as f:
                        f.write(txt2)
                    names = User.objects.all().filter(Is_Attend='已签到').filter(Exam_Site=group_id)
            return render(request, '_exam/sign_in.html', locals())
    else:
        return redirect("/_exam/exam_login")
    return render(request, '_exam/sign_in.html', locals())
