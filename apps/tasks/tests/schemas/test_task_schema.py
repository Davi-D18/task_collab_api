import pytest
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from apps.tasks.schemas.task_schema import TaskSerializer
from apps.tasks.models.tasks import Tasks
from datetime import date


@pytest.fixture
def user():
    """Fixture para criar um usuário de teste."""
    return User.objects.create_user(
        username='usuario_teste',
        email='teste@example.com',
        password='senha123'
    )


@pytest.fixture
def task(user):
    """Fixture para criar uma tarefa de teste."""
    return Tasks.objects.create(
        usuario=user,
        titulo='Tarefa de Teste',
        descricao='Descrição da tarefa de teste',
        prioridade='M',
        prazo=date.today(),
        status='P'
    )


@pytest.mark.django_db
def test_task_serialization_returns_correct_data(task):
    """Testa se a serialização de uma tarefa retorna os dados corretos."""
    # Arrange
    serializer = TaskSerializer(task)
    
    # Act
    data = serializer.data
    
    # Assert
    assert data['titulo'] == 'Tarefa de Teste'
    assert data['descricao'] == 'Descrição da tarefa de teste'
    assert data['status_display'] == 'Pendente'
    assert data['prioridade_display'] == 'Media'
    
    # Verifica se o campo 'usuario' não está presente (é write_only)
    assert 'usuario' not in data
    
    # Verifica se os campos originais não estão presentes (são write_only)
    assert 'status' not in data
    assert 'prioridade' not in data


@pytest.mark.django_db
def test_task_deserialization_valid_data_creates_task(user):
    """Testa se a deserialização de dados válidos cria uma tarefa corretamente."""
    # Arrange
    data = {
        'usuario': 'usuario_teste',
        'titulo': 'Nova Tarefa',
        'descricao': 'Descrição da nova tarefa',
        'prioridade': 'A',
        'prazo': date.today().isoformat(),
        'status': 'EA'
    }
    
    # Act
    serializer = TaskSerializer(data=data)
    is_valid = serializer.is_valid()
    task = serializer.save()
    
    # Assert
    assert is_valid is True
    assert task.titulo == 'Nova Tarefa'
    assert task.usuario == user
    assert task.status == 'EA'


@pytest.mark.django_db
def test_task_deserialization_invalid_user_raises_exception():
    """Testa se a deserialização falha quando um usuário inválido é fornecido."""
    # Arrange
    data = {
        'usuario': 'usuario_inexistente',
        'titulo': 'Tarefa Inválida',
        'descricao': 'Descrição da tarefa inválida',
        'prioridade': 'B',
        'prazo': date.today().isoformat(),
        'status': 'P'
    }
    
    # Act
    serializer = TaskSerializer(data=data)
    
    # Assert
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_task_update_updates_task_correctly(task, user):
    """Testa se a atualização de uma tarefa funciona corretamente."""
    # Arrange
    data = {
        'usuario': 'usuario_teste',
        'titulo': 'Tarefa Atualizada',
        'descricao': 'Descrição atualizada',
        'prioridade': 'A',
        'prazo': date.today().isoformat(),
        'status': 'C'
    }
    
    # Act
    serializer = TaskSerializer(task, data=data)
    is_valid = serializer.is_valid()
    updated_task = serializer.save()
    
    # Assert
    assert is_valid is True
    assert updated_task.titulo == 'Tarefa Atualizada'
    assert updated_task.status == 'C'
    
    # Verifica se o objeto no banco de dados foi atualizado
    db_task = Tasks.objects.get(id=task.id)
    assert db_task.titulo == 'Tarefa Atualizada'
    assert db_task.status == 'C'