""" Django views for the KidsTasks app. """
import datetime
# pylint: disable=E0401
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from .models import Kid, RepeatingTask, Task
from .forms import RepeatingTaskForm, TaskForm


class FullList(ListView):
    """ Shows all of the tasks in the system, broken down by kid """
    model = Kid

    def get_context_data(self, **kwargs):
        # get_context_data creates the context
        context = ListView.get_context_data(self, **kwargs)

        # Get the list of kids
        kid_list = get_list_or_404(Kid.objects.order_by('name'))

        # create a dict with an index for each kid.  The value associated with
        # the kid will be a list of tuples:
        #     (day_name [list of tasks for that day])
        # JHA TODO make this a list so it's ordered
        # https://docs.djangoproject.com/en/dev/howto/custom-template-
        # tags/#howto-custom-template-tags
        kids = {}
        for kid in kid_list:
            kids[kid.name] = kid.build_all_tasks()
        context.update({'kids': kids, })
        return context


def new_repeating_task(request):
    if request.method == "POST":
        form = RepeatingTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = RepeatingTaskForm()
    return render(request, 'tasks/repeating_task_edit.html', {'form': form})


def update_repeating_task(request, task_id):
    task = get_object_or_404(RepeatingTask, id=task_id)
    form = RepeatingTaskForm(request.POST or None, instance=task)
    if request.method == "POST":
        if form.is_valid():
            if 'delete' in request.POST:
                task.delete()
            elif 'save' in request.POST:
                form.save()
            # ignore if the cancel button was pressed
            return redirect(reverse('index'))
    return render(request, 'tasks/repeating_task_update.html', {'form': form})


def today(request):
    """ Generate the 'today' page showing which tasks are due today """
    day_name = datetime.datetime.now().strftime("%A")
    kid_list = get_list_or_404(Kid.objects.order_by('name'))
    kids = dict()
    for kid in kid_list:
        kid.populate_today()  # get RepeatingTasks set up for today
        task_list = Task.objects.filter(kid=kid). \
            filter(date=datetime.datetime.today())
        if task_list:
            kids[kid.name] = [task for task in task_list]

    return render(request, 'tasks/today.html', {'kids': kids, 'day': day_name})


def update_task(_, task_id):
    """ Invert the completed state of the specified task """
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return HttpResponseRedirect(reverse('today'))


def new_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('today'))
    else:
        form = TaskForm()
    return render(request, 'tasks/task_edit.html', {'form': form})
