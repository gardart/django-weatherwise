try:
    from settings_default import *
except ImportError:
    pass

#INTERNAL_IPS = ('127.0.0.1',)
#MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += (
#		'debug_toolbar',
		'weatherwane',
		)
