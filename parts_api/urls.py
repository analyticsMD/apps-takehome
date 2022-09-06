from django.contrib import admin
from django.conf.urls import include, url
from parts_api import views, crud_view


urlpatterns = [
    # I commented this line because this is capturaing the update requests, that's why update request is not working properly.    
    # url("", views.home, name="home"),

    url("admin/", admin.site.urls),
    url("part/update/(?P<part_id>\d+)/$", views.update_part),
    
    # New Endpoints (PARTS CRUD) / Task 2
    url('parts/get-all', crud_view.list),
    url('parts/create', crud_view.create),
    url('parts/get/(?P<part_id>\d+)/$', crud_view.get),
    url('parts/update/(?P<part_id>\d+)/+$', crud_view.update),
    url('parts/delete/(?P<part_id>\d+)/$', crud_view.delete),

    # NLTK tokenization to aggregate the five most common words in the description field of our parts. / Task 3
    url('parts/common-words/(?P<most_common_quantity>\d+)/$', crud_view.get_common_words)
]
