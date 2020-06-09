import os

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
        'api_info': {
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'filename': os.path.join('/logs', 'api_info.log'),
            'level': 'DEBUG',
            'formatter': 'lineFormat',
            'delay': True,
            'maxBytes': 1024 * 1024 * 500,
            'backupCount': 1
        },
        'api_error': {
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'filename': os.path.join('/logs', 'api_warning.log'),
            'level': 'ERROR',
            'formatter': 'lineFormat',
            'delay': True,
            'maxBytes': 1024 * 1024 * 500,
            'backupCount': 1
        },
        'rpc': {
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'filename': os.path.join('/logs', 'rpc.log'),
            'level': 'INFO',
            'formatter': 'lineFormat',
            'delay': True,
            'maxBytes': 1024 * 1024 * 500,
            'backupCount': 1
        },
        'message': {
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'filename': os.path.join('/logs', 'message.log'),
            'level': 'INFO',
            'formatter': 'lineFormat',
            'delay': True,
            'maxBytes': 1024 * 1024 * 500,
            'backupCount': 1
        },
        'default': {
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'filename': os.path.join('/logs', 'api_info.log'),
            'level': 'INFO',
            'formatter': 'lineFormat',
            'delay': True,
            'maxBytes': 1024 * 1024 * 500,
            'backupCount': 1
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        '{{cookiecutter.project}}.middleware.logging': {           # 访问流水日志
            "level": "DEBUG",
            "handlers": ['api_info', 'api_error'],
            "propagate": False
        },
        '{{cookiecutter.project}}.rpc': {                  # rpc调用的日志
            "level": "DEBUG",
            "handlers": ['rpc'],
            "propagate": False
        },
        'message': {                    # 重要信息的记录
            "level": "DEBUG",
            "handlers": ['message'],
            "propagate": False
        },
        '{{cookiecutter.project}}': {                           # 其他的业务日志
            "level": "DEBUG",
            "handlers": ['default'],
            "propagate": False
        }
    }
}
