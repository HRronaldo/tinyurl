import random
import json

from functools import wraps
from django.core.cache import cache
from django.http import HttpResponse


def generate_short_key():
    char_set = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
    short_key = ""
    for i in range(6):
        random_num = random.randint(0, 61)
        short_key += char_set[random_num]

    return short_key


def ratelimit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            host = args[0].headers['Referer']
        except Exception:
            return func(*args, **kwargs)

        count = cache.get(host)
        if count is None:
            count = 0

        # 判断这个 Ip 是否在操作很频繁
        if count >= 3:
            res = {
                "url": "The operation is too frequent, please try again later"
            }

            response = HttpResponse(json.dumps(res))

            return response
        else:
            count += 1
            cache.set(host, count, timeout=5)

        return func(*args, **kwargs)
    return wrapper

