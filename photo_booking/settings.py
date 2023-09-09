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

SECRET_KEY = os.getenv('SECRET_KEY', default='DEFAULT_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG', True))

ALLOWED_HOSTS = [
    '185.41.162.63',
    '127.0.0.1',
    'localhost',
    'photo-market.acceleratorpracticum.ru',
    'backend',
]

CSRF_TRUSTED_ORIGINS = [
    'https://photo-market.acceleratorpracticum.ru',
    'http://photo-market.acceleratorpracticum.ru',
    'http://185.41.162.63',
]

# CORS domains
CORS_ALLOWED_ORIGINS = ['http://localhost:8000', 'http://backend:8000']
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/swagger/.*$'

AUTH_USER_MODEL = 'users.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'corsheaders',
    'channels',
    'rest_framework',
    'social_django',
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
    'chat.apps.ChatConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
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
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
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
        'NAME': 'django.contrib.auth.password_validation.'
        'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'NumericPasswordValidator',
    },
]

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'}
    }
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

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

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

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
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    'PASSWORD_RESET_CONFIRM_URL': 'api/users/reset_password_confirm/{uid}/{token}',
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'HIDE_USERS': False,
    'PERMISSIONS': {
        'user': ('api.permissions.AdminOrReadOnly',),
        'user_list': ('api.permissions.AdminOrReadOnly',),
    },
    'SERIALIZERS': {
        'current_user': 'api.serializers.UserSerializer',
        'user': 'api.serializers.UserSerializer',
        'user_list': 'api.serializers.UserSerializer',
    },
}

# SOCIAL OAUTH2:
SOCIAL_AUTH_URL_NAMESPACE = 'api:social'
LOGIN_URL = 'api/auth/login/google-oauth2/'
LOGIN_REDIRECT_URL = '/api/user_token/'
LOGOUT_REDIRECT_URL = '/api/main/'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.vk.VKOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

# Vkontakte
SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv('VK_APP_ID')
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv('VK_API_SECRET')
SOCIAL_AUTH_VK_OAUTH2_SCOPE = [
    'email',
]

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# Отправка писем для восстановления пароля smtp
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
