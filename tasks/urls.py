""" Url specifications for the KidsTasks django app """
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^today$', views.today, name='today'),
    url(r'^update/(?P<task_id>[0-9]+)$', views.update_task, name='update'),
]
