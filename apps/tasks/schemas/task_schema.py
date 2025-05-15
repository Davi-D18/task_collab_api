from rest_framework import serializers
from apps.tasks.models.tasks import Tasks
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    usuario = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        write_only=True,
    )

    status = serializers.CharField(write_only=True, required=False)
    prioridade = serializers.CharField(write_only=True, required=True)

    status_display = serializers.CharField(source='get_status_display', read_only=True)
    prioridade_display = serializers.CharField(source='get_prioridade_display', read_only=True)

    def validate_usuario(self, value):
        try:
            user = User.objects.get(username=value)
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuário não existe")

    class Meta:
        model = Tasks
        fields = '__all__'
        extra_fields = ['status_display', 'prioridade_display']