from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import sqlite3
from rest_framework.viewsets import ReadOnlyModelViewSet

# Moved connection object inside of the function to avoid issue: An Error ocurred: SQLite objects 
# created in a thread can only be used in that same thread

# connection = sqlite3.connect("db.sqlite3")

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

    # Including try to handle possible errors.
    try:
        connection = sqlite3.connect("db.sqlite3")
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM part WHERE id = {part_id}") 

        rows = cursor.fetchall()

        if not rows:
            response = {
                "message": f"Part id {part_id} not found"
            }
            return HttpResponse(json.dumps(response), status=404, content_type ="application/json")

        # table is callled part, not parts_api, name of table was wrong.
        cursor.execute(
            "UPDATE part SET {value_pairs} WHERE id={part_id}".format(
                value_pairs=value_pairs, part_id=part_id
            )
        )
        connection.commit()
        cursor.close()
    except Exception as e:
        response = {
        'message': f"An Error ocurred: {e}"
        }
        return HttpResponse(json.dumps(response), status=500, content_type ="application/json")

    response = {
        'part_id': part_id,
        'new_data': part,
        'message': "Part was upated successfully"
    }

    return HttpResponse(json.dumps(response), status=200, content_type ="application/json")


