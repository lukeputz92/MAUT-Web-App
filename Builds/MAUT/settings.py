
"""
Django settings for MAUT project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$^@@m)=r)t=qvekpf03&@x7t%y-#a$=k1-tu@*nht-t-@(c=@$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['maut.pythonanywhere.com', '127.0.0.1', 'localhost']

CSRF_USE_SESSIONS = True
# Application definition

INSTALLED_APPS = (
    'social_django',
    'decisions',
    'colleges',
    'books',
    'restaurants',
	'tutorial',
    'cars',
    'movies',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_static_jquery',
)

MIDDLEWARE_CLASSES = (
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
       'django.contrib.sessions.middleware.SessionMiddleware',
     'django.contrib.sessions.models.Session',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

)

ROOT_URLCONF = 'MAUT.urls'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

WSGI_APPLICATION = 'MAUT.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)
# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PROFILE_MODULE = 'accounts.UserProfile'
# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [STATIC_DIR,]
#STATIC_ROOT = (os.path.join(BASE_DIR, 'static'))
LOGIN_REDIRECT_URL = '/profile/home'
#LOGOUT_REDIRECT_URL = 'registration/login.html'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'MAUtilityTheory@gmail.com'
EMAIL_HOST_PASSWORD = 'gonzalez2000#'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


CLICKY_SITE_ID = 'maut'

SOCIAL_AUTH_GITHUB_KEY = '435edbaa28740e017d42'
SOCIAL_AUTH_GITHUB_SECRET = 'fd249117f7f1c76865cc20093b1469d37edcdb61'

SOCIAL_AUTH_TWITTER_KEY = 'lgDffpekDxtsNTqQkihUpkb5G'
SOCIAL_AUTH_TWITTER_SECRET = 'KueW7hmYm8VuVkixPK2jWp50IqFnZCsWd9ljbrrIo06MoQT3qm'

SOCIAL_AUTH_FACEBOOK_KEY = '419225881839270'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = 'b0765dd8a03284268fee339f5797a4d1'  # App Secret