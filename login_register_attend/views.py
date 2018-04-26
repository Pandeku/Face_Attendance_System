# -*- coding: UTF-8 -*-
import datetime
from . import models
from .models import User
from django.shortcuts import render, redirect
import base64
from aip import AipFace
# 正式key
APP_ID = '11155090'
API_KEY = "rG3P2789bywKHfGN0OnEwAgg"
SECRET_KEY = "yTjcZQ92dwGBl3zDY1yWzEz9fb4FeYMc"

client = AipFace(APP_ID, API_KEY, SECRET_KEY)

# Create your views here.


def page_not_found(request):
    return render(request, 'error_html/404.html')


def page_error(request):
    return render(request, 'error_html/500.html')


def permission_denied(request):
    return render(request, 'error_html/403.html')


def bad_request(request):
    return render(request, 'error_html/400.html')


def test(request):
    if request.method == "POST":
        Face = request.POST.get('Face')
        image = base64.b64decode(Face.split(',')[-1])
        # Group_Id = request.session.get('exam_id')
        Group_Id = 201
        options = {
            "ext_fields": "faceliveness",
            "user_top_num": 1
        }
        """ 带参数调用人脸识别 """
        Res = client.identifyUser(Group_Id, image, options)
        print(Res)
        if 'error_msg' in Res:
            message = "fail!"
        else:
            if float(Res['ext_info']['faceliveness']) < 0.0000003241:
                message = 'Error: face biopsy failed. Please take photos again.!'
                return render(request, 'login_register_attend/test.html', locals())
            else:
                if Res['result'][0]['scores'][0] > 78:  # 人脸识别分数
                    message = '，Scores:'",   success!"
                else:
                    msg = str(Res['result'][0]['uid'])
                    message = "EORRR"
                return render(request, 'login_register_attend/test.html', locals())
    return render(request, 'login_register_attend/test.html', locals())


def exam(request):
    if request.method == "POST":
        Exam_Name = request.POST.get("Exam_Name")
        Exam_Password = request.POST.get("Exam_Password")
        if Exam_Password == 'btu':
            request.session['is_login'] = True
            request.session['exam_id'] = Exam_Name
            message = "The entrance of the examination room is successful！"
        else:
            message = "Failure of the entrance examination！"
        return render(request, 'login_register_attend/index.html', locals())
    return render(request, 'login_register_attend/exam.html', locals())


def index(request):
    if request.session.get('is_login', None):
        if request.method == "POST":
            Group_Id = request.session.get('exam_id')
            names = User.objects.all().filter(Exam_Site=Group_Id)
        return render(request, 'login_register_attend/index.html', locals())
    return render(request, 'login_register_attend/index.html')


def update(request):
    if request.method == "POST":
        Student_ID = request.POST.get("Student_ID")  # 人脸库信息
        Res = client.deleteUser(Student_ID)
        models.User.objects.filter(User_Id=Student_ID).update(Is_Add_Face='未注册！')
        models.User.objects.filter(User_Id=Student_ID).update(Is_Attend='未签到！')
        message = "Face library, your information is deleted successfully！"
    else:
        return render(request, 'login_register_attend/update.html', locals())
    return render(request, 'login_register_attend/update.html', locals())


def search(request):
    if request.method == "POST":
        Student_ID = request.POST.get("Student_ID")  # 人脸库信息
        Person = User.objects.all().filter(User_Id=Student_ID)
        Res = client.getUser(Student_ID)
        if 'error_msg' in Res:
            message = 'No person in the face library, please register again.！'  # 返回登陆页面
        else:
            Exam_Name = Res['result'][0]['group_id']
            Student_Id = Res['result'][0]['uid']
            Student_Name = Res['result'][0]['user_info']
    else:
        return render(request, 'login_register_attend/search.html', locals())
    return render(request, 'login_register_attend/search.html', locals())


def login(request):
    if request.session.get('is_login', None):
        if request.method == "POST":
            Face_Img = request.POST.get('Face')
            image = base64.b64decode(Face_Img.split(',')[-1])
            # options = {
            #     "ext_fields": "faceliveness",
            #     "detect_top_num": 3,  # 检测多少个人脸进行比对，默认值1（最对返回10个）
            #     "user_top_num": 1  # 返回识别结果top人数”当同一个人有多张图片时，只返回比对最高的1个分数
            # }
            Group_Id = request.session.get('exam_id')
            # Res = client.multiIdentify(Group_Id, image, options)
            options = {
                "ext_fields": "faceliveness",
                "user_top_num": 1
            }
            """ 带参数调用人脸识别 """
            Res = client.identifyUser(Group_Id, image, options)

            if 'error_msg' in Res:
                message = 'Please register face first！'  # 返回登陆页面
                return render(request, 'login_register_attend/login.html', locals())
            else:
                # if float(Res['ext_info']['faceliveness']) < 0.3241:
                #     message = 'Error: face biopsy failed. Please take photos again.!'
                # else:
                if Res['result'][0]['scores'][0] > 90:  # 人脸识别分数
                    uid = Res['result'][0]['uid']
                    models.User.objects.filter(User_Id=uid).update(Is_Attend='已签到！')
                    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    models.User.objects.filter(User_Id=uid).update(Attend_Time=nowTime)
                    message = "Success in attendance！"
                    names = User.objects.all().filter(User_Id=uid)
                else:
                    message = "Face recognition score is too low! Not the student of this examination room"
            return render(request, 'login_register_attend/login.html', locals())
    else:
        return redirect("/exam/")
    return render(request, 'login_register_attend/login.html', locals())


def register(request):
    if request.method == "POST":
        Uid = request.POST.get('User_Id')  # 前端获取学号
        Uid = Uid.strip()
        Face_Img = request.POST.get('Face')  # 获取头像
        Image = base64.b64decode(Face_Img.split(',')[-1])  # 获取头像的base64 编码
        # noinspection PyBroadException
        try:
            New_User = models.User.objects.get(User_Id=Uid)  # 读mysql 数据库
        except:
            message = "No one in the database！"
            return render(request, 'login_register_attend/register.html', locals())
        UserInfo = New_User.User_Name
        Group_Id = New_User.Exam_Site  # 获取考场
        # noinspection PyBroadException
        Res = client.verifyUser(Uid, Group_Id, Image)  # 注册前人脸认证
        if 'error_msg' in Res:  # 认证没有通过
            if Res['error_msg'] == 'user not found':
                message = 'Face not found'
            if Res['error_msg'] == 'user not exist':
                message = UserInfo + "," + "register was successful!"  # 前台显示信息
                res = client.addUser(Uid, UserInfo, Group_Id, Image)  # 注册人脸
                models.User.objects.filter(User_Id=Uid).update(Is_Add_Face='人脸已注册！')  # 写进mysql
        else:  # 认证通过
            message = "Error:The account has been registered by another person. Please contact the administrator.!"
            return render(request, 'login_register_attend/register.html', locals())
    return render(request, 'login_register_attend/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()

    return redirect("/index/")
