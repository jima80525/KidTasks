""" Define the data models for the KidsTasks app """
import calendar
import datetime
from django.db import models


class Task(models.Model):
    """ Defines a generic task which is not tied to a date """
    name = models.CharField(max_length=256)
    required = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', ]


class DayOfWeekSchedule(models.Model):
    """ Defines a list of tasks which must be performed on a specific day of
    the week. """
    day_of_week_choices = [(calendar.day_name[i], calendar.day_name[i]) for i
                           in range(0, 7)]

    name = models.CharField(max_length=256)
    tasks = models.ManyToManyField(Task, through='DayTask')
    day_name = models.CharField(max_length=20, choices=day_of_week_choices)

    def __str__(self):
        return "{}-{}".format(self.name, self.day_name)

    class Meta:
        ordering = ['name', 'day_name']


class DayTask(models.Model):
    """ Intermediary model to allow multiple tasks with the same name to be
    applied to a single day of the week."""
    task = models.ForeignKey(Task)
    schedule = models.ForeignKey(DayOfWeekSchedule)


class DateTask(models.Model):
    """ Task which has been assigned a specific date on which it must be
    completed. """
    name = models.CharField(max_length=256)
    date = models.DateField(default=datetime.datetime.now)
    completed = models.BooleanField(default=False)
    required = models.BooleanField(default=False)

    def __str__(self):
        return "{}-{}".format(self.date, self.name)

    class Meta:
        ordering = ['completed', 'name', 'date']


class Kid(models.Model):
    """ Defines the kids which have to do the tasks! """
    name = models.CharField(max_length=256)
    day_schedules = models.ManyToManyField(DayOfWeekSchedule)
    # this will be all assigned tasks, both present and future
    date_tasks = models.ManyToManyField(DateTask, through='DateToKid')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', ]

    def build_today(self, day_name=None):
        """ Checks the kid's date_tasks.  If empty, it creates a new date task
        for each task in the kid's day_schedules for today.  Either way, it
        returns a vector of DateTasks from the kid.date_tasks list.
        NOTE: this still needs to be redesigned to create history list from
        old today list."""

        current_date = str(datetime.datetime.now())[:10]
        day_name = day_name or datetime.datetime.now().strftime("%A")
        # need to purge date_tasks if date doesn't match today
        # NOTE: this is not ideal.  We need to figure out how we want to store
        # history as opposed to 'today's tasks'
        if self.date_tasks.exists():
            existing_task = self.date_tasks.all().first()
            existing_date = str(existing_task.date)[:10]
            if current_date != existing_date:
                self.date_tasks.clear()

        if not self.date_tasks.exists():
            for schd in self.day_schedules.filter(day_name=day_name).order_by(
                            "id"):
                for task in schd.tasks.all():
                    date_task = DateTask(name=task.name,
                                         required=task.required)
                    date_task.save()
                    d2k = DateToKid(task=date_task, kid=self)
                    d2k.save()

        return [task for task in
                self.date_tasks.filter(date=current_date).order_by("id")]


class DateToKid(models.Model):
    """ Intermediary model to join DateTasks and Kids """
    task = models.ForeignKey(DateTask)
    kid = models.ForeignKey(Kid)
