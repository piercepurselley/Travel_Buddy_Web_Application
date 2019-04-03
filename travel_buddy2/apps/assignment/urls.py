from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process/(?P<action>\w+)$', views.process),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^create$', views.create),
    url(r'^delete/(?P<product_id>\d+)$', views.delete),
    url(r'^add_item$', views.add_item),
    url(r'^item/(?P<product_id>\d+)$', views.item),
]