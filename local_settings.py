import os

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': 'software.cu2wrymkvn8z.ap-northeast-2.rds.amazonaws.com',
        'NAME': 'postgres',
        'USER': 'software',
        'PASSWORD': 'software123',
    }
}

ALLOWED_HOSTS = ['*']
INTERNAL_IPS = ['127.0.0.1']

# MEDIA_URL = 'http://127.0.0.1:8000/media/'
# http://3.34.124.229/ new server address
# MEDIA_URL = 'http://3.34.124.229:8000/media/'
MEDIA_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media/')
MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

STATIC_URL = '/static/'
