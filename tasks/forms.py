"""Forms for the KidTasks app"""
from django import forms

from .models import RepeatingTask, Task, Kid


class RepeatingTaskForm(forms.ModelForm):
    """ Enter info about repeating tasks """
    class Meta:
        model = RepeatingTask
        fields = ('name', 'kid', 'monday', 'tuesday', 'wednesday', 'thursday',
                  'friday', 'saturday', 'sunday',)


class TaskForm(forms.ModelForm):
    """ Enter info about non-repeating tasks """
    class Meta:
        model = Task
        fields = ('name', 'completed', 'date', 'kid',)


class KidForm(forms.ModelForm):
    """ Enter info about kids """
    class Meta:
        model = Kid
        fields = ('name', 'last_update_date',)
