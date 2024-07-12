from django.forms import ModelForm  
from .models import *

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'finished']
    
    def save(self, commit=True):
        task = super().save(commit=False)
        task.author = self.instance.author
        if commit:
            task.save()
        return task