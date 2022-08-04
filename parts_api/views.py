import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from parts_api.models import Part


def home(request):
    return render(request, "index.html")


@csrf_exempt
@require_http_methods(["PUT"])
def update_part(request, part_id):
    value_pairs = json.loads(request.body)
    part = Part.objects.filter(id=part_id)

    if not part:
        return HttpResponse(status=404)

    try:
        part.update(**value_pairs)
    except:
        return HttpResponse(status=500)

    return HttpResponse(status=200)
