import logging
from django.http.response import Http404
from rest_framework import exceptions
from rest_framework.views import exception_handler as _exception_handler

from {{cookiecutter.project}} import exception as customer_exception

logger = logging.getLogger('{{cookiecutter.project}}.middleware.logging')


def exception_handler(exc, context):

    if isinstance(exc, customer_exception.BaseApiException):
        return exc.to_response()

    HandleClass = None
    detail = None
    if isinstance(exc, exceptions.AuthenticationFailed):
        HandleClass = HandleClass or customer_exception.AuthenticationFailed

    if isinstance(exc, exceptions.NotAuthenticated):
        HandleClass = HandleClass or customer_exception.NotAuthenticated

    if isinstance(exc, exceptions.PermissionDenied):
        HandleClass = HandleClass or customer_exception.PermissionDenied

    if isinstance(exc, exceptions.MethodNotAllowed):
        HandleClass = HandleClass or customer_exception.MethodNotAllowed

    if isinstance(exc, exceptions.ValidationError):
        if isinstance(exc.detail, dict):
            msg = ''
            for k, v in exc.detail.items():
                if isinstance(v, list):
                    msg += "%s-%s" % (k, '&'.join(v))
                else:
                    msg += '%s-%s' % (k, v)
        elif isinstance(exc.detail, list):
            msg = " ".join(map(str, exc.detail))
        else:
            msg = exc.detail
        HandleClass = HandleClass or customer_exception.ValidationError
        detail = detail or msg

    if isinstance(exc, exceptions.ParseError):
        HandleClass = HandleClass or customer_exception.ParseError

    if isinstance(exc, exceptions.NotFound):
        HandleClass = HandleClass or customer_exception.NotFound

    if isinstance(exc, Http404):
        HandleClass = HandleClass or customer_exception.PageNotFound

    if isinstance(exc, exceptions.APIException) and not HandleClass:
        HandleClass = HandleClass or customer_exception.APIException
        detail = detail or exc.detail

    if isinstance(exc, Exception) and not HandleClass:
        logger.error(msg=str(exc), exc_info=exc)
        HandleClass = HandleClass or customer_exception.APIException

    if HandleClass:
        handle_class = HandleClass(detail=detail)
        return handle_class.to_response()
    else:
        logger.debug('未处理的异常 - %s %s' % (exc, context))
        return _exception_handler(exc, context)

