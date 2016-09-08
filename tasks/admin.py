from django.contrib import admin

from .models import Task, Kid, CountedTask, DayOfWeekSchedule, DateSchedule
from .models import WeekSchedule, Schedule, HistoricDate, History

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'required')
    fields = [('name', 'required')]

@admin.register(Kid)
class KidAdmin(admin.ModelAdmin):
    fields = [('name', 'schedule', 'history')]

@admin.register(CountedTask)
class CountedTaskAdmin(admin.ModelAdmin):
    fields = [('task', 'count')]

@admin.register(DayOfWeekSchedule)
class DayOfWeekScheduleAdmin(admin.ModelAdmin):
    list_display = ('day_name',)
    fields = [('tasks', 'day_name')]

@admin.register(DateSchedule)
class DateScheduleAdmin(admin.ModelAdmin):
    fields = [('task', 'date')]

@admin.register(WeekSchedule)
class WeekScheduleAdmin(admin.ModelAdmin):
    fields = [('tasks', 'start_date')]

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    fields = [('name', 'day_tasks', 'date_tasks', 'week_tasks')]

@admin.register(HistoricDate)
class HistoricDateAdmin(admin.ModelAdmin):
    fields = [('date', 'tasks', 'counted_tasks')]

@admin.register(History)
class HistoryDateAdmin(admin.ModelAdmin):
    fields = [('dates')]

