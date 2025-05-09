from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from apps.tasks.schemas.task_schema import TaskSerializer
from apps.tasks.models.tasks import Tasks

class TasksViewSet(ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
