import json

from django.shortcuts import render
from django.http import HttpResponse

from conversion.models import Long2Short


def history(request):
    host = "192.168.33.11"
    url_history = Long2Short.objects.filter(ip_address=host).order_by("-create_date")[:5].values()
    rows = []
    for i in url_history:
        i["create_date"] = i["create_date"].strftime("%Y-%m-%d %H:%M:%S")
        rows.append(i)
    res = {
        "data": rows
    }

    response = HttpResponse(json.dumps(res))

    return response
