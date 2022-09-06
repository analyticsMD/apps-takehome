import json

from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, "index.html")


@csrf_exempt
def update_part(request, part_id):
    part = json.loads(request.body.decode())
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
    except Exception as e:
        return HttpResponse(200)

    return HttpResponse(200)
