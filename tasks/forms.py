from django import forms

from .models import DayOfWeekSchedule

class TaskForm(forms.ModelForm):

    class Meta:
        model = DayOfWeekSchedule
        fields = ('name', 'day_name', 'tasks',)
