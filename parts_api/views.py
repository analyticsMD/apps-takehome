from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import sqlite3
from rest_framework.viewsets import ReadOnlyModelViewSet

connection = sqlite3.connect("db.sqlite3")


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
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE parts_api SET {value_pairs} WHERE id={part_id}".format(
                    value_pairs=value_pairs, part_id=part_id
                )
            )
    except:
        return HttpResponse(status=500)

    return HttpResponse(status=200)
