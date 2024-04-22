from django.urls import path, re_path, include
from tasks import views

import quality_control

app_name = "tasks" # установка пространства имет приложения для url маршрутов, определенных в этом файле


urlpatterns = [
    # # Представления основанные на функциях
    # path('',views.index,name='homepage'), # адрес '' здесь эквивалентен адресу tasks/, т.к. в project_tracer/urls.py есть указание пути "tasks/"
    # path('projects/',views.projects_list,name='projects_list'),
    # path('projects/<int:project_id>/',views.project_detail, name="project_detail"),
    # path('projects/<int:project_id>/tasks/<int:task_id>/',views.task_detail, name="task_detail"),

    # Представления основанные на классах
    path('',views.IndexView.as_view(), name='index'),
    path('projects/',views.ProjectListView.as_view(),name='projects_list'),
    path('projects/<int:project_id>/',views.ProjectDetailView.as_view(), name="project_detail"),
    path('projects/<int:project_id>/tasks/<int:task_id>/',views.TaskDetailView.as_view(), name="task_detail"),
    path('project/new/', views.create_project, name='create_project'),
    path('project/<int:project_id>/add_task/', views.add_task_to_project, name='add_task_to_project'),
    path('project/create/', views.ProjectCreateView.as_view(), name='create_project'),
    path('project/<int:project_id>/add_task/', views.TaskCreateView.as_view(), name='add_task_to_project'),
    path('project/<int:project_id>/update/', views.update_project, name='update_project'),
    path('project/<int:project_id>/task/<int:task_id>/update/', views.update_task, name='update_task'),
    path('project/<int:project_id>/update/', views.ProjectUpdateView.as_view(), name='update_project'),
    path('project/<int:project_id>/task/<int:task_id>/update/', views.TaskUpdateView.as_view(), name='update_task'),
    path('project/<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('project/<int:project_id>/task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('project/<int:project_id>/delete/', views.ProjectDeleteView.as_view(), name='delete_project'),
    path('project/<int:project_id>/task/<int:task_id>/delete/', views.TaskDeleteView.as_view(), name='delete_task'),

    
]

# конвертеры пути: str, int, slug, uuid, path
# urlpatterns = [
#     path('articles/2003/', views.special_case_2003),
#     path('articles/<int:year>/', views.year_archive),
#     path('articles/<int:year>/<int:month>/', views.month_archive),
#     path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),
# ]

# при запросе "articles/2005/03/" вызовется функция views.month_archive
# при запросе "articles/2003/" вызовется views.special_case_2003, а не views.year_archive, т.к. пути проверяются по порядку в листе
# при запросе "articles/2003" н ичего не вызовется, т.к. url-адрес должен заканчиваться "/"
# при запросе "articles/2005/03/building-a-django-site/" вызовется функция views.article_detail
# --------------------------------------------
# для регулярок используется re_path вместо path
# с синтаксисом "(?P<name>pattern)" name - имя группы, patter - шаблон для сопоставления

# urlpatterns = [
#     path('articles/2003/', views.special_case_2003),
#     re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
#     re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
#     re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$', views.article_detail),
# ]

# ----------------------------------------
# Если хотим укоренить пути ниже
# from apps.main import views as main_views
# from credit import views as credit_views

# extra_patterns = [
#     path('reports/', credit_views.report),
#     path('reports/<int:id>/', credit_views.report),
#     path('charge/', credit_views.charge),
# ]

# urlpatterns = [
#     path('',main_views.homepage),
#     path('help/',include('apps.help.urls')),
#     path('credit/',include(extra_patterns))
# ]

# --------------------------------------------
# Если один префикс шаблонный используется многократно
# urlpatterns = [
#     path('<page_slug>-<page_id>/',include([
#         path('history/',views.history),  # == '<page_slug>-<page_id>/history/'
#         path('edit/',views.edit),
#         ...
#     ])),
# ]

# --------------------------------------------
# Обработка ошибок - 
# Данную ошибку можно обработать прописав что нужно вызывать в urlconf
# 
# если клиент отправил запрос, вызвавший ошибку 400
# handler400 = 'mysite.views.my_custom_bad_request_view'
# функция my_custom_bad_request_view(request,exeption) -> HttpResponseBadRequest
# по умолчанию  'django.views.defaults.bad_request()'

# если у прользователя нет разрешения для доступа к ресуру (для перехода по адресу)
# handler403 = 'mysite.views.my_custom_permission_denied_view'
# функция my_custom_permission_denied_view(request,exeption) -> HttpResponseForbidden
# по умолчанию  'django.views.defaults.permission_denied()'

# в случае, если не был найдет url-шаблон в списке шаблонов urlpatterns
# handler404 = 'mysite.views.my_custom_not_found_view'
# функция my_custom_not_found_view(request,exeption) -> HttpResponseNotFound
# по умолчанию  'django.views.defaults.page_not_found()'

# views.py
# from django.shortcuts import render
# from django.http import HttpResponseNotFound

# def custom_404(request, exception): # отображение страницы ошибки 404
#     return render(request, '404.html',status=404) 

## urls.py
# from . import views
# handler404 = 'mysite.views.custom_404' # адрес, по которому перейдется при вызове ошибки 404
# urlpatterns = [
#     ...
# ]

# в случае ошибки сервера (если есть ошибка времени выполнения)
# handler500 = 'mysite.views.my_custom_error_view'
# функция my_custom_error_view(request,exeption) -> HttpResponseServerError
# по умолчанию  'django.views.defaults.server_error()'

