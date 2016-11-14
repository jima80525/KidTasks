""" Define the data models for the KidsTasks app """
import datetime
from django.db import models


class Kid(models.Model):
    """ Defines the kids which have to do the tasks. """
    name = models.CharField(max_length=256)
    days = [
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday'
    ]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', ]

    def build_all_tasks(self):
        tasks = []

        # from
        # http://stackoverflow.com/questions/4720079/django-query-filter-with-\
        # variable-column
        for day in self.days:
            qs = RepeatingTask.objects.filter(kid=self).filter(**{ day : True })
            tasks.append((day, [task for task in qs]))
        return tasks


class Task(models.Model):
    """ A Task is associated with a kid and a date.  This is the actual thing
    the kid has to do! """
    name = models.CharField(max_length=256)
    completed = models.BooleanField()
    date = models.DateField(default=datetime.datetime.now)
    kid = models.ForeignKey(Kid)

    def __str__(self):
        return "{0}:{1}-{2}".format(self.name, self.kid.name, str(self.date))

    class Meta:
        ordering = ['name', ]


class RepeatingTask(models.Model):
    """ Defines a repeating task """
    name = models.CharField(max_length=256)
    kid = models.ForeignKey(Kid)  # NOTE: RepeatingTasks are kid specific
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)

    def __str__(self):
        return "{0}:{1}".format(self.kid.name, self.name)

    class Meta:
        ordering = ['kid', 'name', ]
