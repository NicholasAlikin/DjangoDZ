""" параметры настройки проетка django:
 * конфигурация баз данных
 * список модулей
 * ...
"""

"""
Django settings for project_tracker project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# аюсолютный путь к файлу manage.py
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# для криптографической подписи. секрет...
SECRET_KEY = 'django-insecure-&q#xg^97rr)h3$q6zg96vn=kf6-&hw6x69tuf85yn4+i4%*nl^'

# SECURITY WARNING: don't run with debug turned on in production!
# вкл/выкл режим отладки
DEBUG = True

#список строк с именами хостов/доменов, который может обслуживать сайт джанго
# не применяется при DEBUG == True
ALLOWED_HOSTS = []


# Application definition
# списк приложений, который включены в проект django
INSTALLED_APPS = [
    'django.contrib.admin', # админ панель
    'django.contrib.auth', # фреймворк аунтетификации
    'django.contrib.contenttypes', # фреймворк типов контента
    'django.contrib.sessions', # фреймворк сессий
    'django.contrib.messages', # фреймворк сообщений
    'django.contrib.staticfiles', # фреймворк управления статическими данными
    'tasks.apps.TasksConfig',
    'quality_control.apps.QualityControlConfig',

]
# фреймворк для подключения к обработке запросов/ответов django
# система плагинов для управления системой запросов/ответов 
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# относительный путь к urls.py
ROOT_URLCONF = 'project_tracker.urls'

# настройки языка шаблонов django
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

# относительный путь к wsgi.py
WSGI_APPLICATION = 'project_tracker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# словарь, содержащий настройки для всех баз данных, который будут использоваться в django
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# всегда должна существовать база данных, которая будет использоваться по умолчанию
# в стандартной конфирурации используется sql-lite

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
# список средств проверки надежности паролей пользователя
# по умалчанию проверки нет (принимаются все пароли)
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
# название языка
LANGUAGE_CODE = 'en-us'
# часовой пояс
TIME_ZONE = 'UTC'
# автоматический перевод
USE_I18N = True
# будет ли datetimes учитывать часовой пояс по умалчанию
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
# url адреса, по которому обслуживаются статические данные в каталоге static-root
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
