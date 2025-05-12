from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from common.permissions.is_owner import IsOwner
from apps.tasks.models.tasks import Tasks
from datetime import date


class MockView:
    """
    Classe auxiliar para simular uma view do DRF.
    """
    def __init__(self, swagger_fake_view=False):
        self.swagger_fake_view = swagger_fake_view


class MockRequest:
    """
    Classe auxiliar para simular uma requisição com um usuário.
    """
    def __init__(self, user, data=None, method='GET'):
        self.user = user
        self.data = data or {}
        self.method = method


class IsOwnerPermissionTestCase(TestCase):
    """
    Testes para a classe de permissão IsOwner.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.
        Cria usuários e tarefas para serem usados nos testes.
        """
        # Cria usuários para teste
        self.user1 = User.objects.create_user(
            username='usuario_teste1',
            email='teste1@example.com',
            password='senha123'
        )
        
        self.user2 = User.objects.create_user(
            username='usuario_teste2',
            email='teste2@example.com',
            password='senha123'
        )
        
        # Cria uma tarefa para o usuário 1
        self.task1 = Tasks.objects.create(
            usuario=self.user1,
            titulo='Tarefa do Usuário 1',
            descricao='Descrição da tarefa do usuário 1',
            prioridade='A',
            prazo=date.today(),
            status='P'
        )
        
        # Cria uma tarefa para o usuário 2
        self.task2 = Tasks.objects.create(
            usuario=self.user2,
            titulo='Tarefa do Usuário 2',
            descricao='Descrição da tarefa do usuário 2',
            prioridade='M',
            prazo=date.today(),
            status='EA'
        )
        
        # Instancia a classe de permissão
        self.permission = IsOwner()
    
    def test_has_permission_authenticated_user(self):
        """
        Testa se um usuário autenticado tem permissão básica.
        """
        request = MockRequest(user=self.user1)
        view = MockView()
        
        # Verifica se o usuário autenticado tem permissão
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_has_permission_unauthenticated_user(self):
        """
        Testa se um usuário não autenticado não tem permissão.
        """
        # Cria um usuário anônimo
        anonymous_user = type('AnonymousUser', (), {'is_authenticated': False})()
        request = MockRequest(user=anonymous_user)
        view = MockView()
        
        # Verifica se o método levanta a exceção NotAuthenticated
        with self.assertRaises(NotAuthenticated):
            self.permission.has_permission(request, view)
    
    def test_has_permission_swagger_view(self):
        """
        Testa se a permissão é concedida para views do Swagger.
        """
        request = MockRequest(user=None)  # Usuário não importa neste caso
        view = MockView(swagger_fake_view=True)
        
        # Verifica se a permissão é concedida para views do Swagger
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_has_permission_post_same_user(self):
        """
        Testa se um usuário pode criar uma tarefa para si mesmo.
        """
        request = MockRequest(
            user=self.user1,
            data={'usuario': 'usuario_teste1'},
            method='POST'
        )
        view = MockView()
        
        # Verifica se o usuário tem permissão para criar uma tarefa para si mesmo
        self.assertTrue(self.permission.has_permission(request, view))
    
    def test_has_permission_post_different_user(self):
        """
        Testa se um usuário não pode criar uma tarefa para outro usuário.
        """
        request = MockRequest(
            user=self.user1,
            data={'usuario': 'usuario_teste2'},
            method='POST'
        )
        view = MockView()
        
        # Verifica se o método levanta a exceção PermissionDenied
        with self.assertRaises(PermissionDenied):
            self.permission.has_permission(request, view)
    
    def test_has_object_permission_owner(self):
        """
        Testa se o proprietário de uma tarefa tem permissão para acessá-la.
        """
        request = MockRequest(user=self.user1)
        view = MockView()
        
        # Verifica se o proprietário tem permissão para acessar sua própria tarefa
        self.assertTrue(self.permission.has_object_permission(request, view, self.task1))
    
    def test_has_object_permission_non_owner(self):
        """
        Testa se um não proprietário não tem permissão para acessar uma tarefa.
        """
        request = MockRequest(user=self.user1)
        view = MockView()
        
        # Verifica se um não proprietário não tem permissão para acessar a tarefa de outro usuário
        self.assertFalse(self.permission.has_object_permission(request, view, self.task2))