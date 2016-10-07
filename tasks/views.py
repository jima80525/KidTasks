""" Django views for the KidsTasks app. """
import datetime
# pylint: disable=E0401
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Kid, DateTask, DateToKid


def build_today(kid, day_name=None):
    """ Checks the kid's date_tasks.  If empty, it creates a new date task for
    each task in the kid's day_schedules for today.  Either way, it returns a
    vector of DateTasks from the kid.date_tasks list. """

    current_date = str(datetime.datetime.now())[:10]
    day_name = day_name or datetime.datetime.now().strftime("%A")
    # need to purge date_tasks if date doesn't match today
    # NOTE: this is not ideal.  We need to figure out how we want to store
    # history as opposed to 'today's tasks'
    if kid.date_tasks.exists():
        existing_task = kid.date_tasks.all().first()
        existing_date = str(existing_task.date)[:10]
        if current_date != existing_date:
            kid.date_tasks.clear()

    if not kid.date_tasks.exists():
        for schd in kid.day_schedules.filter(day_name=day_name).order_by("id"):
            for task in schd.tasks.all():
                date_task = DateTask(name=task.name, required=task.required)
                date_task.save()
                d2k = DateToKid(task=date_task, kid=kid)
                d2k.save()

    return [task for task in
            kid.date_tasks.filter(date=current_date).order_by("id")]


def update_task(_, task_id):
    """ Invert the completed state of the specified task """
    date_task = get_object_or_404(DateTask, id=task_id)
    date_task.completed = not date_task.completed
    date_task.save()
    return HttpResponseRedirect(reverse('today'))


def today(request):
    """ Generate the 'today' page showing which tasks are due today """
    day_name = datetime.datetime.now().strftime("%A")
    kid_list = get_list_or_404(Kid)

    kids_tasks = list()
    kids = dict()
    for kid in kid_list:
        tasks = build_today(kid)
        if tasks:
            kids_tasks.append((kid.name, tasks))
            kids[kid.name] = tasks
    return render(request, 'tasks/today.html', {'kids': kids, 'day': day_name})


def index(request):
    """ Shows all of the tasks in the system, broken down by kid """
    kids = get_list_or_404(Kid)
    return render(request, 'tasks/index.html', {'kids': kids})
