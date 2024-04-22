from django.apps import AppConfig

# главная конфигурация приложения

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
