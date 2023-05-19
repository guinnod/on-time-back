from django.urls import path
from . import api_views
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('login/', api_views.Login.as_view()),
    path('register/', api_views.Register.as_view()),
    path('confirm/', api_views.Confirm.as_view()),
    path('change-password/', api_views.ChangePassword.as_view()),
    path('forgot-password/', api_views.ForgotPassword.as_view()),
    path('edit-profile/', api_views.EditProfile.as_view()),
    path('subject/', api_views.SubjectList.as_view()),
    path('students/', api_views.StudentsList.as_view()),
    path('project/', api_views.ProjectList.as_view()),
    path('project/<int:pk>/', api_views.ProjectDetail.as_view()),
    path('task/<int:pk>/', api_views.TaskList.as_view()),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('temp/', api_views.Temp.as_view()),
    path('check-auth/', api_views.CheckAuth.as_view()),
    path('project-users/', api_views.GetProjectUsers.as_view()),
    path('add-task/', api_views.AddTask.as_view()),
    path('add-user-project/', api_views.AddProjectToUser.as_view()),
    path('task-detail/<int:pk1>/<int:pk2>/', api_views.ProjectTaskDetail.as_view()),
    path('add-comment/<int:pk1>/<int:pk2>/', api_views.CommentToTask.as_view()),
    path('set-subtask/<int:pk1>/<int:pk2>/', api_views.SetSubTask.as_view()),
    path('all-tasks/', api_views.AllUserTasks.as_view()),
]
