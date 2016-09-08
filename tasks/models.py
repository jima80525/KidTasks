from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=256)
    required = models.BooleanField()

class CountedTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    count = models.IntegerField()

class DayOfWeekSchedule(models.Model):
    tasks = models.ManyToManyField(Task)
    day_name = models.CharField(max_length=256)

class DateSchedule(models.Model):
    tasks = models.ManyToManyField(Task)
    date = models.DateField()

class WeekSchedule(models.Model):
    tasks = models.ManyToManyField(CountedTask)
    start_date = models.DateField()

class Schedule(models.Model):
    name = models.CharField(max_length=256)
    day_tasks = models.ManyToManyField(DayOfWeekSchedule)
    date_tasks = models.ManyToManyField(DateSchedule)
    week_tasks = models.ManyToManyField(WeekSchedule)

class HistoricDate(models.Model):
    date = models.DateField()
    tasks = models.ManyToManyField(Task)
    counted_tasks = models.ManyToManyField(CountedTask)

class History(models.Model):
    dates = models.ManyToManyField(HistoricDate)

class Kid(models.Model):
    name = models.CharField(max_length=256)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    history = models.ForeignKey(History, on_delete=models.CASCADE)

