from django.forms import BaseModelForm
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404

from .models import Project, Task
from quality_control import urls as quality_control_urls

from django.template.loader import render_to_string

# Create your views here.
# Представления

# влючает в себя логику того, как данное приложение взаимодействует с запросами пользователей
# представления, обрабатывая данные, отображают шаблоны и реагируют на действия
# этот файл преобразует взаимодействие пользователей в ощутимые ответы



# будет срабатывать при обращении к главной странице приложения tasks
def index(request):
    quality_control_url = reverse(f"{quality_control_urls.app_name}:index")
    projects_list_url = reverse('tasks:projects_list')
    html = f"""<h1>Страница приложения tasks</h1>
            <a href='{quality_control_url}'>Система контроля качества</a><br/>
            <a href='{projects_list_url}'>Список всех проектов</a>
            """
    return HttpResponse(html)


def projects_list(request):
    projects = Project.objects.all() # запрос из БД всех объектов типа Project
    projects_html = "<h1>Список проектов</h1><ul>"
    for project in projects:
        projects_html += f"<li><a href='{project.id}/'>{project.name}</a></li>"
    projects_html += "</ul>"
    return HttpResponse(projects_html)

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.task.all()
    response_html = f"<h1>{project.name}</h1><p>{project.description}</p>"
    
    response_html += "<h2>Задачи</h2></ul>"
    for task in tasks:
        response_html += f"<li><a href='tasks/{task.id}/'>{task.name}</a></li>"
    response_html += "</ul>"

    return HttpResponse(response_html)

def task_detail(request,project_id, task_id):
    project = get_object_or_404(Project, id=project_id)
    task = get_object_or_404(Task, id=task_id)

    response_html = f"<h1>{task.name}</h1><p>{task.description}</p>"
    return HttpResponse(response_html)


from django.views import View

class IndexView(View):
    # def get(self, request, *args, **kwargs):
    #     projects_list_url = reverse('tasks:projects_list')
    #     quality_control_url = reverse(f"{quality_control_urls.app_name}:index")
    #     html = f"""<h1>Страница приложения tasks</h1>
    #                 <a href='{projects_list_url}'>Список поектов</a><br/>
    #                 <a href='{quality_control_url}'>Система контроля качества</a>"""
    #     return HttpResponse(html)
    def get(self, request, *args, **kwargs):
        # template = render_to_string('tasks/index.html') # html файлы ищутся в папке templates. Рендер html шаблон
        # return HttpResponse(template)
        return render(request, 'tasks/index.html') # объединение рендера шаблона и отвена

from django.views.generic import ListView

class ProjectListView(ListView):
    model = Project
    template_name = 'tasks/projects_list.html' # автоматически передаются
    
    # def get(self, request, *args, **kwargs):
    #     projects = self.get_queryset()
    #     projects_html = "<h1>Список проектов</h1><ul>"
    #     for project in projects:
    #         projects_html += f"<li><a href='{project.id}/'>{project.name}</a></li>"
    #     projects_html += "</ul>"
    #     return HttpResponse(projects_html)
    
    # def get(self, request, *args, **kwargs):
    #     projects = self.get_queryset()
    #     return render(request, 'tasks/projects_list.html', {'project_list':projects})


from django.views.generic import DetailView

class ProjectDetailView(DetailView):
    model = Project
    pk_url_kwarg = 'project_id' # идентификатор будет передан как project_id
    template_name = 'tasks/project_detail.html'
    
    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     project = self.object
    #     tasks = project.task.all()
    #     response_html = f"<h1>{project.name}</h1><p>{project.description}</p>"
        
    #     response_html += "<h2>Задачи</h2><ul>"
    #     for task in tasks:
    #         response_html += f"<li><a href='tasks/{task.id}/'>{task.name}</a></li>"
    #     response_html += "</ul>"

    #     return HttpResponse(response_html)
    
    # def get(self, request, *args, **kwargs):
    #     return render(request, 'tasks/project_detail.html', {'project':self.get_object()})
        


    
class TaskDetailView(DetailView):
    model = Task
    pk_url_kwarg = 'task_id'
    template_name = 'tasks/task_detail.html' 

    # def get(self, request, *args, **kwargs):
    #     task = self.get_object()
    #     response_html = f"<h1>{task.name}</h1><p>{task.description}</p>"
    #     return HttpResponse(response_html)
    # def get(self, request, *args, **kwargs):
    #     return render(request, 'tasks/task_detail.html', {'task':self.get_object()})

from .forms import FeedbackForm, ProjectForm, TaskForm
from django.shortcuts import redirect
from django.core.mail import send_mail

def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:projects_list')
    else:
        form = ProjectForm()
    return render(request, 'tasks/project_create.html', {'form':form})

def add_task_to_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task : Task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('tasks:project_detail',project_id=project_id)
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form':form, 'project': project})

def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('tasks:project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'tasks/project_update.html', {'form':form, 'project':project})

def update_task(request, project_id, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_detail', project_id=project_id, task_id=task.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_update.html', {'form':form, 'task':task})

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    return redirect('tasks:projects_list')

def delete_task(request, project_id, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return redirect('tasks:project_detail', project_id=project_id)

def feedback_view(request):
    if request.method == "POST": # использован ли метод POST для отправки данных
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Обработка данных формы
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            recipients = ['info@example.com']
            recipients.append(email)
            # send_mail(subject,message,email,recipients)

            return redirect('/tasks') # отправляет пользователя на другую страницу в случае успешной обработки данных формы
    else:
        form = FeedbackForm()
    return render(request, 'tasks/feedback.html', {'form':form})


from django.views.generic import CreateView
from django.urls import reverse_lazy

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'tasks/project_create.html'
    success_url = reverse_lazy('tasks:projects_list')

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/add_task.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('tasks:project_detail', kwargs={'project_id':self.kwargs['project_id']})

from django.views.generic import UpdateView

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'tasks/project_update.html'
    pk_url_kwarg = 'project_id'
    success_url = reverse_lazy('tasks:projects_list')

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_update.html'
    pk_url_kwarg = 'task_id'
    
    def get_success_url(self) -> str:
        return reverse_lazy('tasks:task_detail', kwargs={'project_id':self.object.project.id, 'task_id':self.object.id})


from django.views.generic.edit import DeleteView

class ProjectDeleteView(DeleteView):
    model = Project
    pk_url_kwarg = 'project_id'
    success_url = reverse_lazy('tasks:projects_list')
    template_name = 'tasks/project_confirm_delete.html'

class TaskDeleteView(DeleteView):
    model = Task
    pk_url_kwarg = 'task_id'
    template_name = 'tasks/task_confirm_delete.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('tasks:project_detail', kwargs={'project_id':self.object.project.id})


# -----------------------------
# from django.http import Http404
# from django.shortcuts import render

# def my_view(request):
#     try:
#         # код для получения данных или выполнения действия
#         # если данные не найдены ил возникает ошибка, бросаем Http404
#         result = some_function_to_get_data()
#         if not result:
#             raise Http404
#         # код для обработки данных
#         # ...

#     except Exception as e:
#         # Обработка других ошибок
#         return render(request, 'error_template.html', {'error)message':str(e)})

# -----------------------------
# from django.http import JsonResponse
# #import asyncio - не нужно, т.к. django импортирует внутри себя ее уже

# async def async_view(request):
#     await asyncio.sleep(1) # асинхронная операция задаржки
#     return JsonResponse({'message':'Асинхронный ответ'})