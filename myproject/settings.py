"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rqr_cjv4igscyu8&&(0%e(=sy=f2)p=f_wn&@0xsp7m$@!kp=d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['68.183.91.249','khwoppagiftcard.store','www.khwoppagiftcard.store','localhost','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'widget_tweaks',
    'accounts',
    'boards',
    'products',
    'home',
    'orders',
    'sales',
    'Transactions',
    'crispy_forms',
    # 'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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

# Django Suit configuration example
SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'Khwoppa Gift Card',
    # 'HEADER_DATE_FORMAT': 'l, j. F Y',
    # 'HEADER_TIME_FORMAT': 'H:i',

    # forms
    # 'SHOW_REQUIRED_ASTERISK': True,  # Default True
    # 'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu
    'SEARCH_URL': '/admin/orders/order',

    # Parameter also accepts url name
    # 'SEARCH_URL': 'admin:auth_user_changelist',

    # Set to empty string if you want to hide search from menu
    # 'SEARCH_URL': ''


    'MENU_ICONS': {
       'sites': 'icon-leaf',
       'auth': 'icon-lock',
    },
    # 'MENU_OPEN_FIRST_CHILD': True, # Default True

    # 'MENU_EXCLUDE': ('orders.orderproduct','orderproduct'),

     'MENU': (

        # Keep original label and models
        # 'sites',

        # Rename app and set icon
        # {'app': 'auth', 'label': 'Authorization', 'icon':'icon-lock'},
        #
        # # Reorder app models
        # {'app': 'auth', 'models': ('user', 'group')},
        #
        # # Custom app, with models
        # {'label': 'Settings', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
        #
        # # Cross-linked models with custom name; Hide default icon
        # {'label': 'Custom', 'icon':None, 'models': (
        #     'auth.group',
        #     {'model': 'auth.user', 'label': 'Staff'}
        # )},
        #
        # # Custom app, no models (child links)
        # {'label': 'Users', 'url': 'auth.user', 'icon':'icon-user'},
        #
        # # Separator
        # '-',
        #
        # # Custom app and model with permissions
        # {'label': 'Secure', 'permissions': 'auth.add_user', 'models': [
        #     {'label': 'custom-child', 'permissions': ('auth.add_user', 'auth.add_group')}
        # ]},
    )

    # misc
    # 'LIST_PER_PAGE': 15
}


WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# if DEBUG:
#     DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
# else:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'khwoppadb',
        'USER': 'khwoppa_admin',
        'PASSWORD': 'probook450',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL ='/media/'
#
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_in_env')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT= os.path.join(BASE_DIR,'media')



LOGIN_URL = 'login'

LOGIN_REDIRECT_URL= 'home:home'

LOGOUT_REDIRECT_URL= 'home:home'


SENDGRID_API_KEY='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'
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
MAILER_EMAIL_BACKEND=EMAIL_BACKEND
EMAIL_HOST='smtp.sendgrid.net'
EMAIL_HOST_USER='kgcgiftcard'
EMAIL_HOST_PASSWORD='probook450'
EMAIL_PORT=587
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL='mail@khwoppagiftcard.store'
ACCOUNT_EMAIL_SUBJECT_PREFIX='mail.khwoppagiftcard.store'
