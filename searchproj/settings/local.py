'''
created on 07/30/2013

@author rise riyo
'''
#**********************************************
# settings/local.py: contains exclusive
# server specific and sensitive settings such
# as db username and password, API keys, or
# secret key, etc. and have settings.py import
# all of these values
#**********************************************
# import django core imports; 


# import 3rd party apps

# import project imports; see settings/base.py 
try:
        from .base import *
except ImportError:
        pass

###################### MANAGER CONFIGURATION
ADMINS = (
    # ('nugget', 'nugget.doe@egmail.com'),
)

MANAGERS = ADMINS
###################### END MANAGER CONFIGURATION


################### SECRET CONFIGURATION
# Make this unique, and don't share it with anybody.
SECRET_KEY = get_env_variable('SECRET_KEY_SEARCHENG') 

################### END SECRET CONFIGURATION

###################### EMAIL CONFIGURATION
if LOCAL:
        # No access to SMTP server, then use the following and
        # in terminal enter: python -m smtpd -n -c DebuggingServer localhost:1025
        #EMAIL_USE_TLS = False
        #EMAIL_HOST = 'localhost'
        #EMAIL_HOST_USER = ''
        #EMAIL_HOST_PASSWORD = ''
        #EMAIL_PORT = 1025
        #DEFAULT_FROM_EMAIL = 'testing@example.com'


        # Email settings for sending account activation mail messages
        # Configured mail server use the following; otherwise, add
        # Gmail's SMTP server setting: smtp.gmail.com
        # ask me for these settings...
        EMAIL_USE_TLS = True
        EMAIL_HOST = "smtp.gmail.com"
        EMAIL_HOST_USER = "molecularflipbook@gmail.com"
        EMAIL_HOST_PASSWORD = "Mfbteam1"
        EMAIL_PORT = 587
        DEFAULT_FROM_EMAIL = 'molecularflipbook@gmail.com'
###################### END EMAIL CONFIGURATION

################### DEBUG CONFIGURATION 
DEBUG = True #"DEBUG_MODE" in os.environ
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG


# tuple that specifies the full python path to the order of displayed panel
DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
)

def show_toolbar(request):
        return True # always show toolbar, for example purposes only

DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
        #'EXTRA_SIGNALS': '',
        'HIDE_DJANGO_SQL': False,
        #'SHOW_TEMPLATE_CONTEXT':False,
        #'TAG': 'body',                                 # defaults to <body>
        'ENABLE_STACKTRACES': True,
        #'DEBUG_TOOLBAR_MEDIA_URL': '/'
}

# django_debug_toolbar: required list or tuple for the built-in show_toolbar method
INTERNAL_IPS = ('127.0.0.1',)


MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
)
################### END DEBUG CONFIGURATION


###################### GENERAL CONFIGURATION

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = LOCALTZ
################### END GENERAL CONFIGURATION


###################### APP CONFIGURATION
INSTALLED_APPS = INSTALLED_APPS + (
        'debug_toolbar',
)
################### END APP CONFIGURATION