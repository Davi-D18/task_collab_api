import pytest
from django.contrib.auth.models import User
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


@pytest.fixture
def permission():
    """Fixture para criar uma instância da permissão IsOwner."""
    return IsOwner()


@pytest.fixture
def user1():
    """Fixture para criar o primeiro usuário de teste."""
    return User.objects.create_user(
        username='usuario_teste1',
        email='teste1@example.com',
        password='senha123'
    )


@pytest.fixture
def user2():
    """Fixture para criar o segundo usuário de teste."""
    return User.objects.create_user(
        username='usuario_teste2',
        email='teste2@example.com',
        password='senha123'
    )


@pytest.fixture
def task1(user1):
    """Fixture para criar uma tarefa para o usuário 1."""
    return Tasks.objects.create(
        usuario=user1,
        titulo='Tarefa do Usuário 1',
        descricao='Descrição da tarefa do usuário 1',
        prioridade='A',
        prazo=date.today(),
        status='P'
    )


@pytest.fixture
def task2(user2):
    """Fixture para criar uma tarefa para o usuário 2."""
    return Tasks.objects.create(
        usuario=user2,
        titulo='Tarefa do Usuário 2',
        descricao='Descrição da tarefa do usuário 2',
        prioridade='M',
        prazo=date.today(),
        status='EA'
    )


@pytest.fixture
def anonymous_user():
    """Fixture para criar um usuário anônimo."""
    return type('AnonymousUser', (), {'is_authenticated': False})()


@pytest.mark.django_db
def test_has_permission_authenticated_user_returns_true(permission, user1):
    """Testa se um usuário autenticado tem permissão básica."""
    # Arrange
    request = MockRequest(user=user1)
    view = MockView()
    
    # Act
    result = permission.has_permission(request, view)
    
    # Assert
    assert result is True


@pytest.mark.django_db
def test_has_permission_unauthenticated_user_raises_exception(permission, anonymous_user):
    """Testa se um usuário não autenticado não tem permissão."""
    # Arrange
    request = MockRequest(user=anonymous_user)
    view = MockView()
    
    # Act & Assert
    with pytest.raises(NotAuthenticated):
        permission.has_permission(request, view)


@pytest.mark.django_db
def test_has_permission_swagger_view_returns_true(permission):
    """Testa se a permissão é concedida para views do Swagger."""
    # Arrange
    request = MockRequest(user=None)  # Usuário não importa neste caso
    view = MockView(swagger_fake_view=True)
    
    # Act
    result = permission.has_permission(request, view)
    
    # Assert
    assert result is True


@pytest.mark.django_db
def test_has_permission_post_same_user_returns_true(permission, user1):
    """Testa se um usuário pode criar uma tarefa para si mesmo."""
    # Arrange
    request = MockRequest(
        user=user1,
        data={'usuario': 'usuario_teste1'},
        method='POST'
    )
    view = MockView()
    
    # Act
    result = permission.has_permission(request, view)
    
    # Assert
    assert result is True


@pytest.mark.django_db
def test_has_permission_post_different_user_raises_exception(permission, user1):
    """Testa se um usuário não pode criar uma tarefa para outro usuário."""
    # Arrange
    request = MockRequest(
        user=user1,
        data={'usuario': 'usuario_teste2'},
        method='POST'
    )
    view = MockView()
    
    # Act & Assert
    with pytest.raises(PermissionDenied):
        permission.has_permission(request, view)


@pytest.mark.django_db
def test_has_object_permission_owner_returns_true(permission, user1, task1):
    """Testa se o proprietário de uma tarefa tem permissão para acessá-la."""
    # Arrange
    request = MockRequest(user=user1)
    view = MockView()
    
    # Act
    result = permission.has_object_permission(request, view, task1)
    
    # Assert
    assert result is True


@pytest.mark.django_db
def test_has_object_permission_non_owner_returns_false(permission, user1, task2):
    """Testa se um não proprietário não tem permissão para acessar uma tarefa."""
    # Arrange
    request = MockRequest(user=user1)
    view = MockView()
    
    # Act
    result = permission.has_object_permission(request, view, task2)
    
    # Assert
    assert result is False