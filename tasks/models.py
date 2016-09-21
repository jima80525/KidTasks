from django.db import models
import calendar

class Task(models.Model):
    name = models.CharField(max_length=256)
    required = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', ]

class DayOfWeekSchedule(models.Model):
    day_of_week_choices  = [(calendar.day_name[i], calendar.day_name[i]) for i
                            in range(0,7)]

    name = models.CharField(max_length=256)
    tasks = models.ManyToManyField(Task, through='DayTask')
    day_name = models.CharField(max_length=20, choices=day_of_week_choices)

    def __str__(self):
        return "{}-{}".format(self.name, self.day_name)

    class Meta:
        ordering = ['name', 'day_name']

class DayTask(models.Model):
    task = models.ForeignKey(Task)
    schedule = models.ForeignKey(DayOfWeekSchedule)

class DateSchedule(models.Model):
    name = models.CharField(max_length=256)
    tasks = models.ManyToManyField(Task, through='DateTask')
    date = models.DateField()

    def __str__(self):
        return "{}-{}".format(self.name, self.date)

    class Meta:
        ordering = ['name', 'date']

class DateTask(models.Model):
    task = models.ForeignKey(Task)
    schedule = models.ForeignKey(DateSchedule)

class Schedule(models.Model):
    name = models.CharField(max_length=256)
    day_tasks = models.ManyToManyField(DayOfWeekSchedule)
    date_tasks = models.ManyToManyField(DateSchedule)

    def __str__(self):
        return "{} Schedule".format(self.name)

    class Meta:
        ordering = ['name', ]

class Kid(models.Model):
    name = models.CharField(max_length=256)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', ]

