import sys

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'jsonFormat': {
            '()': '{{cookiecutter.project}}.utils.log.JsonLogFormatter'
        },
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
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        '{{cookiecutter.project}}': {
            "level": "DEBUG",
            "handlers": ['default'],
            "propagate": False
        }
    }
}
