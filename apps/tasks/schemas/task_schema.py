from rest_framework import serializers
from apps.tasks.models.tasks import Tasks, STATUS, PRIORIDADES
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    usuario = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        write_only=True
    )

    status = serializers.ChoiceField(choices=STATUS, default="P", write_only=True)
    prioridade = serializers.ChoiceField(choices=PRIORIDADES, write_only=True)
    
    # Adiciona campo para o valor descritivo do status
    status_display = serializers.SerializerMethodField()
    
    # Adiciona campo para o valor descritivo da prioridade
    prioridade_display = serializers.SerializerMethodField()

    def get_status_display(self, obj):
        return obj.get_status()
    
    def get_prioridade_display(self, obj):
        for code, description in PRIORIDADES:
            if obj.prioridade == code:
                return description
        return "Prioridade desconhecida"

    def validate_usuario(self, value):
        try:
            user = User.objects.get(username=value)
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuário não existe")

    class Meta:
        model = Tasks
        fields = '__all__'