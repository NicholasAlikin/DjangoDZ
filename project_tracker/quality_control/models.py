from django.db import models
import tasks
import tasks.models
# Create your models here.

class BugReport(models.Model):
    STATUS_CHOICES = [
            ('New', 'Новый'),
            ('In_progress', 'В работе'),
            ('Complited', 'Завершен')
        ]
    STATUS = [status[0] for status in STATUS_CHOICES]

    PRIORITY_CHOICES = [
            ('1','1'),
            ('2','2'),
            ('3','3'),
            ('4','4'),
            ('5','5')
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()

    project = models.ForeignKey(
        tasks.models.Project,
        on_delete=models.CASCADE
    )

    task = models.ForeignKey(
        tasks.models.Task,
        on_delete = models.SET_NULL,
        null = True,
        blank = True
    )

    status = models.CharField(
        max_length = 20,
        choices = STATUS_CHOICES,
        default = 'New'
    )

    priority = models.CharField(
        max_length = 10,
        choices = PRIORITY_CHOICES,
        default = '1'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class FeatureRequest(models.Model):
    STATUS_CHOICES = [
            ('Considering', 'Рассмотрение'),
            ('Accepted', 'Принято'),
            ('Rejected', 'Отклонено')
        ]
    PRIORITY_CHOICES = [
            ('1','1'),
            ('2','2'),
            ('3','3'),
            ('4','4'),
            ('5','5')
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()

    project = models.ForeignKey(
        tasks.models.Project,
        on_delete=models.CASCADE
    )

    task = models.ForeignKey(
        tasks.models.Task,
        on_delete = models.SET_NULL,
        null = True,
        blank = True
    )

    status = models.CharField(
        max_length = 20,
        choices = STATUS_CHOICES,
        default = 'New'
    )

    priority = models.CharField(
        max_length = 10,
        choices = PRIORITY_CHOICES,
        default = '1'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title