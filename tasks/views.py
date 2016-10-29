""" Django views for the KidsTasks app. """
import datetime
# pylint: disable=E0401
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from .models import Kid, DateTask


class FullList(ListView):
    """ Shows all of the tasks in the system, broken down by kid """
    model = Kid


class TodayList(ListView):
    """ Generate the 'today' page showing which tasks are due today """
    model = Kid
    template_name = 'tasks/today.html'

    def get_context_data(self, **kwargs):
        # get_context_data creates the context
        context = ListView.get_context_data(self, **kwargs)

        day_name = datetime.datetime.now().strftime("%A")
        kid_list = get_list_or_404(Kid.objects.order_by('name'))

        kids = {kid.name: kid.build_today() for kid in kid_list}
        context.update({'kids': kids, 'day': day_name})

        return context


def update_task(_, task_id):
    """ Invert the completed state of the specified task """
    date_task = get_object_or_404(DateTask, id=task_id)
    date_task.completed = not date_task.completed
    date_task.save()
    return HttpResponseRedirect(reverse('today'))
