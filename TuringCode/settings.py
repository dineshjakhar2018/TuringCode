"""
Django settings for TuringCode project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import storages
import boto3
from storages.backends.s3boto3 import S3Boto3Storage

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%+4x!!_nfwby&33@)9a1ro@7js&+vu4vd0y4dfzth7q7judgn9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'turing',
    'rank',
    'ckeditor',
    'ckeditor_uploader',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'TuringCode.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'TuringCode.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

#remove when using s3 bucket


'''
STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'StaticFiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles')
]
'''

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email backend settings (for example, using Gmail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # Change the port according to your email provider
EMAIL_HOST_USER = 'turingcodecse@gmail.com'  # Your email address
EMAIL_HOST_PASSWORD = 'wlto rosq gkhb vflr'  # Your email password
EMAIL_USE_TLS = True  # Or False, depending on your email provider



#razorpay api keys
RAZORPAY_KEY_ID = 'rzp_test_PVmqSWVDorZAcn'
RAZORPAY_KEY_SECRET = 'l7Pc6jYjq3J28UUWvzFSE8JD'

#use because popup box blank
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"



# Increase the maximum upload size for single files (default is 2.5 MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 1048576000  # 1 GB (in bytes)

# Adjust file size upload limit (if using FileUpload handlers)
FILE_UPLOAD_MAX_MEMORY_SIZE = 1048576000  # 1 GB (in bytes)

# Set the maximum request size
DATA_UPLOAD_MAX_REQUEST_SIZE = 1048576000  # 1 GB (in bytes)

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

#aws bucket settings
AWS_ACCESS_KEY_ID = 'AKIAXYKJVBVIWKFPWY76'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'turingcode11'
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = 'ap-southeast-2'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


turingcodebucket = 'turingcode11'
STATIC_URL = 'https://%s.s3.amazonaws.com/'%turingcodebucket
#if we use S3 bucket then its useless
CKEDITOR_BASEPATH = 'https://turingcode11.s3.amazonaws.com/ckeditor/ckeditor/'
CKEDITOR_UPLOAD_PATH = 'https://turingcode11.s3.amazonaws.com/uploads/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


