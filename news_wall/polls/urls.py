#-*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

app_name = "polls"
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
]