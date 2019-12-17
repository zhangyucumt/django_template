from django.conf import settings
from Crypto.Cipher import AES
import base64
import json
from datetime import datetime, date
from decimal import Decimal


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
