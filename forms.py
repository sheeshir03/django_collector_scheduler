from django import forms
from django_celery_beat.models import PeriodicTask

class PeriodicTaskForm(forms.ModelForm):
    class Meta:
        model=PeriodicTask
        exclude= ['solar', 'clocked']