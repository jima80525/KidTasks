from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=256)
    required = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', ]

class CountedTask(models.Model):
    name = models.CharField(max_length=256)
    required = models.BooleanField()
    count = models.IntegerField()

    def __str__(self):
        return "{} ({:d})".format(self.name, self.count)

    class Meta:
        ordering = ['name', 'count']

class DayOfWeekSchedule(models.Model):
    day_of_week_choices = (
        ('M', 'Monday'),
        ('T', 'Tuesday'),
        ('W', 'Wednesday'),
        ('R', 'Thursday'),
        ('F', 'Friday'),
        ('S', 'Saturday'),
        ('N', 'Sunday'),
    )

    name = models.CharField(max_length=256)
    tasks = models.ManyToManyField(Task)
    day_name = models.CharField(max_length=1, choices=day_of_week_choices)

    def __str__(self):
        full_day = dict(self.day_of_week_choices)[self.day_name]
        return "{}-{}".format(self.name, full_day)

    class Meta:
        ordering = ['name', 'day_name']

class DateSchedule(models.Model):
    """ here"""
    name = models.CharField(max_length=256)
    tasks = models.ManyToManyField(Task)
    date = models.DateField()

    def __str__(self):
        return "{}-{}".format(self.name, self.date)

    class Meta:
        ordering = ['name', 'date']

#class WeekSchedule(models.Model):
    #tasks = models.ManyToManyField(CountedTask)
    #start_date = models.DateField()

#class Schedule(models.Model):
    #name = models.CharField(max_length=256)
    #day_tasks = models.ManyToManyField(DayOfWeekSchedule)
    #date_tasks = models.ManyToManyField(DateSchedule)
    #week_tasks = models.ManyToManyField(WeekSchedule)

#class HistoricDate(models.Model):
    #date = models.DateField()
    #tasks = models.ManyToManyField(Task)
    #counted_tasks = models.ManyToManyField(CountedTask)

#class History(models.Model):
    #dates = models.ManyToManyField(HistoricDate)

#class Kid(models.Model):
    #name = models.CharField(max_length=256)
    #schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    #history = models.ForeignKey(History, on_delete=models.CASCADE)

