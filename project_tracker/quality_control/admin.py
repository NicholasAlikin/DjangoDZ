from django.contrib import admin
from .models import BugReport, FeatureRequest

from django.db.models import QuerySet
# Register your models here.


# Класс администратора для модели BugReport
@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin):
    list_display = ('title','project','task','status','priority','created_at','updated_at')
    list_filter = ('project','task','status','priority')
    search_fields = ('title','description')

    fieldsets = [
        (None, {'fields':['title','project','task','status','priority']})
    ]

    actions = ['increase_status','decrease_status']

    @admin.action(description="Increase status")
    def increase_status(self, request, qs:QuerySet):
        for obj in qs:
            if obj.status == BugReport.STATUS[-1]: continue
            obj.status = BugReport.STATUS[BugReport.STATUS.index(obj.status)+1]
            obj.save()
    
    @admin.action(description="Decrease status")
    def decrease_status(self, request, qs:QuerySet):
        # qs.update(status =)
        for obj in qs:
            print(obj.status)
            if obj.status == BugReport.STATUS[0]: continue
            obj.status = BugReport.STATUS[BugReport.STATUS.index(obj.status)-1]
            obj.save()


# Класс администратора для модели FeatureRequest
@admin.register(FeatureRequest)
class FeatureRequestAdmin(admin.ModelAdmin):
    list_display = ('title','project','task','status','priority','created_at','updated_at')
    list_filter = ('project','task','status','priority')
    search_fields = ('title','description')

    fieldsets = [
        (None, {'fields':['title','project','task','status','priority']})
    ]
  