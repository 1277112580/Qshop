"""
Django settings for Qshop project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l(+d3$c-n+ens#-nlc!o4+h*c%)@&5-@1t$@6flz8-@e8xk+6='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Buyer',
    'Saller',
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

ROOT_URLCONF = 'Qshop.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'Qshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS=(
    os.path.join(BASE_DIR,'static'),
)
# 和上下两条冲突
# 静态文件收集 将其他冲突的注释掉
# STATIC_ROOT=os.path.join(BASE_DIR,'static')

# 媒体文件
MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'static')


# 公钥
alipay_public_key_string="""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtexG8P2qyi04DUrUEQnbpfCYS7im27E0q55gsDiE+g/JdWwJJ3/I2PRPbyz38ah2mv66GFdE4j2nXarL3jSgoP995mZzmllGLDSOWbFI2QB+7ZMikVFXzjWZ68FcQMEJExuC7ikD4vuY8J4Wt00NerbSwKCWL4CjvV3CxcBaJXPn3kIOzItX0yDToK9rvZ9E4P1PIURe96Q/SNz+GkJaR32PQJotUOrsg0gVdWhSBIjRuSpvUpUlPEZrzprhyYn/zZ6TktKaURzfVqSpRa0h+Z9y03sIIDVLSWRlaDKw81WsVKfJlUcN9WA/uypMOOQb6MXolZEYMRm+EDgEFT0oUQIDAQAB
-----END PUBLIC KEY-----"""

# 私钥
alipay_private_key_string="""-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAtexG8P2qyi04DUrUEQnbpfCYS7im27E0q55gsDiE+g/JdWwJJ3/I2PRPbyz38ah2mv66GFdE4j2nXarL3jSgoP995mZzmllGLDSOWbFI2QB+7ZMikVFXzjWZ68FcQMEJExuC7ikD4vuY8J4Wt00NerbSwKCWL4CjvV3CxcBaJXPn3kIOzItX0yDToK9rvZ9E4P1PIURe96Q/SNz+GkJaR32PQJotUOrsg0gVdWhSBIjRuSpvUpUlPEZrzprhyYn/zZ6TktKaURzfVqSpRa0h+Z9y03sIIDVLSWRlaDKw81WsVKfJlUcN9WA/uypMOOQb6MXolZEYMRm+EDgEFT0oUQIDAQABAoIBAGDUC8ZFHdxSSR06ELmo55HhBw52j8kq/n/B4nCpBI4cTPwErrKpXvuqvYTNCINFSSuiHObLvEw2yJggSjZRCJXoptg0+57RmXn51zKCG+X0T5qfz6xNAVEuUmibGEEW/X+ACyY8CmeLxpF7c1fI2T3RhUclsgpCi+REvWCHyvNXYIj5S8c3+KBXGzdmmwv97PTtkkMW4K2QDG9wcimZU/stUrtsx8vBm9T4TmDz3BiXnCHoJDJCx5j9R8MlrT2hD2HdwxjZzMNBveHNdDK2mWrCVnzNzJiUnBPxh0ObJU+Qf9g32Gmyn/8QZbRDDiN6az+NWiMJx/ikPQTB4QWdYckCgYEA8YSEAVCU8bTmRDS//uOB6sGzt1KDG3fmTuSuupoJT4FC7UiUg0eo3ZfvqHrowkVccEgRgKCtUpWNrR1SzheXvc8QajeLqGP3dk5vI2naseqCE1nhqW0i8BRezjrPiWxkzG4aNO2BLTco+ZV7AJYW0E0hMW2YDu9kqrCRzV2PVZcCgYEAwNTvwwEFW2LZwv8gzITqg9S71phz0u4DSvkvlm57FO2G/RWwp5S7ukvLPgOgVHVymFsfUQy2J0HcvqFysvyJulj+PHK9onddnm8msrLsUG66ui1QrIUP06p2v98IaG2jKJxFCX79XPr67UgKXq8kX/s491NkHq774pdUy9InvlcCgYBnp2b8JXh3MBtvhHAuVbgpZ87Yy/nm7ROUIoN3JKsAS0rNCcxrd3La/91korOIxToCGnwgh1U7z2HJvX8PYoLGfLrfy00ODTFkvg7m1QR+PVZsNbQrAeLvxN5XhlgR88pjDpICyzgYjsbwLx5mRwQtjBzF2PJc3pOGylcZG6FrqwKBgQCUoQwU0Cqi37RdGmzbdu+ToVsO8v8Da7VaCmtllc6EuPg9BoTdBkUUOOt05zKjJsunJ0UiIZwc8iUFQke4MfKukX2UdhQ4r6yXO7EmN8bx0AdZDSiLcRxb154kEfLXGvqRiLGluh3rlv/l+IsVpAVzfZ3Q9JPNGq7HXkFbwKYljQKBgGO9dozcq7hspOEsM+tlN2Z21SxM3mK+udOntXw+xD3iSbksiI9GOmHs09Np/95TN21lwl1h7r40/5rxC6s0cfrPd+7c0QhsgM9yOE1onkazY5DLmGDaW979HZLuB1y4V2ksw2ttJfirRtHPYRBcHS/XVmEzTUGk4zfqA4lkQ15x
-----END RSA PRIVATE KEY-----"""