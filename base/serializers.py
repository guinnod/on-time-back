from rest_framework import serializers
from .models import ProjectTask, Project, Subject, Status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'photo', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'user']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectTaskSerializer(serializers.Serializer):
    name = serializers.CharField()
    status = serializers.CharField()
    comments = serializers.IntegerField()
    all_subtasks = serializers.IntegerField()
    done_subtasks = serializers.IntegerField()
    project_users = serializers.ListField()


class ProjectTaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = ['description', 'priority', 'date', 'project_user', 'status']
