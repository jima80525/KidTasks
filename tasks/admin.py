""" Control admin pages for KidsTasks app """
from django.contrib import admin

from .models import DayTask
from .models import Task, DayOfWeekSchedule, Kid


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """ Format admin page for Tasks """
    list_display = ('name', 'required')
    fields = [('name', 'required')]


class DayTaskInline(admin.TabularInline):
    """ create an inline for the DayOfWeekSchedule admin page """
    model = DayTask
    extra = 1  # how many rows to show


@admin.register(DayOfWeekSchedule)
class DayOfWeekScheduleAdmin(admin.ModelAdmin):
    """ Format admin page for DayOfWeekSchedule """
    inlines = (DayTaskInline,)
    filter_horizontal = ('tasks', )
    list_display = ('name', 'day_name', )
    fields = [('name', 'day_name')]


@admin.register(Kid)
class KidAdmin(admin.ModelAdmin):
    """ Format admin page for Kid """
    filter_horizontal = ['day_schedules', ]
    fields = [('name', 'day_schedules', )]
