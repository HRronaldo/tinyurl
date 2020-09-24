import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.utils import timezone
from django.core.cache import cache

from .models import Long2Short, Long2ShortV2
from .my_func import generate_short_key, id_2_short_key, short_key_2_id, ratelimiter
from tinyurl.settings import TinyurlDOMIAN


def index(request):
    return render(request, 'conversion/index.html')


@ratelimiter
def long_2_short(request):
    try:
        ip_address = request.headers['Referer']
        url = json.loads(request.body)['url']

        # 判断 url 是长链接还是短链接
        if TinyurlDOMIAN in url:
            res = {
                "url": "Please enter long url"
            }
            response = HttpResponse(json.dumps(res))

            return response

        long_url = url

        # 查询缓存，如果 short_url 存在，则返回 short_url
        short_url = cache.get(long_url)
        if short_url:
            res = {
                "url": short_url
            }
            response = HttpResponse(json.dumps(res))

            return response

        # 如果 short_url 不存在，则生成一个新的 short_key
        short_key = generate_short_key()

        # 判断 short_key 是否在数据库中已经存在，如果存在则重新生成
        while Long2Short.objects.filter(short_key=short_key):
            short_key = generate_short_key()

        # 保存数据到数据库
        lts = Long2Short(
            long_url=long_url,
            short_key=short_key,
            create_date=timezone.now(),
            ip_address=ip_address,
        )
        lts.save()

        short_url = TinyurlDOMIAN + "/tinyurl/" + short_key + "/"

        # 更新缓存
        cache.set(long_url, short_url, timeout=60 * 60 * 24)
        cache.set(short_key, long_url, timeout=60 * 60 * 24)

        res = {
            "url": short_url
        }
        response = HttpResponse(json.dumps(res))

        return response

    except Exception as e:
        res = {
            "url": 'Internal server error',
        }
        response = HttpResponse(json.dumps(res))

        return response


def short_2_long(request, short_key):
    long_url = cache.get(short_key)
    if long_url:
        return HttpResponsePermanentRedirect(long_url)
    else:
        row = Long2Short.objects.get(short_key=short_key)
        long_url = row.long_url

        # 更新缓存
        cache.set(short_key, long_url, timeout=60 * 60 * 24)

        return HttpResponsePermanentRedirect(long_url)


def long_2_short_v2(request):
    try:
        ip_address = request.headers['Referer']
        url = json.loads(request.body)['url']

        # 判断 url 是长链接还是短链接
        if TinyurlDOMIAN in url:
            res = {
                "url": "Please enter long url"
            }
            response = HttpResponse(json.dumps(res))

            return response

        long_url = url

        # 查询缓存，如果 short_url 存在，则返回 short_url
        short_url = cache.get(long_url)
        if short_url:
            res = {
                "url": short_url
            }
            response = HttpResponse(json.dumps(res))

            return response

        # 保存数据到数据库
        lts = Long2ShortV2(
            long_url=long_url,
            create_date=timezone.now(),
            ip_address=ip_address,
        )
        lts.save()

        fid = lts.id
        short_key = id_2_short_key(fid)
        short_url = TinyurlDOMIAN + "/tinyurl/" + short_key + "/"

        # 更新缓存
        cache.set(long_url, short_url, timeout=60 * 60 * 24)
        cache.set(short_key, long_url, timeout=60 * 60 * 24)

        res = {
            "url": short_url
        }
        response = HttpResponse(json.dumps(res))

        return response

    except Exception:
        res = {
            "url": 'Internal server error',
        }
        response = HttpResponse(json.dumps(res))

        return response


def short_2_long_v2(request, short_key):
    long_url = cache.get(short_key)
    if long_url:
        return HttpResponsePermanentRedirect(long_url)
    else:
        fid = short_key_2_id(short_key)
        row = Long2ShortV2.objects.get(id=fid)
        long_url = row.long_url

        # 更新缓存
        cache.set(short_key, long_url, timeout=60 * 60 * 24)

        return HttpResponsePermanentRedirect(long_url)