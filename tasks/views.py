#!/usr/bin/env python3
""" Django views for the KidsTasks app. """
import datetime
# pylint: disable=E0401
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Kid, RepeatingTask, Task
from .forms import RepeatingTaskForm, TaskForm, KidForm


def get_list_of_kids():
    """ Get the list of kids from the database.  Don't use get_list_or_404 here
    in order to catch the case of a new DB where no kids are defined."""
    try:
        kid_list = Kid.objects.all()
    except Kid.DoesNotExist:
        kid_list = []
    return kid_list


@login_required
def repeating_tasks(request):
    """ Shows all of the repeating tasks in the system, broken down by kid """
    # create a dict with an key for each kid.  The value associated with the
    # kid will be a list of tuples:
    #     (day_name [list of tasks for that day])
    kid_list = {}
    for kid in get_list_of_kids():
        kid_list[kid.name] = kid.build_all_tasks()

    return render(request, 'tasks/repeating_tasks.html', {'kids': kid_list, })


@login_required
def kids(request):
    """ Shows all of the kids in the system """
    return render(request, 'tasks/kids.html',
                  {'kids': get_list_of_kids(), })


@login_required
def new_repeating_task(request):
    """ Generate a new repeating task """
    if request.method == "POST":
        form = RepeatingTaskForm(request.POST)
        if form.is_valid():
            # get the kid out of the cleaned data and make sure that it updates
            # the "today" list with this new task if necessary
            kid = form.cleaned_data['kid']
            # make sure that the kid has repeating tasks moved to "today" tasks
            # before we try to update with the newly created task.  We need to
            # do this as a two-step process to avoid a curious bug.  If the kid
            # has already had today populated, then this will be a no-op and
            # the update_with_new call will work OK.  If it has NOT been called
            # then, if we don't do this first, we end up with two copies of
            # the repeated task for today
            kid.populate_today()

            the_task = form.save()
            kid.update_with_new_repeating_task(the_task, form.cleaned_data)

            # redirect to the page we were on before
            next_task = request.GET.get('next', None)
            if next_task:
                return redirect(next_task)
            return redirect(reverse('rep_tasks'))
    else:
        form = RepeatingTaskForm()
    return render(request, 'tasks/repeating_task_edit.html',
                  {'form': form, 'from': request.GET.get('from', None)})


@login_required
def update_kid(request, kid_id):
    """ Change name or last updated fields for a kid """
    kid = get_object_or_404(Kid, id=kid_id)
    form = KidForm(request.POST or None, instance=kid)
    if request.method == "POST":
        if form.is_valid():
            if 'delete' in request.POST:
                kid.delete()
            elif 'save' in request.POST:
                form.save()
            # ignore if the cancel button was pressed
            return redirect(reverse('show_kids'))
    return render(request, 'tasks/kid_update.html', {'form': form})


@login_required
def update_repeating_task(request, task_id):
    """ Change fields in repeated task """
    task = get_object_or_404(RepeatingTask, id=task_id)
    form = RepeatingTaskForm(request.POST or None, instance=task)
    if request.method == "POST":
        if form.is_valid():
            if 'delete' in request.POST:
                task.delete()
            elif 'save' in request.POST:
                form.save()
            # ignore if the cancel button was pressed
            return redirect(reverse('rep_tasks'))
    return render(request, 'tasks/repeating_task_update.html', {'form': form})


@login_required
def today(request):
    """ Generate the 'today' page showing which tasks are due today """
    day_name = datetime.datetime.now().strftime("%A")

    kid_list = dict()
    for kid in get_list_of_kids():
        kid.populate_today()  # get RepeatingTasks set up for today
        task_list = Task.objects.filter(kid=kid). \
            filter(date=datetime.datetime.today())
        kid_list[kid.name] = [task for task in task_list]

    return render(request, 'tasks/today.html', {'kids': kid_list,
                                                'day': day_name})


@login_required
def update_task(_, task_id):
    """ Invert the completed state of the specified task """
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return HttpResponseRedirect(reverse('today'))


@login_required
def new_task(request):
    """ create a new task with a date """
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            next_task = request.GET.get('next', None)
            if next_task:
                return redirect(next_task)
            # if for some reason it was not set, default to today
            return redirect(reverse('today'))
    else:
        form = TaskForm()
    return render(request, 'tasks/task_edit.html',
                  {'form': form, 'from': request.GET.get('from', None)})


@login_required
def new_kid(request):
    """ Create a new kid!  Sounds more exciting than it is. """
    if request.method == "POST":
        form = KidForm(request.POST)
        if form.is_valid():
            form.save()
            next_task = request.GET.get('next', None)
            if next_task:
                return redirect(next_task)
            # if for some reason it was not set, default to today
            return redirect(reverse('today'))
    else:
        form = KidForm()
    return render(request, 'tasks/kid_edit.html',
                  {'form': form, 'from': request.GET.get('from', None)})
