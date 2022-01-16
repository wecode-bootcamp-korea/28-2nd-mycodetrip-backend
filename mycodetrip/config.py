import os
from dotenv import load_dotenv

load_dotenv() # .env 파일을 읽어서 환경변수에 넣어줌

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['TRIP_DATABASE_NAME'],
        'USER': os.environ['TRIP_DATABASE_USER'],
        'PASSWORD': os.environ['TRIP_DATABASE_PASSWORD'],
        'HOST': os.environ['TRIP_DATABASE_HOST'],
        'PORT': int(os.environ.get('TRIP_DATABASE_PORT', '3306')),
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}

SECRET_KEY = os.environ['TRIP_SECRET_KEY']

KAKAO_APP_KEY = os.environ['TRIP_KAKAO_APP_KEY']
KAKAO_APP_SECRET = os.environ['TRIP_KAKAO_APP_SECRET']
KAKAO_REDIRECT_URI = os.environ['TRIP_KAKAO_REDIRECT_URI']
