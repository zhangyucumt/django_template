import sys
import logging.config

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'lineFormat': {
            '()': '{{cookiecutter.project}}.utils.log.RedStarLogFormatter'
        }
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'lineFormat',
            'stream': sys.stdout,
        }
    },
    'loggers': {
        '': {
            "level": "DEBUG",
            "handlers": ['default'],
            "propagate": False
        }
    }
}

logging.config.dictConfig(logging_config)


