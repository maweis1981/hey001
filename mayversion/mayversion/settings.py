# Django settings for mayversion project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
# ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
'NAME': 'socialReminder',                      # Or path to database file if using sqlite3.
'USER': 'root',                      # Not used with sqlite3.
'PASSWORD': 'password',                  # Not used with sqlite3.
'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
}
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
# LANGUAGE_CODE = 'zh-CN'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
STATIC_ROOT = os.path.join(PROJECT_PATH, 'media')
BOOKS_ROOT = '/Users/peter/Public/books/'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
BOOK_URL = '/book/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'


# Make this unique, and don't share it with anybody.
SECRET_KEY = '+=(w0&-0kkyyq3@ze3s*pbiko&*@*e+*^68z3i_!79wctfd1&5'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
'django.template.loaders.filesystem.Loader',
'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
'django.middleware.common.CommonMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
#    '/Users/peter/github-projects/hey001/mayversion/templates'
os.path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.sites',
'django.contrib.messages',
# Uncomment the next line to enable the admin:
'django.contrib.admin',
'accounts',
'groups',
'messages',
# 'datings',
'microblog',
# 'bookreader',
'votes',
'avatar_crop',
'avatar',
'chat',
'photologue',
'tagging',
'sorted_paginated_authored_archived_list_view',
# 'iptocountry',
'locations',
# 'django_cron',
'reminds',
'foods',
'weibo',
'twitter',
# 'friends',
# 'mailer',
# 'notification',
# 'emailconfirmation',
)


#-------------------------------------------------------
#Var
#-------------------------------------------------------
###AppInfo
WEIBO_APP_KEY = "1245737263"
WEIBO_APP_SECRET = "7fe77ecdf63a2c162150bc901a67a7b2"

consumer_key    = 'NYqIbv9vCijVb2B6x7jhHg'
consumer_secret = 'fwqThazPj8UGUoEHgErQWjrePssvEdnYpHFuYLfL7jw'

AVATAR_CROP_MIN_SIZE = 8

AUTH_PROFILE_MODULE = "accounts.UserProfile"

ORBITED_SERVER = "192.168.0.14"
APP_SERVER_HOST = "http://192.168.0.14:8000"

APNS_CERTIFICATE = os.path.join(PROJECT_PATH,'social-reminder-apns-dev-cert.pem')
APNS_KEY = os.path.join(PROJECT_PATH,'social-reminder-noenc-apns-dev-key.pem')

# APNS_CERTIFICATE = '/Users/peter/github-projects/hey001/mayversion/ourpoke-dev.pem'
# APNS_KEY = '/Users/peter/github-projects/hey001/mayversion/ourpoke-dev.pem'