# -*- coding: UTF-8 -*-
from django.db import models

# Create your models here.


class Login(models.Model):
    Exam_Site = models.CharField(max_length=128, unique=True)  # 考试地点
    Exam_password = models.CharField(max_length=256)  # 密码
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Exam_Site


class User(models.Model):
    User_Id = models.CharField(max_length=128, unique=True)  # 学号
    User_Name = models.CharField(max_length=128)  # 姓名
    Class_Name = models.CharField(max_length=128)  # 班级
    Exam_Time = models.CharField(max_length=30)  # 考试时间
    Exam_Site = models.CharField(max_length=32)  # 考场地点
    Exam_Number = models.CharField(max_length=32)  # 考场座位号
    Is_Add_Face = models.CharField(max_length=12)  # 人脸是否注册
    Is_Attend = models.CharField(max_length=12)  # 是否签到
    Attend_Time = models.DateTimeField(auto_now_add=True)  # 签到时间

    def __str__(self):
        return self.User_Name

    class Meta:
        ordering = ["-Attend_Time"]