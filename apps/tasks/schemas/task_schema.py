from rest_framework import serializers
from apps.tasks.models.tasks import Tasks
from apps.tasks.models.tasks import STATUS, PRIORIDADES
from django.contrib.auth.models import User


class TaskSerializer(serializers.ModelSerializer):
    usuario = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        write_only=True,
    )

    # Status e Prioridade são aceitos no POST, mas não são retornados na requisição GET
    status = serializers.CharField(
        write_only=True, required=False, default="P")
    prioridade = serializers.CharField(write_only=True, required=False)

    # Propriedades que são retornadas apenas na resposta GET, em vez de retornar as iniciais
    # dos campos salvos no banco, retorna o nome completo 
    status_display = serializers.CharField(
        source='get_status_display', read_only=True)
    prioridade_display = serializers.CharField(
        source='get_prioridade_display', read_only=True)

    def validate_usuario(self, value):
        try:
            user = User.objects.get(username=value)
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuário não existe")

    def validate(self, data):
        if data["status"] not in dict(STATUS):
            raise serializers.ValidationError("Status inválido")

        elif data["prioridade"] not in dict(PRIORIDADES):
            raise serializers.ValidationError("Prioridade inválida")

        return data
    
    
    class Meta:
        model = Tasks
        fields = '__all__'
        extra_fields = ['status_display', 'prioridade_display']