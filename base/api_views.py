from .models import Project, ProjectUser, ProjectTask
from .serializers import ProjectTaskSerializer, ProjectTaskDetailSerializer, ProjectSerializer, SubjectSerializer
from django.contrib.auth import authenticate
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import random

User = get_user_model()


class CheckAuth(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({'authenticated': True}, status=HTTP_200_OK)
        else:
            return Response({'authenticated': False}, status=HTTP_401_UNAUTHORIZED)


class Temp(APIView):
    def post(self, request):
        return Response({}, status=HTTP_200_OK)


class Login(APIView):
    def post(self, request):
        user = authenticate(email=request.data.get("email"), password=request.data.get("password"))
        if not user:
            return Response({'error': 'Email or password is incorrect'}, status=HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=HTTP_200_OK)


class Register(APIView):
    def post(self, request):
        email = request.data.get('email')
        full_name = request.data.get('fullName')
        photo = request.FILES.get('photo')
        first_name, last_name = full_name.split(' ', 1)
        if len(User.objects.filter(email=email)) > 0:
            return Response('Email is already taken or confirmation code is already send', status=HTTP_400_BAD_REQUEST)
        user = User(username=email,  email=email, first_name=first_name, last_name=last_name, confirm_code=random.randint(1000, 9999))
        if photo is not None:
            user.photo = photo
        user.is_active = False
        user.save()
        return Response({'data': 'Please confirm your email address to complete the registration', 'token': user.confirm_code}, status=HTTP_200_OK)


class Confirm(APIView):
    def post(self, request):
        token = request.data.get('token')
        email = request.data.get('email')
        if len(User.objects.filter(email=email)) == 0:
            return Response({'error': 'Invalid email'}, status=HTTP_400_BAD_REQUEST)
        user = User.objects.get(email=email)
        if str(user.confirm_code) == token:
            new_token = random.randint(1000, 9999)
            user.confirm_code = new_token
            user.save()
            return Response({'data': 'Success! You can create password', 'token': new_token}, HTTP_200_OK)
        return Response({'error': 'Invalid token'}, status=HTTP_400_BAD_REQUEST)

    def put(self, request):
        email = request.data.get('email')
        user_token = request.data.get('token')
        user = User.objects.get(email=email)
        if str(user.confirm_code) == user_token:
            password = request.data.get('password')
            user.password = password
            user.confirm_code = None
            user.is_active = True
            user.save()
            return Response('Congratulations!', HTTP_200_OK)
        return Response('Invalid token', HTTP_400_BAD_REQUEST)


class EditProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        if 'photo' in request.data:
            user.photo = request.data.get('photo')
            user.save()
        return Response('Saved!', HTTP_200_OK)


class SubjectList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
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
        taskss = ProjectTask.objects.get(pk=1)
        for projectuser in user.projectuser_set.all():
            for task in projectuser.projecttask_set.all():
                tasks.append(
                    {"name": task.name, "status": task.status.name, "comments": len(task.projecttaskcomment_set.all()),
                     "all_subtasks": len(task.subtask_set.all()), "done_subtasks": 5, "project_users": []})
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
