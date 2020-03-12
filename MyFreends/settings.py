import os

import django
django.__path__[0] + ''

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'g6l)2(vhpsn+1_mc(^jxn8&9@av2e0fmr4r#k2rg8y1szsrn3a'

DEBUG = True

AUTH_USER_MODEL = 'account.Account'

ALLOWED_HOSTS = ['*', '127.0.0.1']

INSTALLED_APPS = [
    'account',
    'channels',
    'chat',
    'friendship',
    'django.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MyFreends.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'MyFreends.wsgi.application'

ASGI_APPLICATION = 'MyFreends.routing.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            # "hosts": [('redis', 6379)],
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'HOST': 'postgre',
        # 'PORT': 5432,
        # 'NAME': 'mf',
        # 'USER': 'admin',
        # 'PASSWORD': 'password',
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

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

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER = 'myfreends.official@gmail.com'

EMAIL_HOST_PASSWORD = 'AzegKovWdar142..'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/"),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

MEDIA_URL = '/media/'
