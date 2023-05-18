from rest_framework import serializers
from .models import ProjectTask, Project, Subject, Status, ProjectTaskComment
from django.contrib.auth import get_user_model
from .utils import get_image_path
from itertools import groupby
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'photo']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'user']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['name']


class ProjectTaskSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    project_users = serializers.SerializerMethodField()
    all_subtasks = serializers.SerializerMethodField()
    all_done_subtasks = serializers.SerializerMethodField()
    status = StatusSerializer()
    class Meta:
        model = ProjectTask
        fields = ['id', 'name', 'status', 'comments', 'project_users', 'all_subtasks', 'all_done_subtasks', 'project']

    def get_all_subtasks(self, obj):
        return len(obj.subtask_set.all())

    def get_all_done_subtasks(self, obj):
        return len(obj.subtask_set.filter(is_done=True))


    def get_comments(self, obj):
        return len(obj.projecttaskcomment_set.all())

    def get_project_users(self, obj):
        res = []
        for user in obj.user_task.all():
            res.append("http://127.0.0.1:8000" + str(user.photo.url))
        return res

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        status_id = representation.pop('status')
        status_name = instance.status.name if instance.status else None
        grouped_representation = {status_name: representation}
        return grouped_representation





class ProjectTaskDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    class Meta:
        model = ProjectTask
        fields = ['pk', 'description', 'date', 'status', 'author', 'name', 'users', 'project']

    def get_author(self, obj):
        user = obj.user
        return str(user.first_name + user.last_name)

    def get_status(self, obj):
        return obj.status.name

    def get_users(self, obj):
        users = []
        for user in obj.user_task.all():
            users.append(user.photo.url)
        return users


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = ProjectTaskComment
        fields = ['user', 'id', 'project_task', 'description', 'date']

    def get_user(self, obj):
        user = obj.user
        return str(user.first_name)