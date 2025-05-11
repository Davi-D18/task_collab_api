from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    # Define o campo password como apenas escrita, garantindo que a senha 
    # nunca seja retornada nas respostas da API
    password = serializers.CharField(write_only=True)
    
    class Meta:
        # Usa o modelo de usuário configurado no projeto, permitindo flexibilidade caso o modelo seja personalizado
        model = get_user_model()
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Sobrescreve o método create para usar create_user em vez de create normal
        # Isso garante que a senha seja devidamente criptografada antes de salvar no banco
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),  # Usa .get() para permitir email opcional
            password=validated_data['password']
        )
        return user


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Estende o token JWT padrão para incluir informações adicionais do usuário
        token = super().get_token(user)
        # Adiciona o nome de usuário ao payload do token, permitindo que o frontend
        # tenha acesso a esta informação sem fazer uma requisição adicional
        token['username'] = user.username
        return token
