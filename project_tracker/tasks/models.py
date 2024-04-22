from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# структура данных, используемая орм django
# каждый класс модели представляет собой таблицу в базе данных
# этот файл формирует основу управления данными данного приложения 


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # автоматическое сохранение времени создания проекта

    def __str__(self):
        return self.name
    
class Task(models.Model):
    STATUS_CHOICES = [
        ('New', 'Новая'),
        ('In_progress', 'В работе'),
        ('Complited', 'Завершена')
    ]

    project = models.ForeignKey(
        Project,  # отношение один ко многим: каждая задача связана с конкретным проектом
        related_name='task', # обращение к задаче по имени
        on_delete = models.CASCADE # при удалении проекта, все связанные с ним задачи также будут удалены
    )
    name = models.CharField(max_length=100) # название/заголовок задачи
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # автоматическое сохранение времени создания задачи
    updated_at = models.DateTimeField(auto_now=True) # автоматическое сохранение времени последнего сохранения задачи

    assignee = models.ForeignKey(  # отношение многие ко одному: каждая задача закреплена за конкретным пользователем, и пользователь может решать любое количество задач
        User, # указывате на пользователя, которому назначена задача 
        related_name = 'tasks', # позволяет обращаться к задачам, назначенным на пользователя через атрибут tasks
        on_delete = models.SET_NULL, # если пользователь удаляется, поле assignee = models.SET_NULL
        null = True, # допускается assignee = models.SET_NULL
        blank = True # позволяет полю быть пустым на уровне форм django
    )

    status = models.CharField(
        max_length = 50,
        choices = STATUS_CHOICES,
        default = 'New'
    )

    def __str__(self):
        return self.name