import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.core.cache import cache

from .models import Long2Short
from .my_func import generate_short_key

TinyurlDOMIAN = 'http://192.168.33.11:8080'


def index(request):
    return HttpResponse("This is an index")


def long_2_short(request):
    url_dict = json.loads(request.body)
    url = url_dict['url']
    # host = request.headers['Referer']
    host = "192.168.33.11"

    count = cache.get(host)
    if count is None:
        count = 0

    # 判断这个 Ip 是否在操作很频繁
    if count >= 3:
        res = {
            "url": "The operation is too frequent, please try again later"
        }

        response = HttpResponse(json.dumps(res))
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"

        return response
    else:
        count += 1
        cache.set(host, count, timeout=5)

    # 判断 url 是长链接还是短链接
    if TinyurlDOMIAN in url:
        res = {
            "url": "Please enter long url"
        }

        response = HttpResponse(json.dumps(res))
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"

        return response

    long_url = url

    # 查询缓存，如果 short_url 存在，则返回 short_url
    short_url = cache.get(long_url)
    if short_url:
        res = {
            "url": short_url
        }

        response = HttpResponse(json.dumps(res))
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"

        return response

    # 如果 short_url 不存在，则生成一个新的 short_key
    short_key = generate_short_key()

    # 判断 short_key 是否在数据库中已经存在，如果存在则重新生成
    while Long2Short.objects.filter(short_key=short_key):
        short_key = generate_short_key()

    # 保存数据到数据库
    lst = Long2Short(
        long_url=long_url,
        short_key=short_key,
        create_date=timezone.now(),
        ip_address=host,
    )
    lst.save()

    short_url = TinyurlDOMIAN + "/tinyurl/" + short_key + "/"

    # 更新缓存
    cache.set(long_url, short_url, timeout=60 * 60 * 24)
    cache.set(short_key, long_url, timeout=60 * 60 * 24)

    res = {
        "url": short_url
    }

    response = HttpResponse(json.dumps(res))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"

    return response


def short_2_long(request, short_key):
    long_url = cache.get(short_key)
    if long_url:
        return HttpResponseRedirect(long_url)
    else:
        row = Long2Short.objects.get(short_key=short_key)
        long_url = row.long_url

        # 更新缓存
        cache.set(short_key, long_url, timeout=60 * 60 * 24)

        return HttpResponseRedirect(long_url)
