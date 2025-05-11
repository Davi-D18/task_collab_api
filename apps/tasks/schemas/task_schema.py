from rest_framework import serializers
from apps.tasks.models.tasks import Tasks
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    usuario = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        write_only=True
    )

    def validate_usuario(self, value):
        try:
            user = User.objects.get(username=value)
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuário não existe")

    class Meta:
        model = Tasks
        fields = '__all__'    
