from django import forms
from .models import BugReport, FeatureRequest
from tasks.models import Project, Task

from django.shortcuts import render
from django.http import HttpResponse


class BugReportForm(forms.ModelForm):
    class Meta:
        model = BugReport
        fields = ['title','description','project','task','status','priority']
    
    def valid_project_task(self,request,not_valid_html,html_kwargs) -> HttpResponse|None:
        return valid_form_project_task(self,request,not_valid_html,html_kwargs)

class FeatureRequestForm(forms.ModelForm):
    class Meta:
        model = FeatureRequest
        fields = ['title','description','project','task','status','priority']
    
    def valid_project_task(self,request,not_valid_html,html_kwargs) -> HttpResponse|None:
        return valid_form_project_task(self,request,not_valid_html,html_kwargs)

def valid_form_project_task(form:BugReportForm|FeatureRequestForm,request,not_valid_html,html_kwargs) -> HttpResponse|None:

    if (form.data['project'] and form.data['task'] and
        form.cleaned_data['project'].id != form.cleaned_data['task'].project.id):
        
        data = form.data.copy()
        data['task'] = 0
        form.data = data
        return render(request, not_valid_html, html_kwargs)
    return None




    # project = forms.ModelChoiceField(queryset=Project.objects.all())
    # task = forms.ModelChoiceField(queryset=Task.objects.all())
