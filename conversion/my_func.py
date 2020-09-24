import random
import json

from functools import wraps
from django.core.cache import cache
from django.http import HttpResponse

char_set = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"


def generate_short_key():
    short_key = ""
    for i in range(6):
        random_num = random.randint(0, 61)
        short_key += char_set[random_num]

    return short_key


def id_2_short_key(fid, alphabet=char_set):
    if fid == 0:
        return alphabet[0]

    arr = []
    base = len(alphabet)
    while fid:
        fid, rem = divmod(fid, base)
        arr.append(alphabet[rem])
    arr.reverse()

    return ''.join(arr)


def short_key_2_id (short_key):
    digit = 0
    fid = 0
    for i in short_key[::-1]:
        num = char_set.find(i)
        fid += num * 62 ** digit
        digit += 1

    return fid


def ratelimiter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            ip_address = args[0].headers['Referer']

            count = cache.get(ip_address)
            if count is None:
                count = 0

            # 5秒最多访问5次
            if count >= 5:
                res = {
                    "url": "The operation is too frequent, please try again later"
                }
                response = HttpResponse(json.dumps(res))

                return response
            else:
                count += 1
                cache.set(ip_address, count, timeout=5)

            return func(*args, **kwargs)

        except Exception:
            return func(*args, **kwargs)

    return wrapper


if __name__ == "__main__":
    print(id_2_short_key(10008349))
    print(short_key_2_id('H0D0'))