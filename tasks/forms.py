from django import forms

from .models import RepeatingTask


class TaskForm(forms.ModelForm):
    class Meta:
        model = RepeatingTask
        fields = ('name', 'kid', 'monday', 'tuesday', 'wednesday', 'thursday',
                  'friday', 'saturday', 'sunday',)
