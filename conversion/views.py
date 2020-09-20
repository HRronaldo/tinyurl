import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

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
    row = Long2Short.objects.get(short_key=short_key)
    long_url = row.long_url
    row.visit_sum += 1
    row.modified_data = timezone.now()
    row.save()

    return HttpResponseRedirect(long_url)