from .models import Project, ProjectUser, ProjectTask
from .serializers import ProjectTaskSerializer, ProjectTaskDetailSerializer, ProjectSerializer, SubjectSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer

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


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():

            confirmation_code = get_random_string(length=16)

            user = serializer.save()

            user.confirmation_code = confirmation_code

            subject = 'Please confirm your email address'
            message = render_to_string('registration/confirmation_email.html', {
                'user': user,
                'confirmation_code': confirmation_code,
            })
            from_email = 'noreply@example.com'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)

            # Return a response indicating that the user needs to confirm their email address
            return Response({'detail': 'Please check your email to confirm your address.'},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        confirmation_code = request.data.get('confirmation_code')
        password = request.data.get('password')

        try:
            user = User.objects.get(confirmation_code=confirmation_code)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid confirmation code.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()

        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class SubjectList(APIView):
    def get(self, request):
        print(vars(request))
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
