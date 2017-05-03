""" Url specifications for the KidsTasks django app """
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.repeating_tasks, name='rep_tasks'),
    url(r'^today$', views.today, name='today'),

    # this is the url to change completed state of tasks
    url(r'^update/(?P<task_id>[0-9]+)$', views.update_task, name='update'),

    url(r'^task/new$', views.new_task, name='task_new'),
    url(r'^repeatingtask/new$', views.new_repeating_task, name='rep_task_new'),
    url(r'^repeatingtask/update/(?P<task_id>[0-9]+)$',
        views.update_repeating_task, name='rep_task_update'),
    url(r'^kids$', views.kids, name='show_kids'),
    url(r'^kid/new$', views.new_kid, name='kid_new'),
    url(r'^kid/update/(?P<name>[a-zA-Z ]+)$',
        views.update_kid, name='kid_update'),
]
