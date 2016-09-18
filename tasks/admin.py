from django.contrib import admin

from .models import DayTask, DateTask
from .models import Task, DayOfWeekSchedule, DateSchedule, Kid
from .models import Schedule#, HistoricDate, History

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'required')
    fields = [('name', 'required')]

class DayTaskInline(admin.TabularInline):
    model = DayTask
    extra = 1 # how many rows to show

@admin.register(DayOfWeekSchedule)
class DayOfWeekScheduleAdmin(admin.ModelAdmin):
    inlines = (DayTaskInline,)
    filter_horizontal = ('tasks', )
    list_display = ('name', 'day_name',  )
    fields = [('name', 'day_name')]

class DateTaskInline(admin.TabularInline):
    model = DateTask
    extra = 1 # how many rows to show

@admin.register(DateSchedule)
class DateScheduleAdmin(admin.ModelAdmin):
    inlines = (DateTaskInline,)
    filter_horizontal = ('tasks', )
    fields = [('name', 'date')]

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    filter_horizontal = ['day_tasks', 'date_tasks', ]
    fields = [('name', 'day_tasks', 'date_tasks', )]

@admin.register(Kid)
class KidAdmin(admin.ModelAdmin):
    fields = [('name', 'schedule', )]

