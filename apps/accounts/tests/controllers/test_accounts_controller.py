from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
import json

User = get_user_model()

class RegisterViewTestCase(TestCase):
    """
    Testes para a view de registro de usuários.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.
        """
        self.client = APIClient()
        self.register_url = reverse('register')
        
        # Dados para registro de usuário
        self.valid_user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        
        # Cria um usuário existente para testar duplicação
        self.existing_user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existingpassword123'
        )
    
    def test_register_valid_user(self):
        """
        Testa se um usuário válido pode ser registrado.
        """
        response = self.client.post(
            self.register_url,
            data=json.dumps(self.valid_user_data),
            content_type='application/json'
        )
        
        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verifica se o usuário foi criado no banco de dados
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Verifica se os dados retornados estão corretos
        self.assertEqual(response.data['username'], 'newuser')
        self.assertEqual(response.data['email'], 'newuser@example.com')
        
        # Verifica se a senha não está presente na resposta
        self.assertNotIn('password', response.data)
    
    def test_register_duplicate_username(self):
        """
        Testa se o registro falha quando um nome de usuário duplicado é fornecido.
        """
        duplicate_data = {
            'username': 'existinguser',  # Nome de usuário já existente
            'email': 'new@example.com',
            'password': 'newpassword123'
        }
        
        response = self.client.post(
            self.register_url,
            data=json.dumps(duplicate_data),
            content_type='application/json'
        )
        
        # Verifica se a resposta foi um erro de validação
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verifica se a mensagem de erro contém informações sobre o nome de usuário duplicado
        error_found = False
        for error in response.data['errors']:
            if error['field'] == 'username':
                error_found = True
                break
        self.assertTrue(error_found, "Erro de username não encontrado na resposta")
    
    def test_register_duplicate_email(self):
        """
        Testa se o registro falha quando um email duplicado é fornecido.
        """
        duplicate_data = {
            'username': 'newuser2',
            'email': 'existing@example.com',  # Email já existente
            'password': 'newpassword123'
        }
        
        response = self.client.post(
            self.register_url,
            data=json.dumps(duplicate_data),
            content_type='application/json'
        )
        
        # Verifica se a resposta foi um erro de validação
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verifica se a mensagem de erro contém informações sobre o email duplicado
        error_found = False
        for error in response.data['errors']:
            if error['field'] == 'email':
                error_found = True
                break
        self.assertTrue(error_found, "Erro de email não encontrado na resposta")
    
    def test_register_missing_fields(self):
        """
        Testa se o registro falha quando campos obrigatórios estão ausentes.
        """
        incomplete_data = {
            'username': 'incompleteuser',
            # Email ausente
            'password': 'incompletepassword123'
        }
        
        response = self.client.post(
            self.register_url,
            data=json.dumps(incomplete_data),
            content_type='application/json'
        )
        
        # Verifica se a resposta foi um erro de validação
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verifica se a mensagem de erro contém informações sobre o campo ausente
        error_found = False
        for error in response.data['errors']:
            if error['field'] == 'email':
                error_found = True
                break
        self.assertTrue(error_found, "Erro de email ausente não encontrado na resposta")


class TokenViewsTestCase(TestCase):
    """
    Testes para as views de obtenção e atualização de tokens.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.
        """
        self.client = APIClient()
        self.login_url = reverse('login')
        self.refresh_url = reverse('token_refresh')
        
        # Cria um usuário para teste
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Credenciais válidas usando nome de usuário
        self.valid_credentials_username = {
            'credential': 'testuser',
            'password': 'testpassword123'
        }
        
        # Credenciais válidas usando email
        self.valid_credentials_email = {
            'credential': 'test@example.com',
            'password': 'testpassword123'
        }
        
        # Credenciais inválidas
        self.invalid_credentials = {
            'credential': 'testuser',
            'password': 'wrongpassword'
        }
    
    def test_login_with_username(self):
        """
        Testa se o login funciona corretamente usando o nome de usuário.
        """
        response = self.client.post(
            self.login_url,
            data=json.dumps(self.valid_credentials_username),
            content_type='application/json'
        )
        
        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se os tokens foram retornados
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_with_email(self):
        """
        Testa se o login funciona corretamente usando o email.
        """
        response = self.client.post(
            self.login_url,
            data=json.dumps(self.valid_credentials_email),
            content_type='application/json'
        )
        
        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se os tokens foram retornados
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_invalid_credentials(self):
        """
        Testa se o login falha quando credenciais inválidas são fornecidas.
        """
        response = self.client.post(
            self.login_url,
            data=json.dumps(self.invalid_credentials),
            content_type='application/json'
        )
        
        # Verifica se a resposta foi um erro de validação
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_token_refresh(self):
        """
        Testa se a atualização de token funciona corretamente.
        """
        # Primeiro, obtém um token de atualização
        login_response = self.client.post(
            self.login_url,
            data=json.dumps(self.valid_credentials_username),
            content_type='application/json'
        )
        
        refresh_token = login_response.data['refresh']
        
        # Usa o token de atualização para obter um novo token de acesso
        refresh_response = self.client.post(
            self.refresh_url,
            data=json.dumps({'refresh': refresh_token}),
            content_type='application/json'
        )
        
        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        
        # Verifica se um novo token de acesso foi retornado
        self.assertIn('access', refresh_response.data)
    
    def test_token_refresh_invalid_token(self):
        """
        Testa se a atualização de token falha quando um token inválido é fornecido.
        """
        response = self.client.post(
            self.refresh_url,
            data=json.dumps({'refresh': 'invalid-token'}),
            content_type='application/json'
        )
        
        # Verifica se a resposta foi um erro de autenticação
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)