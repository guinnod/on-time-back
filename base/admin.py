from django.contrib import admin
from .models import User, Project, ProjectTask, ProjectTaskComment
# Register your models here.


admin.site.register(User)
admin.site.register(Project)
admin.site.register(ProjectTask)
admin.site.register(ProjectTaskComment)
