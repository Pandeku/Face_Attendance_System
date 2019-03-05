# -*- coding: UTF-8 -*-
from django.shortcuts import render, redirect
import pymysql
from aip import AipFace
# import configparser
#
# config = configparser.ConfigParser()
# config.read("project.ini")  # 读配置文件
# # 测试人脸库得到百度 Key
# APP_ID = config.get("Baidu_Key", "APP_ID")
# API_KEY = config.get("Baidu_Key", "API_KEY")
# SECRET_KEY = config.get("Baidu_Key", "SECRET_KEY")
# client = AipFace(APP_ID, API_KEY, SECRET_KEY)
APP_ID = '11155090'
API_KEY = "rG3P2789bywKHfGN0OnEwAgg"
SECRET_KEY = "yTjcZQ92dwGBl3zDY1yWzEz9fb4FeYMc"

client = AipFace(APP_ID, API_KEY, SECRET_KEY)

# Create your views here.


def Get_stu_info(uid):
    result = []
    db = pymysql.connect("localhost", "pandeku", "pandeku", "django_stu_info", charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM _exam_user WHERE User_Id='%s' " % uid
    # noinspection PyBroadException
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
    except:
        print("Error: unable to fetch data")
    # 关闭数据库连接
    db.close()
    return result


def search(request):
    if request.method == "POST":
        Student_ID = request.POST.get("Student_ID")  # 人脸库信息
        try:
            Person = Get_stu_info(Student_ID)
            User_Id = Person[1]
            User_Name = Person[2]
            Class_Name = Person[3]
            Exam_Time = Person[4]
            Exam_Site = Person[5]
            Exam_Number = Person[6]
            Is_Add_Face = Person[7]
            Is_Attend = Person[8]
            Attend_Time = Person[9]
        #
        except:
            message = "No one in info database!"
        Res = client.getUser(Student_ID)
        if 'error_msg' in Res:
            message = 'No person in the face set, please register again.！'  # 返回登陆页面
        else:
            Exam_Name = Res['result'][0]['group_id']
            Student_Id = Res['result'][0]['uid']
            Student_Name = Res['result'][0]['user_info']

        return render(request, '_search/search.html', locals())
    else:
        return render(request, '_search/search.html', locals())
