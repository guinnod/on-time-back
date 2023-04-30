from django.contrib import admin
from .models import User, Project, ProjectTask, ProjectTaskComment, Subject, UserSubject, ProjectUser, Status, SubTask
# Register your models here.


admin.site.register(User)
admin.site.register(Project)
admin.site.register(ProjectTask)
admin.site.register(ProjectTaskComment)
admin.site.register(Subject)
admin.site.register(UserSubject)
admin.site.register(ProjectUser)
admin.site.register(Status)
admin.site.register(SubTask)
