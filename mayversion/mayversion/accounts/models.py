#!/usr/bin/env python
# encoding: utf-8


from django.db import models,connection
from django.contrib.auth.models import User,UserManager

class UserProfile(models.Model):

    GENDER_CHOICES = (
    (1, '男'),
    (2, '女'),
    )

    PROVINCE_CHOICES = (
    ('JiangSu','江苏'),
    ('ShangHai','上海'),
    ('ShangHai','上海'),
    ('ShangHai','上海'),
    ('ShangHai','上海'),
    ('ShangHai','上海'),
    )

    user = models.ForeignKey(User, unique=True)
    gender = models.IntegerField(max_length=1, choices=GENDER_CHOICES,default=1)
    birthday = models.DateField(blank=True)
    province = models.CharField(max_length=20, choices=PROVINCE_CHOICES,default=1)
    city = models.CharField(max_length=10)
    livecity = models.CharField(max_length=10)
    regist_date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.user.username

    def set_user_id(self,raw_user_id):
        raw_user = User.objects.get(pk = raw_user_id)
        if raw_user:
            self.user = raw_user
        else:
            raise Exception('User not exist')
    def get_more_profile(self):
        u = UserMoreProfile.objects.get(user = self)
        return u

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class UserMoreProfile(models.Model):
    NATIONAL_CHOICES = ( ('Han','汉族'), ('Hui','回族'), )
    COUNTRY_CHOICES = ( ('China','中国'), ('America','AMERICA'), )
    INCOMING_CHOICES = ( (1,'<2000'), (2,'2000-5000'), (3,'5000-10000'), (4,'10000-20000'), (5,'>20000'), )
    BLOOD_CHOICES = ( ('A','A型'), ('B','B型'), ('AB','AB型'), ('O','O型'), )
    BODY_CHOICES = ( ('A','较瘦'), ('AA','适中'), ('AAA','强壮'), ('AAA','较胖'), )
    DEGREE_CHOICES = ( ('never','从不'), ('little','有时'), ('normal','经常'), )

    user = models.ForeignKey(UserProfile, unique=True)
    height = models.IntegerField("身高",null=True)
    weight = models.IntegerField("体重",null=True)
    blood = models.CharField("血型", max_length=10, choices = BLOOD_CHOICES,default=1)
    body = models.CharField("身材", max_length=10, choices = BODY_CHOICES,default=1)
    national = models.CharField("民族", max_length=10, choices = NATIONAL_CHOICES,default=1)
    country = models.CharField("国籍", max_length=10, choices = COUNTRY_CHOICES,default=1)
    gradute = models.CharField("学历", max_length=10)
    industry = models.CharField("行业", max_length=10)
    incoming = models.IntegerField("收入", choices=INCOMING_CHOICES,default=1,null=True)
    smoking = models.CharField("抽烟", max_length=10, choices = DEGREE_CHOICES,default=1)
    drinking = models.CharField("喝酒", max_length=10, choices = DEGREE_CHOICES,default=1)
    family = models.CharField("家庭情况", max_length=10)
    language = models.CharField("语言", max_length=10)
    hobby = models.CharField("兴趣", max_length=10)
    short = models.SlugField("座右铭")

    def set_user_id(self,raw_user_id):
        raw_user = UserProfile.objects.get(pk = raw_user_id)
        if raw_user:
            self.user = raw_user
        else:
            raise Exception('no user exist')

class WhoVisitMe(models.Model):
    master = models.ForeignKey(User,related_name="masters")
    visitor = models.ForeignKey(User,related_name="visitors")
    visit_time = models.DateTimeField(auto_now_add=True)

    def whoVisitMe(self):
        m_user = self.master
        visitor_list = WhoVisitMe.objects.filter(master=m_user).order_by('-visit_time')
        visitor_user_list = []
        for v in visitor_list:
            visitor_user_list.append(v.visitor)
        return visitor_user_list

    def __unicode__(self):
        return '%s visit %s ' % (self.visitor,self.master)

def listWhoVisitMe(user):
    query = ("select distinct visitor_id from accounts_whovisitme "
                "where master_id='%(user_id)s'") % {
                    'user_id': user.id,
                    }
    cursor = connection.cursor()
    visitor_ids = cursor.execute(query)
    visitorList = []
    
    for v in cursor.fetchall():
        print v[0]
        visitorList.append(User.objects.get(pk=int(v[0])))
    return visitorList

