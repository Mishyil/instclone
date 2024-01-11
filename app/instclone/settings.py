from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = Path(__file__).parent.parent
from decouple import config

import sys
sys.path.append(str(PROJECT_ROOT / 'apps'))



SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(' ')

DEBUG = config('DEBUG', cast=bool)

def show_toolbar(request):
	return config('DEBUG', cast=bool)

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}


INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',

	'debug_toolbar',
	'rest_framework',
	'rest_framework.authtoken',
	'django_extensions',
	'storages',
	'channels',
	'cachalot',

	'explore',
	'main',
	'userprofile',
	'comment',
	'like',
	'userpost',
	'notifications',
	'content',
	'tools',
	'api',

]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['host.docker.internal']

ROOT_URLCONF = 'instclone.urls'




TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
					BASE_DIR / 'templates',
				],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
				'main.context_processors.add_user_to_context',
            ],
        },
    },
]

# WSGI_APPLICATION = 'instclone.wsgi.application'
ASGI_APPLICATION = 'instclone.asgi.application'

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'HOST': config('SQL_HOST'),
		'NAME': config('SQL_NAME'),
		'USER': config('SQL_USER'),
		'PASSWORD': config('SQL_PASS'),
	}
}

CHANNEL_LAYERS = {
	'default': {
		'BACKEND': 'channels_redis.core.RedisChannelLayer',
		'CONFIG': {
			"hosts": [('redis', 6379)],
		},
	},
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

REST_FRAMEWORK = {
	'DEFAULT_RENDERER_CLASSES': (
		'rest_framework.renderers.JSONRenderer',
		'rest_framework.renderers.BrowsableAPIRenderer',
	),
	'DEFAULT_AUTHENTICATION_CLASSES': [
		'rest_framework.authentication.SessionAuthentication',
		'rest_framework.authentication.TokenAuthentication',
	],
	'DEFAULT_PERMISSION_CLASSES': [
		'api.userpost.permissions.IsProfileOwnerOrReadOnly'
	]
}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'userprofile.User'
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
BROKER_URL = config('BROKER_URL')
CELERY_BROKER_URL = config('BROKER_URL')
CELERY_RESULT_BACKEND = config('BROKER_URL')

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
SESSION_COOKIE_SECURE = False

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')



# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL')
AWS_S3_ENDPOINT = config('AWS_S3_ENDPOINT')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}


CACHALOT_UNCACHABLE_TABLES = {'notifications_usernotification'}


CASHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.redis.RedisCache',
		'LOCATION': config('BROKER_URL'),
		'OPTIONS': {
			'db': 3
		}
	}
}