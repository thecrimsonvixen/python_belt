from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^home$', views.home),
    url(r'^logout$', views.logout),
    # url(r'^new$', views.new),
    # url(r'^create$', views.create),
    url(r'^(?P<id>\d+)/view$', views.view),
    url(r'^(?P<id>\d+)/friend$', views.friend), #change to FRIEND elsewhere
    url(r'^(?P<id>\d+)/unfriend$', views.unfriend), #change to FRIEND elsewhere
    # url(r'^(?P<id>\d+)/edit$', views.edit),
    # url(r'^(?P<id>\d+)/update$', views.update),    
    # url(r'^(?P<id>\d+)/delete$', views.delete),
]