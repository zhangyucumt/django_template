import functools

from rest_framework.serializers import BaseSerializer
from {{cookiecutter.project}}.exception import raise_system_error


def parse_request_with(parser_cls):
    """
    验证request.data 的参数
    :param parser_cls:
    :return:
    """
    def deco(func):
        func._parser_serializer = parser_cls()  # 该属性为自定义属性 对应 schema中的 serializer_fields

        @functools.wraps(func)
        def wrapper(cls, request, *args, **kwargs):
            if not issubclass(parser_cls, BaseSerializer):
                raise_system_error('invalid request parser')

            serializer = parser_cls(data=request.data)
            serializer.is_valid(raise_exception=True)
            kwargs.update(serializer.data)
            return func(cls, request, *args, **kwargs)

        return wrapper

    return deco


def allows_filters(func):
    """
    增加 _allows_filters  属性 可以在swagger中显示 filter_backends 中的参数
    :param func:
    :return:
    """
    func._allows_filters = True

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
