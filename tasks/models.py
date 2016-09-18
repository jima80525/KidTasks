from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=256)
    required = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', ]

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
    tasks = models.ManyToManyField(Task, through='DayTask')
    day_name = models.CharField(max_length=1, choices=day_of_week_choices)

    def __str__(self):
        full_day = dict(self.day_of_week_choices)[self.day_name]
        return "{}-{}".format(self.name, full_day)

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

