from django.forms import BaseModelForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
import django.http.request
from django.urls import reverse
from django.shortcuts import get_object_or_404


from .models import BugReport, FeatureRequest
from tasks.models import Project, Task

from .forms import BugReportForm, FeatureRequestForm


###--- Представления через функции (FBV) ---###

# Главная страница 
def index(request):
    return render(request, 'quality_control/index.html')

# Список всех багов
def bug_list(request):
    return render(request, 'quality_control/bug_list.html', {'bugs':BugReport.objects.all()})

# Список запросов на улучшение
def feature_list(request):
    return render(request, 'quality_control/feature_list.html', {'features':FeatureRequest.objects.all()})

# Описание отчета об ошибках
def bug_detail(request,bug_id):
    bug = get_object_or_404(BugReport, pk=bug_id)
    return render(request, 'quality_control/bug_detail.html', {'bug':bug})

# Описание запроса об улучшении
def feature_detail(request,feature_id):
    feature = get_object_or_404(FeatureRequest, pk=feature_id)
    return render(request, 'quality_control/feature_detail.html', {'feature':feature})

# Создание нового отчета об ошибках
def create_bug(request):
    form_html = 'quality_control/bug_report_form.html'
    form_html_kwargs = {'form':None}

    if request.method == "POST":
        form = BugReportForm(request.POST)
        form_html_kwargs['form'] = form

        if form.is_valid():
            not_valid_response = form.valid_project_task(request,form_html,form_html_kwargs)
            if not_valid_response: return not_valid_response

            form.save()
            return redirect('quality_control:bug_list')
    else:
        form_html_kwargs['form'] = BugReportForm()
    return render(request, form_html, form_html_kwargs)

# Создание нового запроса об улучшении
def create_feature(request):
    form_html = 'quality_control/feature_request_form.html'
    form_html_kwargs = {'form':None}
    
    if request.method == "POST":
        form = FeatureRequestForm(request.POST)
        form_html_kwargs['form'] = form

        if form.is_valid():
            not_valid_response = form.valid_project_task(request,form_html,form_html_kwargs)
            if not_valid_response: return not_valid_response

            form.save()
            return redirect('quality_control:feature_list')
    else:
        form_html_kwargs['form'] = FeatureRequestForm()
    return render(request, form_html, form_html_kwargs)

# Обновление отчета об ошибках
def update_bug(request, bug_id):
    bug = get_object_or_404(BugReport, pk=bug_id)
    form_html = 'quality_control/bug_update.html'
    form_html_kwargs = {'form':None, 'bug':bug}

    if request.method == "POST":
        form = BugReportForm(request.POST, instance=bug)
        form_html_kwargs['form'] = form

        if form.is_valid():
            not_valid_response = form.valid_project_task(request,form_html,form_html_kwargs)
            if not_valid_response: return not_valid_response
            
            form.save()
            return redirect('quality_control:bug_detail', bug_id=bug.id)
    else:
        form_html_kwargs['form'] = BugReportForm(instance=bug)
    return render(request, form_html, form_html_kwargs)

# Обновление запроса об улучшении
def update_feature(request, feature_id):
    feature = get_object_or_404(FeatureRequest, pk=feature_id)
    form_html = 'quality_control/feature_update.html'
    form_html_kwargs = {'form':None, 'feature':feature}

    if request.method == "POST":
        form = FeatureRequestForm(request.POST, instance=feature)
        form_html_kwargs['form'] = form
        
        if form.is_valid():
            not_valid_response = form.valid_project_task(request,form_html,form_html_kwargs)
            if not_valid_response: return not_valid_response

            form.save()
            return redirect('quality_control:feature_detail', feature_id=feature.id)
    else:
        form_html_kwargs['form'] = FeatureRequestForm(instance=feature)
    return render(request, form_html, form_html_kwargs)

# удаление объекта
def delete_object(request, Model, object_id, redirect_url, **redirect_url_args):
    obj = get_object_or_404(Model, pk=object_id)
    obj.delete()
    return redirect(redirect_url,**redirect_url_args)

# Удаление отчета об ошибках
def delete_bug(request, bug_id):
    return delete_object(request,BugReport,bug_id,'quality_control:bug_list')
# Удаление запроса об улучшении
def delete_feature(request, feature_id):
    return delete_object(request,FeatureRequest,feature_id,'quality_control:feature_list')


###--- Представления через классы (CBV) ---###
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Главная страница 
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'quality_control/index.html')

# Список всех багов
class BugListView(ListView):
    model = BugReport
    template_name = 'quality_control/bug_list.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'bugs':BugReport.objects.all()})

# Список всех запросов на улучшение
class FeatureListView(ListView):
    model = FeatureRequest
    template_name = 'quality_control/feature_list.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'features':FeatureRequest.objects.all()})

# Описание отчета об ошибках
class BugDetailView(DetailView):
    model = BugReport
    pk_url_kwarg = 'bug_id'
    template_name = 'quality_control/bug_detail.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'bug':self.get_object()})

# Описание запроса на улучшения
class FeatureDetailView(DetailView):
    model = FeatureRequest
    pk_url_kwarg = 'feature_id'
    template_name = 'quality_control/feature_detail.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'feature':self.get_object()})

# Создание нового отчета об ошибках
class BugCreateView(CreateView):
    model = BugReport
    form_class = BugReportForm
    template_name = 'quality_control/bug_report_form.html'
    success_url = reverse_lazy('quality_control:bug_list')

    def form_valid(self, form: BugReportForm) -> HttpResponse:
        not_valid_response = form.valid_project_task(self.request,self.template_name,{'form':form})
        if not_valid_response: return not_valid_response
        return super().form_valid(form)

# Создание нового запроса на улучшения
class FeatureCreateView(CreateView):
    model = FeatureRequest
    form_class = FeatureRequestForm
    template_name = 'quality_control/feature_report_form.html'
    success_url = reverse_lazy('quality_control:feature_list')

    def form_valid(self, form: FeatureRequestForm) -> HttpResponse:
        not_valid_response = form.valid_project_task(self.request,self.template_name,{'form':form})
        if not_valid_response: return not_valid_response
        return super().form_valid(form)

# Обновление отчета об ошибках
class BugUpdateView(UpdateView):
    model = BugReport
    form_class = BugReportForm
    template_name = 'quality_control/bug_update.html'
    pk_url_kwarg = 'bug_id'

    def form_valid(self, form: BugReportForm) -> HttpResponse:
        not_valid_response = form.valid_project_task(self.request,self.template_name,{'form':form,'bug':self.get_object()})
        if not_valid_response: return not_valid_response
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('quality_control:bug_detail', kwargs={'bug_id':self.object.id})
    
# Обновление запроса на улучшения
class FeatureUpdateView(UpdateView):
    model = FeatureRequest
    form_class = FeatureRequestForm
    template_name = 'quality_control/feature_update.html'
    pk_url_kwarg = 'feature_id'

    def form_valid(self, form: FeatureRequestForm) -> HttpResponse:
        not_valid_response = form.valid_project_task(self.request,self.template_name,{'form':form,'feature':self.object})
        if not_valid_response: return not_valid_response
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('quality_control:feature_detail', kwargs={'feature_id':self.object.id})

# Удаление отчета об ошибках
class BugDeleteView(DeleteView):
    model = BugReport
    pk_url_kwarg = 'bug_id'
    success_url = reverse_lazy('quality_control:bug_list')
    template_name = 'quality_control/bug_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{'bug':self.get_object()})

# Удаление запроса на улучшения
class FeatureDeleteView(DeleteView):
    model = FeatureRequest
    pk_url_kwarg = 'feature_id'
    success_url = reverse_lazy('quality_control:feature_list')
    template_name = 'quality_control/feature_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{'feature':self.get_object()})