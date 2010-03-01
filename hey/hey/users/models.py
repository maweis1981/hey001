from django.db import models

class User(models.Model):
    GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    )


    PROVINCE_CHOICES = (
    ('JiangSu','JIANGSU'),
    ('ShangHai','SHANGHAI')
    )



    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField()
    birthday = models.DateField("your birthday")
    province = models.CharField(max_length=10, choices = PROVINCE_CHOICES)
    city = models.CharField(max_length=10)
    livecity = models.CharField(max_length=10)
    regist_date = models.DateField("regist date",auto_now_add=True)
   
    def __unicode__(self):
        return self.name

class UserMoreInfo(models.Model):

    NATIONAL_CHOICES = (
    ('Han','HAN'),
    ('Hui','HUI'),
    )

    COUNTRY_CHOICES = (
    ('China','CHINA'),
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
    ('A','A'),
    ('B','B'),
    ('AB','AB'),
    ('O','O'),
    )

    BODY_CHOICES = (
    ('A','A'),
    ('AA','AA'),
    ('AAA','AAA'),
    )

    DEGREE_CHOICES = (
    ('never','Never'),
    ('little','Little'),
    ('normal','Normal'),
    )

    user_id = models.OneToOneField(User,primary_key=True)
    height    = models.IntegerField()
    weight = models.IntegerField()
    blood = models.CharField(max_length=10, choices = BLOOD_CHOICES)
    body = models.CharField(max_length=10, choices = BODY_CHOICES)

    national = models.CharField(max_length=10, choices = NATIONAL_CHOICES)
    country = models.CharField(max_length=10, choices = COUNTRY_CHOICES)

    gradute  = models.CharField(max_length=10)
    industry  = models.CharField(max_length=10)

    incoming  = models.IntegerField(choices=INCOMING_CHOICES)

    smoking = models.CharField(max_length=10, choices = DEGREE_CHOICES)
    drinking = models.CharField(max_length=10, choices = DEGREE_CHOICES)
    family = models.CharField(max_length=10)
    language = models.CharField(max_length=10)
    hobby = models.CharField(max_length=10)
    short = models.SlugField()

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