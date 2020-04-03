import functools
import pickle

from rest_framework.serializers import BaseSerializer
from {{cookiecutter.project}}.exception import raise_system_error


def parse_request_with(parser_cls, partial=False, with_instance=False):
    """
    验证request.data 的参数
    :param parser_cls:
    :param partial: 是否部分
    :param with_instance: 是否有实例对象
    :return:
    """
    def deco(func):
        func._parser_serializer = parser_cls()  # 该属性为自定义属性 对应 schema中的 serializer_fields

        @functools.wraps(func)
        def wrapper(cls, request, *args, **kwargs):
            if not issubclass(parser_cls, BaseSerializer):
                raise_system_error('invalid request parser')
            if not with_instance:
                serializer = parser_cls(data=request.data, context={'request': request}, partial=partial)
            else:
                instance = cls.get_object()
                serializer = parser_cls(instance=instance, data=request.data, context={'request': request}, partial=partial)
            serializer.is_valid(raise_exception=True)
            return func(cls, request, *args, validate_data=serializer.validated_data, serializer=serializer, **kwargs)

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


class memorize(dict):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result

 
def save_result_to_cache(key, expire):
    def deco(missing_func):
        @functools.wraps(missing_func)
        def wrapper(*args, **kwargs):

            current_cache = cache[cache_backend]
            cache_key = key
            if re.search(r'{\w*}', key):
                cache_key = key.format(*args, **kwargs)
            cached_value = current_cache.get(cache_key)
            if cached_value is not None:
                return pickle.loads(cached_value)
            else:
                v = missing_func(*args, **kwargs)
                current_cache.set(cache_key, pickle.dumps(v), expire)
                return v
        return wrapper
    return deco
