# -*- coding: UTF-8 -*-
import base64
import datetime
import time
import os
import pymysql
from .models import login
from django.shortcuts import render
from aip import AipFace
# import configparser
#
# config = configparser.ConfigParser()
# config.read("project.ini")  # 读配置文件
# APP_ID = config.get("Baidu_Key", "APP_ID")
# API_KEY = config.get("Baidu_Key", "API_KEY")
# SECRET_KEY = config.get("Baidu_Key", "SECRET_KEY")
# client = AipFace(APP_ID, API_KEY, SECRET_KEY)

APP_ID = '11155090'
API_KEY = "rG3P2789bywKHfGN0OnEwAgg"
SECRET_KEY = "yTjcZQ92dwGBl3zDY1yWzEz9fb4FeYMc"

client = AipFace(APP_ID, API_KEY, SECRET_KEY)


def teacher_login(request):
    if request.method == "POST":
        teacher = request.POST.get("Teacher_Name")
        password = request.POST.get("Teacher_Password")
        # noinspection PyBroadException
        try:
            New_Teacher = login.objects.get(Teacher_Name=teacher)
            if New_Teacher.Teacher_Password == password:
                request.session['is_login'] = True
                request.session['is_teacher'] = True
                request.session['is_exam'] = False
                request.session['teacher'] = teacher
                message = "Successfully Login！"
                return render(request, '_teacher/index.html', locals())
            else:
                message = "Incorrect password!"
        except:
            message = "Teacher does not exist!"
        return render(request, '_teacher/teacher_login.html', locals())
    return render(request, '_teacher/teacher_login.html', locals())


def index(request):
    return render(request, '_teacher/index.html', locals())


def add_student(request):
    if request.method == "POST":
        student = []
        student_id = request.POST.get("student_id")
        student_name = request.POST.get("student_name")
        student_class = request.POST.get("student_class")
        test_time = request.POST.get("test_time")
        test_site = request.POST.get("test_site")
        test_number = request.POST.get("test_number")
        is_add = "人脸未注册！"
        is_attend = "未签到！"
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db = pymysql.connect("localhost", "pandeku", "pandeku", "django_stu_info", charset='utf8')  # 数据库连接
        cursor = db.cursor()
        sql = "INSERT INTO `_exam_user`(User_Id, User_Name, Class_Name, Exam_Time, \
        Exam_Site,Exam_Number,Is_Add_Face,Is_Attend,Attend_Time) \
        VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s' )" % \
              (student_id, student_name, student_class, test_time, test_site, test_number, is_add, is_attend, nowtime)
        try:
            cursor.execute(sql)
            db.commit()
            message = "Added successfully!"
        except:
            message = "The student already exists!"
            db.rollback()
        db.close()

    return render(request, '_teacher/add_student.html', locals())


def Back_Student(uid):  # 连接mysql 获取学号对应的学生信息
    result = []
    db = pymysql.connect("localhost", "pandeku", "pandeku", "django_stu_info", charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM `_exam_user` WHERE User_Id='%s' " % uid
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
    except:
        print("Error: unable to fetch data")
    db.close()
    return result


def Update_Table(uid):  # 连接mysql 更新学号对应学生的人脸签到记录
    db = pymysql.connect("localhost", "pandeku", "pandeku", "django_stu_info", charset='utf8')
    cursor = db.cursor()
    sql = "UPDATE _exam_user SET Is_Add_Face='%s' WHERE User_Id = '%s'" % ("人脸已注册!", uid)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print("Error: unable to update data")
    db.close()
    return


def register(request):
    if request.method == "POST":
        uid = request.POST.get('User_Id')  # 前端获取学号
        uid = uid.strip()
        face__img = request.POST.get('Face')  # 获取头像
        image = base64.b64decode(face__img.split(',')[-1])  # 获取头像的base64 编码
        # noinspection PyBroadException
        try:
            User = Back_Student(uid)  # 查询学生信息 pymysql 方法查询学生信息
            user_info = User[2]  # 学生姓名
            group__id = User[5]  # 获取考场

            # group__id = "test"  # 获取考场
            # (382, '1770603106', 'DIEYE MAISSA', '注会173（全英）', '14：25-15：35', '15_201', '工2-201-6', '未注册！', '未签到！\r',
            #  datetime.datetime(2018, 5, 14, 12, 12, 8))
            # new__user = models.User.objects.get(User_Id=uid)  # django方法查询学生姓名
        except:
            message = "No one in the database!"
            return render(request, '_teacher/register.html', locals())
        res = client.addUser(uid, user_info, group__id, image)  # 注册人脸
        print(res)
        if 'error_msg' not in res:
            Update_Table(uid)
            message = "register was successful!"  # 前台显示信息
        else:
            message = "register fail!"  # 前台显示信息
        # models.User.objects.filter(User_Id=uid).update(Is_Add_Face='人脸已注册!')  # 更新注册记录

        un_time = time.mktime(datetime.datetime.now().timetuple())
        path = "images_register"
        file = open(os.path.join(path, str(uid) + "_" + str(un_time) + ".PNG"), 'wb')
        file.write(image)
        file.close()
        # Res = client.verifyUser(Uid, group__id, Image)  # 注册前人脸认证
        # print(Res)
        # if 'error_msg' in Res:  # 认证没有通过
        #     if Res['error_msg'] == 'user not found':
        #         message = 'Face not found'
        #     if Res['error_msg'] == 'user not exist':
        #         message = "register was successful!"  # 前台显示信息
        #         res = client.addUser(Uid, UserInfo, group__id, Image)  # 注册人脸
        #         models.User.objects.filter(User_Id=Uid).update(Is_Add_Face='人脸已注册!')  # 写进mysql
        # else:  # 认证通过
        #     message = "Error:The account has been registered by another person. Please contact the administrator!"
        #     return render(request, 'login_register_attend/register.html', locals())
    return render(request, '_teacher/register.html', locals())


def delete_student(request):
    if request.method == "POST":
        student_id = request.POST.get("Student_ID")
        db = pymysql.connect("localhost", "pandeku", "pandeku", "django_stu_info", charset='utf8')
        cursor = db.cursor()
        sql = "DELETE FROM `_exam_user` WHERE User_Id = '%s'" % student_id
        try:
            cursor.execute(sql)
            db.commit()
            message = "Database, your information is deleted successfully!"
        except:
            message = "Error: unable to update data!"
            db.rollback()
        db.close()
    return render(request, '_teacher/delete_student.html', locals())


def update_table(uid):  # 连接mysql 更新学号对应学生的人脸签到记录
    db = pymysql.connect("localhost", "pandeku", "pandeku", "django_stu_info", charset='utf8')
    cursor = db.cursor()
    sql = "UPDATE `_exam_user` SET Is_Add_Face='%s',Is_Attend='%s' WHERE User_Id = '%s'" % ("未注册！", "未签到！", uid)
    try:
        cursor.execute(sql)
        db.commit()
        message = "Face library, your information is deleted successfully!"
    except:
        message = "Error: unable to update data!"
        db.rollback()
    db.close()
    return message


def delete_face(request):
    if request.method == "POST":
        student_id = request.POST.get("Student_ID")  # 人脸库信息
        res = client.deleteUser(student_id)
        try:
            message = update_table(student_id)
        except:
            pass
    else:
        return render(request, '_teacher/delete_face.html', locals())
    return render(request, '_teacher/delete_face.html', locals())
