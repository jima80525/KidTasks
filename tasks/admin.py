""" Control admin pages for KidsTasks app """
from django.contrib import admin

from .models import Task, RepeatingTask, Kid


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """ Format admin page for Tasks """
    list_display = ('name', 'completed', 'date', 'kid')
    fields = [('name', 'completed', 'date', 'kid')]


@admin.register(Kid)
class KidAdmin(admin.ModelAdmin):
    """ Format admin page for Kid """
    list_display = ('name', 'last_update_date', )
    fields = [('name', 'last_update_date',)]


@admin.register(RepeatingTask)
class RepeatingTaskAdmin(admin.ModelAdmin):
    """ Format admin page for Tasks """
    list_display = ('name', 'kid', 'monday', 'tuesday', 'wednesday', 'thursday',
                   'friday', 'saturday', 'sunday')
    fields = [('name', 'kid', 'monday', 'tuesday', 'wednesday', 'thursday',
               'friday', 'saturday', 'sunday' )]
