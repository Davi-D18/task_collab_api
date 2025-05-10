from rest_framework.viewsets import ModelViewSet
from apps.tasks.schemas.task_schema import TaskSerializer
from apps.tasks.models.tasks import Tasks
from apps.tasks.permissions import IsOwner
from rest_framework.exceptions import PermissionDenied

from apps.tasks.services.tasks_service import check_permission


class TasksViewSet(ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        queryset = Tasks.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        # Checa payload antes de salvar
        if not check_permission(self):
            raise PermissionDenied("Não é permitido criar tarefa para outro usuário.")
        serializer.save()
