""" Django views for the KidsTasks app. """
import datetime
# pylint: disable=E0401
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from .models import Kid, DateTask


class FullList(ListView):
    """ Shows all of the tasks in the system, broken down by kid """
    model = Kid


def update_task(_, task_id):
    """ Invert the completed state of the specified task """
    date_task = get_object_or_404(DateTask, id=task_id)
    date_task.completed = not date_task.completed
    date_task.save()
    return HttpResponseRedirect(reverse('today'))


def today(request):
    """ Generate the 'today' page showing which tasks are due today """
    day_name = datetime.datetime.now().strftime("%A")
    kid_list = get_list_or_404(Kid.objects.order_by('name'))

    kids = {kid.name: kid.build_today() for kid in kid_list}
    return render(request, 'tasks/today.html', {'kids': kids, 'day': day_name})
