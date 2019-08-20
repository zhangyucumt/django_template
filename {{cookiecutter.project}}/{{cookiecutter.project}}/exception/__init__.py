from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException as RFWAPIException


class ErrorCode(object):
    SYSTEM_ERROR = 10000
    DATABASE_ERROR = 10001
    OBJECT_NOT_FOUND = 10002
    INFO_EXCEPTION = 10003
    PARAM_CHECK_FAILED = 10004
    PARSE_ERROR = 10005
    METHOD_NOT_ALLOW = 10006
    NOT_ACCEPTABLE = 10007
    UNSUPPORTED_MEDIA_TYPE = 10008
    THROTTLED = 10009
    PAGE_NOT_FOUND = 10010

    USER_NOT_EXIST = 20001
    PASSWORD_WRONG = 20002
    AUTH_FAILED = 20003
    NEED_LOGIN = 20004
    PERMISSION_DENIED = 20005


CODE_TRANSLATIONS = {
    ErrorCode.SYSTEM_ERROR: '系统异常',
    ErrorCode.DATABASE_ERROR: '数据系统异常',
    ErrorCode.OBJECT_NOT_FOUND: '请求对象不存在',
    ErrorCode.INFO_EXCEPTION: '',
    ErrorCode.PARAM_CHECK_FAILED: '验证参数失败',
    ErrorCode.PARSE_ERROR: "JSON格式错误",
    ErrorCode.METHOD_NOT_ALLOW: "请求方法不允许",
    ErrorCode.NOT_ACCEPTABLE: "非法的请求header参数",
    ErrorCode.UNSUPPORTED_MEDIA_TYPE: "无法处理该媒体类型",
    ErrorCode.THROTTLED: "请求速度太快，请销后再试",
    ErrorCode.PAGE_NOT_FOUND: "请求地址不存在",

    ErrorCode.USER_NOT_EXIST: '该用户不存在',
    ErrorCode.PASSWORD_WRONG: '密码错误',
    ErrorCode.AUTH_FAILED: '用户名或者密码不正确',
    ErrorCode.NEED_LOGIN: '您未登录',
    ErrorCode.PERMISSION_DENIED: '权限不足'

}


class BaseApiException(RFWAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = ErrorCode.SYSTEM_ERROR
    default_detail = None

    def __init__(self, detail=None, code=None):
        if code is None:
            code = self.default_code
        self.code = code
        if detail is None:
            detail = CODE_TRANSLATIONS.get(code) or self.default_detail
        super(BaseApiException, self).__init__(detail, code)

    def to_dict(self):
        return {
            'message': self.detail,
            'code': self.code,
        }

    def to_response(self):
        return Response(status=self.status_code, exception=True, data=self.to_dict())


class APIException(BaseApiException):
    """
    服务器异常
    """
    pass


class ValidationError(BaseApiException):
    """
    验证参数失败
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = ErrorCode.PARAM_CHECK_FAILED


class ParseError(BaseApiException):
    """
    json解析错误
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = ErrorCode.PARSE_ERROR


class AuthenticationFailed(BaseApiException):
    """
    账号密码不对
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = ErrorCode.AUTH_FAILED


class NotAuthenticated(BaseApiException):
    """
    未登录
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = ErrorCode.NEED_LOGIN


class PermissionDenied(BaseApiException):
    """
    无权限
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_code = ErrorCode.PERMISSION_DENIED


class NotFound(APIException):
    """
    对象未找到
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_code = ErrorCode.OBJECT_NOT_FOUND


class PageNotFound(APIException):
    """
    请求地址不存在
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_code = ErrorCode.PAGE_NOT_FOUND


class ObjectNotFound(APIException):
    """
    对象未找到
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_code = ErrorCode.OBJECT_NOT_FOUND


class MethodNotAllowed(APIException):
    """
    请求方法不允许
    """
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_code = ErrorCode.METHOD_NOT_ALLOW


class NotAcceptable(APIException):
    """
    无法处理的请求头
    """
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_code = ErrorCode.NOT_ACCEPTABLE


class UnsupportedMediaType(APIException):
    """
    不支持的媒体类型
    """
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    default_code = ErrorCode.UNSUPPORTED_MEDIA_TYPE


class Throttled(APIException):
    """
    请求超限
    """
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_code = ErrorCode.THROTTLED


def raise_system_error(message):
    raise APIException(
        detail=message
    )


def raise_invalid_param(code=None, message=None):
    code = code or ErrorCode.PARAM_CHECK_FAILED
    message = message or CODE_TRANSLATIONS.get(code, None)
    raise ValidationError(
        code=code,
        detail=message
    )


def raise_need_login():
    raise NotAuthenticated()


def raise_permission_denied():
    raise PermissionDenied()
