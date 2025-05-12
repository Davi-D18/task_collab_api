from rest_framework.viewsets import ModelViewSet
from apps.tasks.schemas.task_schema import TaskSerializer
from apps.tasks.models.tasks import Tasks
from common.permissions.is_owner import IsOwner


class TasksViewSet(ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
            
        # Filtra as tarefas pelo usuário autenticado
        queryset = Tasks.objects.filter(usuario=self.request.user)
        return queryset