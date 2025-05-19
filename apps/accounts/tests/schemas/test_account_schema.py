from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from apps.accounts.schemas.account_schema import UserSerializer, TokenObtainPairSerializer

User = get_user_model()

class UserSerializerTestCase(TestCase):
    """
    Testes para o UserSerializer que serializa e deserializa objetos do modelo User.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.
        """
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123'
        }
        
        self.user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existingpassword123'
        )
    
    def test_user_serialization(self):
        """
        Testa se a serialização de um usuário funciona corretamente.
        """
        serializer = UserSerializer(self.user)
        data = serializer.data
        
        # Verifica se os campos foram serializados corretamente
        self.assertEqual(data['username'], 'existinguser')
        self.assertEqual(data['email'], 'existing@example.com')
        
        # Verifica se o campo 'password' não está presente (é write_only)
        self.assertNotIn('password', data)
    
    def test_user_deserialization_valid_data(self):
        """
        Testa se a deserialização de dados válidos funciona corretamente.
        """
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        
        # Salva o usuário e verifica se foi criado corretamente
        user = serializer.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpassword123'))
    
    def test_user_deserialization_duplicate_username(self):
        """
        Testa se a deserialização falha quando um nome de usuário duplicado é fornecido.
        """
        duplicate_data = {
            'username': 'existinguser',  # Nome de usuário já existente
            'email': 'new@example.com',
            'password': 'newpassword123'
        }
        
        serializer = UserSerializer(data=duplicate_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)
    
    def test_user_deserialization_duplicate_email(self):
        """
        Testa se a deserialização falha quando um email duplicado é fornecido.
        """
        duplicate_data = {
            'username': 'newuser',
            'email': 'existing@example.com',  # Email já existente
            'password': 'newpassword123'
        }
        
        serializer = UserSerializer(data=duplicate_data)
        # Agora a validação deve falhar porque adicionamos validação de email único
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)


class TokenObtainPairSerializerTestCase(TestCase):
    """
    Testes para o TokenObtainPairSerializer que gera tokens JWT.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.
        """
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        self.credentials_username = {
            'credential': 'testuser',
            'password': 'testpassword123'
        }
        
        self.credentials_email = {
            'credential': 'test@example.com',
            'password': 'testpassword123'
        }
        
        self.invalid_credentials = {
            'credential': 'testuser',
            'password': 'wrongpassword'
        }
    
    def test_token_obtain_with_username(self):
        """
        Testa se o token é gerado corretamente usando o nome de usuário como credencial.
        """
        serializer = TokenObtainPairSerializer(data=self.credentials_username)
        self.assertTrue(serializer.is_valid())
        
        # Verifica se os tokens foram gerados
        data = serializer.validated_data
        self.assertIn('access', data)
        self.assertIn('refresh', data)
    
    def test_token_obtain_with_email(self):
        """
        Testa se o token é gerado corretamente usando o email como credencial.
        """
        serializer = TokenObtainPairSerializer(data=self.credentials_email)
        self.assertTrue(serializer.is_valid())
        
        # Verifica se os tokens foram gerados
        data = serializer.validated_data
        self.assertIn('access', data)
        self.assertIn('refresh', data)
    
    def test_token_obtain_invalid_credentials(self):
        """
        Testa se a validação falha quando credenciais inválidas são fornecidas.
        """
        serializer = TokenObtainPairSerializer(data=self.invalid_credentials)
        
        # Verifica se a validação falha
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
    
    def test_token_contains_username(self):
        """
        Testa se o token gerado contém o nome de usuário no payload.
        """
        token = TokenObtainPairSerializer.get_token(self.user)
        
        # Verifica se o nome de usuário está no payload do token
        self.assertEqual(token['username'], 'testuser')