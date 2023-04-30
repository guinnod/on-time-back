from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=70, )
    code = models.CharField(max_length=70, )
    user = models.ManyToManyField('User', through='UserSubject')
    is_deactivated = models.BooleanField()


class User(AbstractUser):
    class UserRole(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
    number = models.IntegerField(null=True)
    photo = models.ImageField(null=True)
    role = models.CharField(max_length=70, choices=UserRole.choices, null=True)


class UserSubject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class Project(models.Model):
    name = models.CharField(max_length=70, )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, through='ProjectUser', related_name='user_projects')


class ProjectUser(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Status(models.Model):
    name = models.CharField(max_length=70, )


class ProjectTask(models.Model):
    class TaskPriority(models.TextChoices):
        URGENT = "URGENT", "Urgent"
        HIGH = "HIGH", "High"
        NORMAL = "NORMAL", "Normal"
        LOW = "Low"
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_user = models.ManyToManyField(ProjectUser)
    priority = models.CharField(max_length=70, choices=TaskPriority.choices)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    is_deactivated = models.BooleanField()


class SubTask(models.Model):
    name = models.CharField(max_length=70)
    project_task = models.ForeignKey(ProjectTask, on_delete=models.CASCADE)


class ProjectTaskComment(models.Model):
    date = models.DateField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_task = models.ForeignKey(ProjectTask, on_delete=models.CASCADE)
