from rest_framework import serializers
from .models import ProjectTask, Project, Subject, Status
from django.contrib.auth import get_user_model
from .utils import get_image_path
from itertools import groupby
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


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
        fields = ['id', 'name', 'status', 'comments', 'project_users', 'all_subtasks', 'all_done_subtasks']

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
    class Meta:
        model = ProjectTask
        fields = ['description', 'priority', 'date', 'project_user', 'status']
