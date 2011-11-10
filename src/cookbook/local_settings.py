import os

from settings import SITE_ROOT

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_ROOT, 'cookbook.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'newsdb': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_ROOT, 'news.db'),
    },
    'addressdb': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_ROOT, 'address.db'),
    },
}
