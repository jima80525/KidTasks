from django import forms

from .models import RepeatingTask, Task, Kid


class RepeatingTaskForm(forms.ModelForm):
    class Meta:
        model = RepeatingTask
        fields = ('name', 'kid', 'monday', 'tuesday', 'wednesday', 'thursday',
                  'friday', 'saturday', 'sunday',)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'completed', 'date', 'kid',)


class KidForm(forms.ModelForm):
    class Meta:
        model = Kid
        fields = ('name', 'last_update_date',)
