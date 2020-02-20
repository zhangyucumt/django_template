import json
import sys
from logging import Formatter
from {{cookiecutter.project}}.middleware.logging import get_current_request


class RedStarLogFormatter(Formatter):

    def __init__(self):
        super(RedStarLogFormatter, self).__init__(
            fmt='[%(asctime)s] p%(process)s %(name)s %(filename)s:%(lineno)d %(levelname)s - %(message)s'
        )

    def format(self, record):
        request = get_current_request()
        if hasattr(record, "msg") and request:
            request_id = getattr(request, 'request_id', '')
            if request_id and request_id not in record.msg:
                user_id = getattr(getattr(request, "user", object), "id", "") or "NULL"
                record.msg = 'request_id:{} user_id:{} {}'.format(
                    request_id,
                    user_id,
                    record.msg
                )
        return super(RedStarLogFormatter, self).format(record)


class JsonLogFormatter(Formatter):
    def format(self, record):
        from {{cookiecutter.project}}.utils import JsonEncoder
        data = {
            'name': record.name,
            'asctime': self.formatTime(record),
            'process': record.process,
            'processname': record.processName,
            'thread': record.thread,
            'threadname': record.threadName,
            'filename': record.filename,
            'lineno': record.lineno,
            'levelname': record.levelname,
            'msg': record.msg
        }

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            s = ''
            if s[-1:] != "\n":
                s = s + "\n"
            try:
                s = s + record.exc_text
            except UnicodeError:
                s = s + record.exc_text.decode(sys.getfilesystemencoding(), 'replace')
            data['exception'] = s

        return json.dumps(data, cls=JsonEncoder)
