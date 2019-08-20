import logging
import uuid
import time
import threading
import json

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object
from django.http import JsonResponse

logger = logging.getLogger(__name__)

local = threading.local()


def get_current_request():
    return getattr(local, 'request', None)


def get_current_user():
    request = get_current_request()
    if request:
        return getattr(request, 'user', None)


class LoggingMiddleware(MiddlewareMixin):
    """
    记录请求log
    """
    _initial_http_body = None

    def process_request(self, request):
        request_id = self._get_request_id(request)
        request.request_id = request_id
        request.start_at = time.time()
        local.request = request
        self._initial_http_body = request.body

    def process_exception(self, request, exc_info):
        from {{cookiecutter.project}}.exception import APIException
        response = JsonResponse(APIException().to_dict(), status=500)
        self.log_data(request, response, exc_info)
        return response

    def process_response(self, request, response):
        response['X-Request-Id'] = getattr(request, 'request_id', '')
        self.log_data(request, response)
        return response

    def _get_request_id(self, request):
        return request.META.get('HTTP_REQUEST_ID') or str(uuid.uuid4())

    def log_data(self, request, response, exc_info=None):
        if response.status_code >= 500:
            level = 'error'
        elif response.status_code >= 400:
            level = 'warning'
        else:
            level = 'info'
        message = self._gen_log_data(request, response, exc_info=exc_info)
        getattr(logger, level)(
            message,
            extra={
                'status_code': response.status_code,
                'request': request,
            },
            exc_info=exc_info,
        )

    def _gen_log_data(self, request, response, exc_info=None):
        http_method = request.method
        path_info = request.get_full_path_info()

        logger_fmt = '{normal_meta}, {time_meta}, {response}'

        json_data = request.POST.dict()
        if not json_data:
            try:
                json_data = json.loads(self._initial_http_body.decode('utf-8'))
            except:
                pass

        if json_data:
            for sensitive_data in ['password', 'pwd', 'secret_key']:
                if sensitive_data in json_data:
                    del json_data[sensitive_data]

        normal_meta = '<{http_method} {path_info}> {json} [{status_code}]'.format(
            http_method=http_method,
            path_info=path_info,
            json=json_data,
            status_code=response.status_code
        )
        time_meta = 'cost: {time}s'.format(time=time.time() - request.start_at)

        log_meta = dict(
            normal_meta=normal_meta,
            time_meta=time_meta,
        )
        if exc_info:
            log_meta['response'] = str(exc_info)
        elif http_method.lower() == 'get':
            log_meta['response'] = ''
        else:
            log_meta['response'] = response.content.decode('utf-8')
        try:
            return logger_fmt.format(**log_meta)
        except:
            log_meta['response'] = ""
            return logger_fmt.format(**log_meta)
