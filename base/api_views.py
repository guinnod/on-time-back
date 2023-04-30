from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, ProjectUser, User
from .serializers import ProjectTaskSerializer, ProjectTaskDetailSerializer, ProjectSerializer, SubjectSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK


class Login(APIView):
    def post(self, request):
        user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
        if not user:
            return Response({'error': 'Credentials are incorrect or user does not exist'}, status=HTTP_404_NOT_FOUND)
        login(request, user)
        return Response({'auth': 'ok'}, status=HTTP_200_OK)


class SubjectList(APIView):
    def get(self, request):
        user = request.user
        subjects = user.subject_set.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)


class ProjectList(APIView):
    def get(self, request):
        user = request.user
        projects = set([p for p in user.project_set.all()])
        for p in user.projectuser_set.all():
            projects.add(p.project)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class TaskList(APIView):
    def get(self, request):
        user = request.user
        tasks = []
        for projectuser in user.projectuser_set.all():
            for task in projectuser.projecttask_set.all():
                tasks.append(task)
        serializer = ProjectTaskSerializer(tasks, many=True)
        return Response(serializer.data)


class ProjectTaskList(APIView):
    def get(self, request, pk):
        project = Project.objects.get(pk=pk)
        project_tasks = project.projecttask_set.all()
        serializer = ProjectTaskSerializer(project_tasks, many=True)
        return Response(serializer.data)


class ProjectTaskDetail(APIView):
    def get(self, request, pk1, pk2):
        project = Project.objects.get(pk=pk1)
        project_task = project.projecttask_set.get(pk=pk2)
        serializer = ProjectTaskDetailSerializer(project_task)
        return Response(serializer.data)
