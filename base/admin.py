from django.contrib import admin
from .models import User, Project, ProjectTask, ProjectTaskComment, Subject, UserSubject, ProjectUser, Status, SubTask


# Register your models here.
class ProjectUserAdmin(admin.ModelAdmin):
    list_filter = ['user']


class UserSubjectAdmin(admin.ModelAdmin):
    list_filter = ['user']


class SubjectAdmin(admin.ModelAdmin):
    search_fields = ['name', 'code']


admin.site.register(User)
admin.site.register(Project)
admin.site.register(ProjectTask)
admin.site.register(ProjectTaskComment)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(UserSubject, UserSubjectAdmin)
admin.site.register(ProjectUser, ProjectUserAdmin)
admin.site.register(Status)
admin.site.register(SubTask)
