#!/usr/bin/env python
# encoding: utf-8

from django.db import models

class User(models.Model):
    GENDER_CHOICES = (
    ('M', '男'),
    ('F', '女'),
    )

    PROVINCE_CHOICES = (
    ('JiangSu','江苏'),
    ('ShangHai','上海')
    )

    username = models.CharField("用户名",max_length=200)
    gender = models.CharField("性别", max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField("电子邮箱")
    birthday = models.DateField("生日")
    province = models.CharField("省份",max_length=10, choices = PROVINCE_CHOICES)
    city = models.CharField("出生城市", max_length=10)
    livecity = models.CharField("居住城市", max_length=10)
    regist_date = models.DateField("注册时间",auto_now_add=True)
   
    def __unicode__(self):
        return self.username

class Message(models.Model):
     user = models.ForeignKey(User)
     message = models.CharField(max_length=256)
     def __unicode__(self):
         return self.message


class UserMoreInfo(models.Model):

    NATIONAL_CHOICES = (
    ('Han','汉族'),
    ('Hui','回族'),
    )

    COUNTRY_CHOICES = (
    ('China','中国'),
    ('America','AMERICA'),
    )
    

    INCOMING_CHOICES = (
    (1,'<2000'),
    (2,'2000-5000'),
    (3,'5000-10000'),
    (4,'10000-20000'),
    (5,'>20000'),
    )

    BLOOD_CHOICES = (
    ('A','A型'),
    ('B','B型'),
    ('AB','AB型'),
    ('O','O型'),
    )

    BODY_CHOICES = (
    ('A','较瘦'),
    ('AA','适中'),
    ('AAA','强壮'),
    ('AAA','较胖'),
    )

    DEGREE_CHOICES = (
    ('never','从不'),
    ('little','有时'),
    ('normal','经常'),
    )

    user_id = models.OneToOneField(User,primary_key=True)
    height    = models.IntegerField("身高")
    weight = models.IntegerField("体重")
    blood = models.CharField("血型", max_length=10, choices = BLOOD_CHOICES)
    body = models.CharField("身材", max_length=10, choices = BODY_CHOICES)

    national = models.CharField("民族", max_length=10, choices = NATIONAL_CHOICES)
    country = models.CharField("国籍", max_length=10, choices = COUNTRY_CHOICES)

    gradute  = models.CharField("学历", max_length=10)
    industry  = models.CharField("行业", max_length=10)

    incoming  = models.IntegerField("收入", choices=INCOMING_CHOICES)

    smoking = models.CharField("抽烟", max_length=10, choices = DEGREE_CHOICES)
    drinking = models.CharField("喝酒", max_length=10, choices = DEGREE_CHOICES)
    family = models.CharField("家庭情况", max_length=10)
    language = models.CharField("语言", max_length=10)
    hobby = models.CharField("兴趣", max_length=10)
    short = models.SlugField("座右铭")
    def __unicode__(self):
        return self.user_id


class UserTarget(models.Model):
    user_id = models.OneToOneField(User,primary_key=True)
    livecity = models.CharField(max_length=20)
    

class UserHistory(models.Model):
    name = models.CharField(max_length=200)
    updating_date = models.DateTimeField("last updated date")
    gender = models.BooleanField("Choose Female OR Male ")
    def __unicode__(self):
        return self.name

class UserSocialValue(models.Model):
    talent = models.IntegerField()

class UserLog(models.Model):
    resource = models.CharField(max_length=500)
    url = models.CharField(max_length=500)