import io

from .models import Project, ProjectUser, ProjectTask, Subject
from .serializers import ProjectTaskSerializer, ProjectTaskDetailSerializer, ProjectSerializer, SubjectSerializer, UserSerializer
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

import os


def get_image_path(relative_path):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, relative_path)


class CheckAuth(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({'authenticated': True}, status=HTTP_200_OK)
        else:
            return Response({'authenticated': False}, status=HTTP_401_UNAUTHORIZED)


class Temp(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        subject = Subject.objects.get(name=request.data.get('subject'))
        project_name = request.data.get('name')
        if request.user.project_set.filter(user=user, subject=subject, name=project_name).exists():
            return Response({"Project already exists"})
        project = Project(user=user, subject=subject, name=project_name)
        project.save()
        project_user = ProjectUser(project=project, user=user)
        project_user.save()
        for email in request.data.get('users'):
            user = User.objects.get(email=email)
            print(user.user_projects.filter(pk=project.pk))
            if not user.user_projects.filter(pk=project.pk).exists():
                project_user = ProjectUser(project=project, user=user)
                project_user.save()
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
        user = User(username=email, email=email, first_name=first_name, last_name=last_name,
                    confirm_code=random.randint(1000, 9999))
        if bool(photo):
            user.photo = photo
        user.is_active = False
        user.save()
        return Response(
            {'data': 'Please confirm your email address to complete the registration', 'token': user.confirm_code},
            status=HTTP_200_OK)


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


class ChangePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.password != request.data.get('password'):
            return Response('Invalid current password!', HTTP_400_BAD_REQUEST)
        if 8 > len(request.data.get('newPassword')) or len(request.data.get('newPassword')) > 20:
            return Response('Incorrect format!', HTTP_400_BAD_REQUEST)
        user.password = request.data.get('newPassword')
        user.save()
        return Response("Password changed!", HTTP_200_OK)


class ForgotPassword(APIView):
    def post(self, request):
        email = request.data.get('email')
        if len(User.objects.filter(email=email)) == 0:
            return Response('Email does not exist!', HTTP_400_BAD_REQUEST)
        user = User.objects.get(email=email)
        code = random.randint(1000, 9999)
        user.confirm_code = code
        user.save()
        return Response({'data': 'Token send', 'token': code}, HTTP_200_OK)

    def put(self, request):
        code = request.data.get('code')
        email = request.data.get('email')
        user = User.objects.get(email=email)
        if str(user.confirm_code) != code:
            return Response('Invalid code!', HTTP_400_BAD_REQUEST)
        password = request.data.get('password')
        if 8 > len(password) or len(password) > 20:
            return Response('Invalid password format!', HTTP_400_BAD_REQUEST)
        user.confirm_code = None
        user.password = password
        user.save()
        return Response('Success!', HTTP_200_OK)


class EditProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        photo = 'no'
        if bool(user.photo):
            photo = user.photo.url
        return Response(
            {'email': user.email, 'fullName': str(user.first_name + " " + user.last_name), 'photo': photo})

    def post(self, request):
        user = request.user
        if 'photo' in request.data:
            user.photo = request.data.get('photo')
        if 'email' in request.data:
            email = request.data.get('email')
            if len(User.objects.filter(email=email)) > 0 and user.email != email:
                return Response('Email is already taken', status=HTTP_400_BAD_REQUEST)
            user.email = email
            user.username = email
        if 'fullName' in request.data:
            full_name = request.data.get('fullName')
            first_name, last_name = full_name.split(' ', 1)
            user.first_name = first_name
            user.last_name = last_name
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


class StudentsList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class ProjectList(APIView):
    def get(self, request):
        user = request.user
        projects = user.user_projects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class TaskList(APIView):
    def get(self, request, pk):
        user = request.user
        project = user.user_projects.get(pk=pk)
        tasks = project.projecttask_set.all()
        serializer = ProjectTaskSerializer(tasks, many=True)
        return Response(serializer.data)


class ProjectTaskList(APIView):
    def get(self, request, pk):
        project = Project.objects.get(pk=pk)
        task = ProjectTask.objects.first()
        print(task._meta.get_field('project').related_query_name())
        return 1
        # project_tasks = project.projecttasks.all()
        # serializer = ProjectTaskSerializer(project_tasks, many=True)
        # return Response(serializer.data)


class ProjectTaskDetail(APIView):
    def get(self, request, pk1, pk2):
        project = Project.objects.get(pk=pk1)
        project_task = project.projecttask_set.get(pk=pk2)
        serializer = ProjectTaskDetailSerializer(project_task)
        return Response(serializer.data)
