from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Subject(models.Model):
    name = models.CharField()
    code = models.CharField()
    user = models.ManyToManyField('User', through='UserSubject')
    is_deactivated = models.BooleanField()


class User(AbstractUser):
    class UserRole(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
    number = models.IntegerField()
    photo = models.ImageField()
    role = models.CharField(choices=UserRole.choices)


class UserSubject(models.Model):
    user = models.ForeignKey(User)
    subject = models.ForeignKey(Subject)


class Project(models.Model):
    name = models.CharField()
    user = models.ForeignKey(User)
    subject = models.ForeignKey(Subject)
    executor = models.ManyToManyField('User', through='ProjectUser')


class ProjectUser(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)


class Status(models.Model):
    name = models.CharField()


class ProjectTask(models.Model):
    class TaskPriority(models.TextChoices):
        URGENT = "URGENT", "Urgent"
        HIGH = "HIGH", "High"
        NORMAL = "NORMAL", "Normal"
        LOW = "Low"
    project = models.ForeignKey(Project)
    date = models.DateField()
    user = models.ForeignKey(User)
    executor = models.ManyToManyField(ProjectUser)
    priority = models.CharField(TaskPriority.choices)
    status = models.ForeignKey(Status)
    is_deactivated = models.BooleanField()


class SubTask(models.Model):
    name = models.CharField()
    project_task = models.ForeignKey(ProjectTask)


class ProjectTaskComment(models.Model):
    date = models.DateField()
    description = models.TextField()
    user = models.ForeignKey(User)
    project_task = models.ForeignKey(ProjectTask)