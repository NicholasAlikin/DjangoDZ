"""место расположения всех url адресов

"""

"""
URL configuration for project_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from project_tracker import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls), # admin/ будет добавлен к базовому пути сайта
    #path('tasks/', tasks.views.index), # path(суфикс url адреса - т.е. часть добавляемая после доменного имени, 
    #ссылка на функцию представления, которая будет автоматически вызыватья при срабатывании url адреса и возвращать ответ на запрос)
    path('tasks/', include('tasks.urls')), # include("имя приложения.файл urls, с маршрутами приложения")
    path('quality_control/', include('quality_control.urls')),
]
