from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import sqlite3
from rest_framework.viewsets import ReadOnlyModelViewSet


def connection():
    return sqlite3.connect("db.sqlite3")


def home(request):
    return render(request, "index.html")


@csrf_exempt
def update_part(request, part_id):
    part = json.loads(request.body)
    # this table is part of the ERP application, so I can't create a model for it, because it tries to create migrations
    value_pairs = ",".join(
        (
            "{key}='{value}'".format(key=key, value=value)
            if isinstance(value, (str, bool))
            else "{key}={value}".format(key=key, value=value)
            for key, value in part.items()
        )
    )
    try:
        with connection() as cursor:
            query = f"UPDATE part SET {value_pairs} WHERE id={part_id}"
            cursor.execute(query)
    except:
        return HttpResponse(status=500)

    return HttpResponse(status=200)
