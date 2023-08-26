"""
Django settings for photo_booking project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
    "django-insecure-63a8^!ocz7m^3r!g%xw88@f(v*2pa_!sswjfg)rm_r5andp&xc"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '185.41.162.63',
    '127.0.0.1',
    'localhost',
    'photo-market.acceleratorpracticum.ru',
    'backend:8000',
]

AUTH_USER_MODEL = 'users.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',  # Регистрация приложения channels
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'djoser',
    'phone_field',
    'sorl.thumbnail',
    'users.apps.UsersConfig',
    'api.apps.ApiConfig',
    'services.apps.ServicesConfig',
    'properties.apps.PropertiesConfig',
    'orders.apps.OrdersConfig',
    'chat.apps.ChatConfig',  # Регистрация приложения чат
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "photo_booking.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = 'photo_booking.wsgi.application'
ASGI_APPLICATION = 'photo_booking.asgi.application'

# Добавляем возможность работы со слоями для websocket соединения.
# Дополнительно необходимо установить Redis
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE'),
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation\
        .UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation\
        .MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.\
        CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.\
        NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

# Vkontakte
VK_APP_ID = os.getenv('VK_APP_ID')
VK_APP_SECRET = os.getenv('VK_API_SECRET')


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MAX_EMAIL_NAME_LENGTH = 40
MAX_LEN_ABOUT_ME = 150
MAX_LEN_NAME = 25
MAX_TEXT_LEN = 500
NO_REGISTER_USERNAME = 'me'

# DJOSER

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'HIDE_USERS': False,
    'PERMISSIONS': {
        'user': ('api.permissions.AdminOrAuthorOrReadOnly',),
        'user_list': ('api.permissions.AdminOrAuthorOrReadOnly',),
    },
    'SERIALIZERS': {
        'current_user': 'api.serializers.UserSerializer',
        'user': 'api.serializers.UserSerializer',
        'user_list': 'api.serializers.UserSerializer',
    },
}
