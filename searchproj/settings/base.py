# Django settings for searchproj project.
# stdlib imports
from os.path import join, abspath, dirname
import os
import logging

logger = logging.getLogger(__name__)

# third party plugins
#from unipath import Path

# django core
# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    """Get the environment variable or return exception"""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)


###################### PATH CONFIGURATION
LOCAL = True

#REPO_ROOT = os.path.dirname(os.path.)
#PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
#print abspath(dirname(__file__))
here = lambda *x: join(abspath(dirname(__file__)), *x)
PROJECT_ROOT = here("..")
root = lambda *x: join(abspath(PROJECT_ROOT), *x)
print "project_root = %s" %PROJECT_ROOT

#rel = lambda p: os.path.join(PROJECT_ROOT, p)

###################### END PATH CONFIGURATION


####################### DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': get_env_variable('SECRET_DATABASE'), # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': get_env_variable('SECRET_DATABASE_NAME'),                            # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',             # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
        'OPTIONS': {'autocommit': True,},
    }
}
####################### END DATABASE CONFIGURATION 

########### USER PROFILE CONFIGURATION
#AUTH_USER_MODEL = "profiles.UserProfile"

######################## HAYSTACK CONFIGURATION
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },

    'autocomplete': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'hs_autocomplete',
    },
}

# enable signal processor that updates the index with additions/deletions
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
######################## END HAYSTACK CONFIGURATION


########################## REGISTRATION CONFIGURATION
ACCOUNT_ACTIVATION_DAYS = 2

########################## END REGISTRATION CONFIGURATION

###################### GENERAL CONFIGURATION
# provide our get_profile()
AUTH_PROFILE_MODULE = 'profiles.UserProfile'

ACCOUNT_ACTIVATION_DAYS = 2

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
LOCALTZ = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True
###################### END GENERAL CONFIGURATION


###################### MEDIA CONFIGURATION
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
#MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_ROOT = root("media")
print MEDIA_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# URL prefix for admin static files, i.e., CSS, JS, and images; must use trailing slash.
ADMIN_MEDIA_PREFIX = '/static/admin/'
###################### END MEDIA CONFIGURATION


###################### STATIC CONFIGURATION
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
#STATIC_ROOT = os.path.join(PROJECT_ROOT,'templates')
STATIC_ROOT = root("templates")
print ("templates/static is %s")%STATIC_ROOT

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    root("static"), 
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
###################### END STATIC CONFIGURATION


###################### TEMPLATE CONFIGURATION

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

#TEMPLATE_DIRS = os.path.join(PROJECT_ROOT, "templates"),
TEMPLATE_DIRS = (
    root("templates"), 
)

print ("template_dirs is %s")%TEMPLATE_DIRS

#TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
#)
###################### END TEMPLATE CONFIGURATION


###################### MIDDLEWARE CONFIGURATION
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
###################### END MIDDLEWARE CONFIGURATION


###################### URL CONFIGURATION
ROOT_URLCONF = 'searchconfig.urls'
###################### END URL CONFIGURATION


###################### WSGI CONFIGURATION
# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'searchconfig.wsgi.application'
###################### END WSGI CONFIGURATION


###################### APP CONFIGURATION
DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    'south',
    'haystack',
    'easy_thumbnails',
    'django_extensions',
)

LOCAL_APPS = (
    'profiles',
    'notes',
    'uploads',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
######################## END APP CONFIGURATION


###################### LOGGING CONFIGURATION
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
###################### END LOGGING CONFIGURATION
