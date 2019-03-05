# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-02 11:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Exam_Site', models.CharField(max_length=128, unique=True)),
                ('Exam_password', models.CharField(max_length=256)),
                ('c_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User_Id', models.CharField(max_length=128, unique=True)),
                ('User_Name', models.CharField(max_length=128)),
                ('Class_Name', models.CharField(max_length=128)),
                ('Exam_Time', models.CharField(max_length=30)),
                ('Exam_Site', models.CharField(max_length=32)),
                ('Exam_Number', models.CharField(max_length=32)),
                ('Is_Add_Face', models.CharField(max_length=12)),
                ('Is_Attend', models.CharField(max_length=12)),
                ('Attend_Time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['Is_Attend'],
            },
        ),
    ]