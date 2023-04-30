from django.urls import path
from . import api_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('auth/', api_views.Login.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('subject/', api_views.SubjectList.as_view()),
    path('project/', api_views.ProjectList.as_view()),
    path('tasks/', api_views.TaskList.as_view()),
    # path('auth/register/', 'base.urls'),
    # path('auth/forgot/', 'base.urls'),
    # path('profile/edit/photo/', 'base.urls'),
    # path('profile/edit/password/', 'base.urls'),
    # path('project/new/', 'base.urls'),
    # path('project/<int:pk>/edit/'),
    # path('project/<int:pk>/delete/'),
    # path('project/<int:pk>/add-person/'),
    # path('project/<int:pk>/'),
    # path('project/<int:pk>/deadline/'),
    # path('project/<int:pk>/board/<int:pk>/'),
    # path('project/<int:pk>/board/<int:pk>/'),
]
