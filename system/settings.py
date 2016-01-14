"""
Django settings for system project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import tempfile
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages",
"customers.context_processors.usuario",
)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cv*2n!28j*_p(+6%nn%)&@d^x1w75$bimq9bxfcv9hl(&&t=!7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

USE_TZ=True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'proyects',
    'payments',
    'customers',
    'developers',
    'contents',
    'servicios',
    'postman',
    'support',
    'fileupload',
    'ckeditor',
    'allaccess', 
    'djrill',
    'pinax.notifications',
    'paypal.standard.ipn',
    "django_cron",
)

SITE_ID = 1


AUTHENTICATION_BACKENDS = (
    # Default backend
    'django.contrib.auth.backends.ModelBackend',
    # Additional backend
    'allaccess.backends.AuthorizedServiceBackend',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

#Crons
CRON_CLASSES = [
    "servicios.crons.ComputeDate",
    # ...
]



LOGIN_REDIRECT_URL = '/customer/process'

TEMPLATE_DIRS = (
    BASE_DIR + '/templates/',
)

ROOT_URLCONF = 'system.urls'

WSGI_APPLICATION = 'system.wsgi.application'

POSTMAN_DISALLOW_ANONYMOUS = True
POSTMAN_DISALLOW_COPIES_ON_REPLY = True
POSTMAN_AUTO_MODERATE_AS = True
#POSTMAN_NOTIFIER_APP = 'pinax.notifications'
POSTMAN_MAILER_APP = 'django.core.mail' 
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases


DEFAULT_FROM_EMAIL = 'contacto@serverticsup.com'
#Email Setting
MANDRILL_API_KEY = "tuK68gZttFdaUESJZ-brSA"
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
#EMAIL_BACKEND = 'django_mailer.smtp_queue.EmailBackend'
# Host for sending e-mail.
#EMAIL_HOST = 'smtp.mandrillapp.com'

# Port for sending e-mail.
#EMAIL_PORT = 587

# Optional SMTP authentication information for EMAIL_HOST.
#EMAIL_HOST_USER = 'albertisfu@gmail.com'
#EMAIL_HOST_PASSWORD = 'tuK68gZttFdaUESJZ-brSA'
#EMAIL_USE_TLS = True




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


#Paypal
PAYPAL_RECEIVER_EMAIL = "admin@ticsup.com"
PAYPAL_TEST = True
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ =  False


MEDIA_ROOT = BASE_DIR
MEDIA_URL = '/'

#CKE Editor
CKEDITOR_CONFIGS = {
    'text': {
         'language' :'es-es',
    'uiColor': '#F3F3F4',

    'disableNativeSpellChecker': False,
'removePlugins': 'contextmenu,liststyle,tabletools',
'toolbar': [
        { 'name': 'basicstyles', 'groups': [ 'basicstyles', 'cleanup' ], 'items': [ 'Bold', 'Italic', 'Underline', 'Strike',] },
        [ 'Paste', 'PasteFromWord', '-', 'Undo', 'Redo' ],                                                                                        
        { 'name': 'paragraph', 'groups': [ 'list', 'indent', 'blocks', 'align', 'bidi' ], 'items': [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', ] },
        { 'name': 'links', 'items': [ 'Link', 'Unlink', ] },
        { 'name': 'insert', 'items': [ 'Image', 'Table', 'Smiley', 'SpecialChar', ] },
        '/',
    { 'name': 'styles', 'items': [ 'Styles', 'Format', 'FontSize' ] },
    { 'name': 'colors', 'items': [ 'TextColor', 'BGColor' ] },
     { 'name': 'document', 'items': [ 'Source',] }, 
    ],

    },
}
CKEDITOR_UPLOAD_PATH = BASE_DIR + '/static/uploads'
#STATIC_ROOT = os.path.join(tempfile.gettempdir(), 'ck_static')
#MEDIA_ROOT = os.path.join(tempfile.gettempdir(), 'ck_media')
#CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

#encripted
ENCRYPTED_FIELDS_KEYDIR = BASE_DIR + '/static/fieldkeys'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),

)


