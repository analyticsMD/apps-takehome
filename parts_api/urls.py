from django.conf.urls import url
from django.contrib import admin

from parts_api import views

urlpatterns = [
    url(r"^$", views.home, name="home"),
    url("admin/", admin.site.urls),
    url("part/update/(?P<part_id>\d+)/$", views.update_part),
]
