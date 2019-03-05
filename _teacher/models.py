# -*- coding: UTF-8 -*-
from django.db import models


# Create your models here.


class login(models.Model):
    Teacher_Name = models.CharField(max_length=128, unique=True)  # 考试地点
    Teacher_Password = models.CharField(max_length=256)  # 密码
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Teacher_Name
