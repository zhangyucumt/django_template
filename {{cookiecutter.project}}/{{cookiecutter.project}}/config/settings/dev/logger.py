import sys

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'lineFormat': {
            '()': '{{cookiecutter.project}}.utils.log.RedStarLogFormatter'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'default': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'lineFormat',
            'stream': sys.stdout,
        }
    },
    'loggers': {
        '': {
            "level": "INFO",
            "handlers": ['default'],
            "propagate": False
        },
        'django': {
            'handlers': ['null'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}




