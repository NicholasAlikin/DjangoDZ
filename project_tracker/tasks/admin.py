from django.contrib import admin
from .models import Project, Task

# Register your models here.
# настройка моделей приложения в интерфейсе администратора django

# admin.site.register(Project)

# Inline класс для модели Task
# простое редактирование объектов модели Task прямо в интерфейсе проекта
class TaskInline(admin.TabularInline):
    model = Task
    extra = 0 # не будут отображаться пустые формы 
    fields = ('name','project','assignee','status','created_at','updated_at') # поля, которые хотим отредактировать
    readonly_fields = ('created_at','updated_at')
    can_delete = True # возможность удаления задачи прямо в интерфесе проекта
    show_change_link = True # добавление ссылки для перехода к форме и редактированию задачи


# Класс администратора для модели Project
# как показывать модель на сайте и как с ней взаимодействовать
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at') # поля, которые будут отображаться в списке полей при создании объектов в административном интерфесе
    search_fields = ('name', 'description') # создание поисковой строки для фильтрации списка объектов
    ordering = ('created_at',) # порядок сортировки объектов по умолчанию
    date_hierarchy = 'created_at' # добавление навигации по датам (для поиска объектов)

    # Подключение inline для Task
    # список из inline классов, связанные с объектом класса Project
    inlines = [TaskInline]

# Класс администратора для модели Task
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name','project','assignee','status','created_at','updated_at')
    list_filter = ('status','assignee','project')
    search_fields = ('name','description')
    list_editable = ('status','assignee')
    readonly_fields = ('created_at','updated_at')