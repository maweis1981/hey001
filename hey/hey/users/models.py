#!/usr/bin/env python
# encoding: utf-8

from django.db import models
from django.utils.encoding import smart_str
from django.utils.hashcompat import md5_constructor, sha_constructor
from django.core.urlresolvers import reverse

def get_hexdigest(algorithm, salt, raw_password):
    """
    Returns a string of the hexdigest of the given plaintext password and salt
    using the given algorithm ('md5', 'sha1' or 'crypt').
    """
    raw_password, salt = smart_str(raw_password), smart_str(salt)
    if algorithm == 'crypt':
        try:
            import crypt
        except ImportError:
            raise ValueError('"crypt" password algorithm not supported in this environment')
        return crypt.crypt(raw_password, salt)

    if algorithm == 'md5':
        return md5_constructor(salt + raw_password).hexdigest()
    elif algorithm == 'sha1':
        return sha_constructor(salt + raw_password).hexdigest()
    raise ValueError("Got unknown password algorithm type in password.")

def check_password(raw_password, enc_password):
    """
    Returns a boolean of whether the raw_password was correct. Handles
    encryption formats behind the scenes.
    """
    algo, salt, hsh = enc_password.split('$')
    print hsh
    print get_hexdigest(algo, salt, raw_password)
    return hsh == get_hexdigest(algo, salt, raw_password)

class User(models.Model):
    GENDER_CHOICES = (
    (1, '男'),
    (2, '女'),
    )

    PROVINCE_CHOICES = (
    ('JiangSu','江苏'),
    ('ShangHai','上海')
    )

    username = models.CharField("用户名",max_length=200)
    password = models.CharField("密码",max_length=32)
    gender = models.IntegerField("性别", max_length=1, choices=GENDER_CHOICES,default=1)
    email = models.EmailField("电子邮箱")
    birthday = models.DateField("生日")
    province = models.CharField("省份",max_length=10, choices = PROVINCE_CHOICES,default=1)
    city = models.CharField("出生城市", max_length=10)
    livecity = models.CharField("居住城市", max_length=10)
    regist_date = models.DateField("注册时间",auto_now_add=True)

    def __unicode__(self):
        return self.username

    def set_password(self, raw_password):
        import random
        algo = 'sha1'
        salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
        hsh = get_hexdigest(algo, salt, raw_password)
        self.password = '%s$%s$%s' % (algo, salt, hsh)

    def validate_password(self, raw_password):
        print '--------------------------==================='
        print self.password
        """
        Returns a boolean of whether the raw_password was correct. Handles
        encryption formats behind the scenes.
        """
        # Backwards-compatibility check. Older passwords won't include the
        # algorithm or salt.
        if '$' not in self.password:
            is_correct = (self.password == get_hexdigest('md5', '', raw_password))
            if is_correct:
            # Convert the password to the new, more secure format.
                self.set_password(raw_password)
                self.save()
            return is_correct
        return check_password(raw_password, self.password)

    @models.permalink
    def get_absolute_url(self):
        return ("view",[str(self.id)])


class Message(models.Model):
    user = models.ForeignKey(User)
    message = models.CharField(max_length=256)
    happenTime = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=32)
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
    height = models.IntegerField("身高")
    weight = models.IntegerField("体重")
    blood = models.CharField("血型", max_length=10, choices = BLOOD_CHOICES,default=1)
    body = models.CharField("身材", max_length=10, choices = BODY_CHOICES,default=1)

    national = models.CharField("民族", max_length=10, choices = NATIONAL_CHOICES,default=1)
    country = models.CharField("国籍", max_length=10, choices = COUNTRY_CHOICES,default=1)

    gradute  = models.CharField("学历", max_length=10)
    industry  = models.CharField("行业", max_length=10)

    incoming  = models.IntegerField("收入", choices=INCOMING_CHOICES,default=1)

    smoking = models.CharField("抽烟", max_length=10, choices = DEGREE_CHOICES,default=1)
    drinking = models.CharField("喝酒", max_length=10, choices = DEGREE_CHOICES,default=1)
    family = models.CharField("家庭情况", max_length=10)
    language = models.CharField("语言", max_length=10)
    hobby = models.CharField("兴趣", max_length=10)
    short = models.SlugField("座右铭")

    def set_user_id(self,raw_user_id):
        raw_user = User.objects.get(pk = raw_user_id)
        if raw_user:
            self.user_id = raw_user
        else:
            raise Exception('no user exist')

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

class Friendly(models.Model):
    a = models.ForeignKey(User)

class ForbiddenUser(models.Model):
    a = models.ForeignKey(User)
    