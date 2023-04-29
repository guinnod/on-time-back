from django.urls import path

urlpatterns = [
    path('auth/', 'base.urls'),
    path('auth/register/', 'base.urls'),
    path('auth/forgot/', 'base.urls'),
    path('profile/edit/photo/', 'base.urls'),
    path('profile/edit/password/', 'base.urls'),
    path('project/new/', 'base.urls'),
    path('project/<int:pk>/edit/'),
    path('project/<int:pk>/delete/'),
    path('project/<int:pk>/add-person/'),
    path('project/<int:pk>/'),
    path('project/<int:pk>/deadline/'),
    path('project/<int:pk>/board/<int:pk>/'),
    path('project/<int:pk>/board/<int:pk>/'),
]
