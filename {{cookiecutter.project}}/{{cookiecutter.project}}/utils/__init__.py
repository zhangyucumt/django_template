import os
import re
from collections import defaultdict
from django.conf import settings
from Crypto.Cipher import AES
import base64
import json
from datetime import datetime, date
from decimal import Decimal
from uuid import uuid4
import random
import importlib
import pkgutil
import inspect
import time
import arrow
import hashlib

from django.utils import six
from django.conf import settings
from django.utils import timezone


def update_config_recursively(old_data, new_data):
    for k, v in new_data.items():
        if isinstance(v, dict):
            if k not in old_data:
                old_data[k] = {}
            update_config_recursively(old_data[k], v)
        else:
            old_data[k] = v


class SimpleAesEncryption(object):
    def __init__(self, key=settings.SECRET_KEY[:16]):
        self.key = key
        self.mode = AES.MODE_CBC

    def encrypt(self, text):
        crypto = AES.new(self.key, self.mode, self.key)
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)
        crypto_text = crypto.encrypt(text)
        return base64.b64encode(crypto_text)

    def decrypt(self, text):
        crypto = AES.new(self.key, self.mode, self.key)
        plain_text = crypto.decrypt(base64.b64decode(text))
        return plain_text.rstrip('\0')


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def partial_update_instance(instance, update_dict):
    for key, val in update_dict.items():
        if hasattr(instance, key):
            setattr(instance, key, val)
    return True


def upload_file_with_raw_name(instance, filename, base_path):
    return os.path.join(base_path, uuid4().hex, filename)


def list_index_by(revert_list, key):
    """
    将字典组成的列表转化成按照字典中的某个字段的值为key的字典
    :param revert_list: etc. [{"color": "red", "sex": "male", "c": 3}, {"color": "black", "sex": "female", "c": 2}, ]
    :param key: "color"
    :return: {"red": {"color": "red", "sex": "male", "c": 3}, "black": {"color": "black", "sex": "female", "c": 2}}
    """
    return {c_dict[key]: c_dict for c_dict in revert_list}


def list_index_by_list_return(revert_list, key):
    """
    将字典组成的列表转化成按照字典中的某个字段的值为key的字典
    :param revert_list: etc. [{"color": "red", "sex": "male", "c": 3}, {"color": "black", "sex": "female", "c": 2}, ]
    :param key: "color"
    :return: {"red": [{"color": "red", "sex": "male", "c": 3}], "black": [{"color": "black", "sex": "female", "c": 2}]}
    """
    ret = defaultdict(list)
    for c_dict in revert_list:
        ret[c_dict[key]].append(c_dict)
    return ret


def gen_random_num_code(length=4):
    return random.choice(range(int("1" + "0" * (length - 1)), int("9" * length)))


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def obj_scanner(pkg, _filter, obj_type=inspect.isclass, depth=None):
    """
    :param pkg: a module instance or name of the module
    :param _filter: a function to filter matching classes
    :param obj_type: type in inspect
    :param depth: depth to scanner in pkg
    :return: all filtered obj
    """

    assert callable(obj_type) and obj_type.__module__ == 'inspect'

    if isinstance(pkg, str):
        pkg = importlib.import_module(pkg)

    objs = set()
    for importer, modname, ispkg in pkgutil.iter_modules(pkg.__path__):
        module = importlib.import_module('.' + modname, pkg.__name__)
        if ispkg:
            if depth is not None and isinstance(depth, int):
                depth -= 1
                if depth > 0:
                    objs |= obj_scanner(module, _filter, obj_type, depth)
            else:
                objs |= obj_scanner(module, _filter, obj_type, depth)
        else:
            obj_in_module = {
                cls[1] for cls in inspect.getmembers(module, obj_type) if _filter(cls[1])  # noqa
            }
            objs.update(obj_in_module)
    else:
        obj_in_module = {
            cls[1] for cls in inspect.getmembers(pkg, obj_type) if _filter(cls[1])  # noqa
        }
        objs.update(obj_in_module)
    return objs


def timestamp2datetime(timestamp):
    if isinstance(timestamp, six.string_types):
        if re.match(r'/^[\d]+$/', timestamp):
            timestamp = int(timestamp)
    elif not isinstance(timestamp, six.integer_types):
        return None

    if timestamp > 100000000000:
        timestamp = int(timestamp / 1000)

    return arrow.get(timestamp).to(settings.TIME_ZONE).datetime


def simple_md5_sign(data, secret_key):
    if not isinstance(data, dict) or not data:
        raise ValueError("data must be json")

    str_to_be_signed = "&".join(['='.join([str(k), str(v)]) for k, v in sorted(data.items())]) + "&key=" + secret_key

    return hashlib.md5(str_to_be_signed.encode("utf-8")).hexdigest()

