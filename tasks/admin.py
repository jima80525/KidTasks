from django.contrib import admin

from .models import Task, CountedTask, DayOfWeekSchedule, DateSchedule  #, Kid
#from .models import WeekSchedule, Schedule, HistoricDate, History
#from .models import Task, Kid, CountedTask, DayOfWeekSchedule, DateSchedule
#from .models import WeekSchedule, Schedule, HistoricDate, History

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'required')
    fields = [('name', 'required')]

@admin.register(CountedTask)
class CountedTaskAdmin(admin.ModelAdmin):
    fields = [('name', 'count', 'required')]

@admin.register(DayOfWeekSchedule)
class DayOfWeekScheduleAdmin(admin.ModelAdmin):
    filter_horizontal = ('tasks', )
    list_display = ('name', 'day_name',  )
    fields = [('name', 'day_name', 'tasks')]

@admin.register(DateSchedule)
class DateScheduleAdmin(admin.ModelAdmin):
    filter_horizontal = ('tasks', )
    fields = [('name', 'tasks', 'date')]

#@admin.register(WeekSchedule)
#class WeekScheduleAdmin(admin.ModelAdmin):
    #fields = [('tasks', 'start_date')]

#@admin.register(Schedule)
#class ScheduleAdmin(admin.ModelAdmin):
    #fields = [('name', 'day_tasks', 'date_tasks', 'week_tasks')]

#@admin.register(HistoricDate)
#class HistoricDateAdmin(admin.ModelAdmin):
    #fields = [('date', 'tasks', 'counted_tasks')]

#@admin.register(History)
#class HistoryDateAdmin(admin.ModelAdmin):
    #fields = [('dates')]

#@admin.register(Kid)
#class KidAdmin(admin.ModelAdmin):
    #fields = [('name', 'schedule', 'history')]

