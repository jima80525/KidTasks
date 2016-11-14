""" Url specifications for the KidsTasks django app """
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.FullList.as_view(), name='index'),
    #url(r'^today$', views.TodayList.as_view(), name='today'),
    #url(r'^update/(?P<task_id>[0-9]+)$', views.update_task, name='update'),
    url(r'^repeatingtask/new$', views.new_repeating_task, name='rep_task_new'),
    url(r'^repeatingtask/update/(?P<task_id>[0-9]+)$',
        views.update_repeating_task, name='rep_task_update'),
]
