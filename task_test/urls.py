from django.urls import path, include
from rest_framework import routers
from task_test import views

app_name = 'task_test'
router = routers.DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('rest_framework.urls', namespace='rest_framework'))
]
