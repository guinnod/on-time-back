from rest_framework import serializers
from .models import ProjectTask, Project, Subject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'user']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = '__all__'


class ProjectTaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = '__all__'
