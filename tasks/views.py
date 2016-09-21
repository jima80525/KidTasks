from django.shortcuts import get_list_or_404, render
from django.http import HttpResponse
from .models import Task, Kid
import datetime
#import calendar

def buildToday(kid, day_name):
    output = ''
    for sched in kid.schedule.day_tasks.filter(day_name=day_name):
        output += ', '.join([t.name for t in sched.tasks.all()])
    return output


# jha for each kid we need to build the list of today's tasks and add that to
# the kid model.  Maybe that needs to be part of kid -
# Question is if this should be a "today's task" list or if it should be just
# another entry in the history list (which would make the selecting of tasks
# and/or days a bit more orthoganal.
# let's start with today list and then generalize it
# likely need to create a new model for date_task and have a cstor with a Task
# object to create it.
def today(request):
    output = ''

    day_name = datetime.datetime.now().strftime("%A")
    kids = get_list_or_404(Kid)
    for kid in kids:
        output += buildToday(kid, day_name)
    output += '<h2>'

    #day_number = datetime.datetime.today().weekday()
    #day = calendar.day_name[day_number]
    #output += "num {:d} day {} = new = ".format(day_number, day)
    #output += str(now)
    #output += " THAT "
    #now = datetime.datetime.now()
    #output += now.strftime("%A")
    output += "here " + datetime.datetime.now().strftime("%A")
    output += '</h2>'
    return HttpResponse(output)
    #return render(request, 'tasks/index.html', {'kids': kids})

def index(request):
    kids = get_list_or_404(Kid)
    return render(request, 'tasks/index.html', {'kids': kids})

def testtoday(request):
    output = ''
    #task_list = Task.objects.order_by('-name')
    #output = ', '.join([t.name for t in task_list])
    #output += " THIS IS HERE "
    #output += "and THAT IS HERE "
    kids = Kid.objects.order_by('name')
    #output += ', '.join([t.name for t in kids])
    for kid in kids:
       name = kid.schedule.name
       output += " THIS IS HERE "
       output += "and THAT IS HERE "
       output += "kid name " + kid.name + " NEW schedule name " + name
       output += " NEW STUFF "
       for x in kid.schedule.day_tasks.all():
           output += " test " + x.__str__()
           output += " has tasks:"
           output += ', '.join([t.name for t in x.tasks.filter(name='bath')])
           #output += ', '.join([t.name for t in x.tasks.all()])
    return HttpResponse(output)
    #return HttpResponse("Hello, world. You're at the tasks index.")

