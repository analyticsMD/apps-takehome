from django.contrib import admin
from django.conf.urls import include, url
from parts_api import views

urlpatterns = [
    url(r"^$", views.home, name="home"),
    url("admin/", admin.site.urls),
    url("part/update/(?P<part_id>\d+)/$", views.update_part, name="part-update"),
]
