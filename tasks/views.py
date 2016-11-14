""" Django views for the KidsTasks app. """
import datetime
# pylint: disable=E0401
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.forms.models import inlineformset_factory
from .models import Kid, RepeatingTask
from .forms import TaskForm


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
        kids = {}
        for kid in kid_list:
            kids[kid.name] = kid.build_all_tasks()
        context.update({'kids': kids, })
        return context


def new_repeating_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = TaskForm()
    return render(request, 'tasks/task_edit.html', {'form': form})


def update_repeating_task(request, task_id):
    task = get_object_or_404(RepeatingTask, id=task_id)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == "POST":
        if form.is_valid():
            if 'delete' in request.POST:
                task.delete()
            elif 'save' in request.POST:
                form.save()
            # ignore if the cancel button was pressed
            return redirect(reverse('index'))
    return render(request, 'tasks/task_update.html', {'form': form })


#class TodayList(ListView):
    #""" Generate the 'today' page showing which tasks are due today """
    #model = Kid
    #template_name = 'tasks/today.html'

    #def get_context_data(self, **kwargs):
        # get_context_data creates the context
        #context = ListView.get_context_data(self, **kwargs)

        #day_name = datetime.datetime.now().strftime("%A")
        #kid_list = get_list_or_404(Kid.objects.order_by('name'))

        #kids = {kid.name: kid.build_today() for kid in kid_list}
        #context.update({'kids': kids, 'day': day_name})

        #return context


#def update_task(_, task_id):
    #""" Invert the completed state of the specified task """
    #date_task = get_object_or_404(DateTask, id=task_id)
    #date_task.completed = not date_task.completed
    #date_task.save()
    #return HttpResponseRedirect(reverse('today'))


#def task_new(request):
    #if request.method == "POST":
        #form = TaskForm(request.POST)
        #if form.is_valid():
            #form.save()
            #return redirect(reverse('today'))
    #else:
        #form = TaskForm()
    #return render(request, 'tasks/task_edit.html', {'form': form})

