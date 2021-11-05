"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
# import django

# django.setup()
import os.path
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.


BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-e84)f1*014u+zp_z)b(ou+j^s@naz4r2!wspiv8j_^o2xo%1dz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    # Apps
    'users',
    'dashboard',
    'training',
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Rest
    'rest_framework',
    'rest_framework.authtoken',
    # drf-social-oauth2
    'oauth2_provider',
    'social_django',
    'drf_social_oauth2',
    # CORS
    'corsheaders',
    # django models to diagram
    'django_extensions',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.AllowAny'
        'rest_framework.permissions.IsAuthenticated'
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'drf_social_oauth2.authentication.SocialAuthentication',
    )
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # cors
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.UserExtended'

AUTHENTICATION_BACKENDS = (
    # drf_social_oauth2
    'drf_social_oauth2.backends.DjangoOAuth2',
    # Django
    'django.contrib.auth.backends.ModelBackend',
    # Facebook OAuth2
    'social_core.backends.facebook.FacebookAppOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    # Google OAuth2
    'social_core.backends.google.GoogleOAuth2',
)

# Facebook configuration
SOCIAL_AUTH_FACEBOOK_KEY = '412879967053238'
SOCIAL_AUTH_FACEBOOK_SECRET = '68a29697b18a588ee205b3170036be2a'
# Define SOCIAL_AUTH_FACEBOOK_SCOPE to get extra permissions from Facebook.
# Email is not sent by default, to get it, you must request the email permission.
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email'
}

# Google configuration
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '184998521093-72jv3431tpjsrgfb1icl3qftpqda7e8j.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

# Define SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE to get extra permissions from Google.
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

# MEDIA_PHOTO_VIDEOS_PATH = FileSystemStorage(location='/media/photos_videos')

MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')
IMAGES_ROOT = MEDIA_ROOT + 'images/'
# PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


# print(STATIC_ROOT)

# PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
# STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
# print(STATIC_ROOT)
CORS_ORIGIN_ALLOW_ALL = True

# On production
CORS_ORIGIN_WHITELIST = ('http://localhost:3000',)

# CORS_ALLOWED_ORIGINS = ['*']

JITSI_SECRET = "0JJbsqPcqayuUiJftRadR0ilW137goLQgfxw5VjZxjDoBCtHfxqZhci5zllX8E6"
