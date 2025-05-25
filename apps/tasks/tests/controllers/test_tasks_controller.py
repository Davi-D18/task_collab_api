import pytest
import json
from datetime import date
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from apps.tasks.models.tasks import Tasks


@pytest.fixture
def api_client():
    """Fixture para criar um cliente API."""
    return APIClient()


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
        titulo='Tarefa 1',
        descricao='Descrição da tarefa 1',
        prioridade='A',
        prazo=date.today(),
        status='P'
    )


@pytest.fixture
def task2(user1):
    """Fixture para criar outra tarefa para o usuário 1."""
    return Tasks.objects.create(
        usuario=user1,
        titulo='Tarefa 2',
        descricao='Descrição da tarefa 2',
        prioridade='M',
        prazo=date.today(),
        status='EA'
    )


@pytest.fixture
def task3(user2):
    """Fixture para criar uma tarefa para o usuário 2."""
    return Tasks.objects.create(
        usuario=user2,
        titulo='Tarefa 3',
        descricao='Descrição da tarefa 3',
        prioridade='B',
        prazo=date.today(),
        status='C'
    )


@pytest.fixture
def tasks_url():
    """Fixture para a URL da lista de tarefas."""
    return reverse('tasks-list')


@pytest.mark.django_db
def test_list_tasks_authenticated_returns_only_user_tasks(api_client, user1, task1, task2, task3, tasks_url):
    """Testa se um usuário autenticado consegue listar apenas suas próprias tarefas."""
    # Arrange
    api_client.force_authenticate(user=user1)
    
    # Act
    response = api_client.get(tasks_url)
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    task_titles = [task['titulo'] for task in response.data]
    assert 'Tarefa 1' in task_titles
    assert 'Tarefa 2' in task_titles
    assert 'Tarefa 3' not in task_titles


@pytest.mark.django_db
def test_list_tasks_unauthenticated_returns_401(api_client, tasks_url):
    """Testa se um usuário não autenticado não consegue listar tarefas."""
    # Act
    response = api_client.get(tasks_url)
    
    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_task_authenticated_creates_new_task(api_client, user1, tasks_url):
    """Testa se um usuário autenticado consegue criar uma tarefa para si mesmo."""
    # Arrange
    api_client.force_authenticate(user=user1)
    task_data = {
        'usuario': 'usuario_teste1',
        'titulo': 'Nova Tarefa',
        'descricao': 'Descrição da nova tarefa',
        'prioridade': 'M',
        'prazo': date.today().isoformat(),
        'status': 'P'
    }
    
    # Act
    response = api_client.post(
        tasks_url,
        data=json.dumps(task_data),
        content_type='application/json'
    )
    
    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert Tasks.objects.filter(titulo='Nova Tarefa').exists()


@pytest.mark.django_db
def test_create_task_for_another_user_returns_403(api_client, user1, user2, tasks_url):
    """Testa se um usuário não consegue criar uma tarefa para outro usuário."""
    # Arrange
    api_client.force_authenticate(user=user1)
    task_data = {
        'usuario': 'usuario_teste2',
        'titulo': 'Tarefa Não Permitida',
        'descricao': 'Tentativa de criar tarefa para outro usuário',
        'prioridade': 'B',
        'prazo': date.today().isoformat(),
        'status': 'P'
    }
    
    # Act
    response = api_client.post(
        tasks_url,
        data=json.dumps(task_data),
        content_type='application/json'
    )
    
    # Assert
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not Tasks.objects.filter(titulo='Tarefa Não Permitida').exists()


@pytest.mark.django_db
def test_retrieve_own_task_returns_task_details(api_client, user1, task1):
    """Testa se um usuário consegue recuperar detalhes de sua própria tarefa."""
    # Arrange
    api_client.force_authenticate(user=user1)
    task_detail_url = reverse('tasks-detail', args=[task1.id])
    
    # Act
    response = api_client.get(task_detail_url)
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data['titulo'] == 'Tarefa 1'
    assert response.data['descricao'] == 'Descrição da tarefa 1'


@pytest.mark.django_db
def test_retrieve_another_users_task_returns_404(api_client, user1, task3):
    """Testa se um usuário não consegue recuperar detalhes de uma tarefa de outro usuário."""
    # Arrange
    api_client.force_authenticate(user=user1)
    task_detail_url = reverse('tasks-detail', args=[task3.id])
    
    # Act
    response = api_client.get(task_detail_url)
    
    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_own_task_updates_task(api_client, user1, task1):
    """Testa se um usuário consegue atualizar sua própria tarefa."""
    # Arrange
    api_client.force_authenticate(user=user1)
    task_detail_url = reverse('tasks-detail', args=[task1.id])
    update_data = {
        'usuario': 'usuario_teste1',
        'titulo': 'Tarefa 1 Atualizada',
        'descricao': 'Descrição atualizada',
        'prioridade': 'B',
        'prazo': date.today().isoformat(),
        'status': 'EA'
    }
    
    # Act
    response = api_client.put(
        task_detail_url,
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    updated_task = Tasks.objects.get(id=task1.id)
    assert updated_task.titulo == 'Tarefa 1 Atualizada'
    assert updated_task.status == 'EA'


@pytest.mark.django_db
def test_delete_own_task_removes_task(api_client, user1, task1):
    """Testa se um usuário consegue excluir sua própria tarefa."""
    # Arrange
    api_client.force_authenticate(user=user1)
    task_detail_url = reverse('tasks-detail', args=[task1.id])
    
    # Act
    response = api_client.delete(task_detail_url)
    
    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Tasks.objects.filter(id=task1.id).exists()


@pytest.mark.django_db
def test_delete_another_users_task_returns_404(api_client, user1, task3):
    """Testa se um usuário não consegue excluir a tarefa de outro usuário."""
    # Arrange
    api_client.force_authenticate(user=user1)
    task_detail_url = reverse('tasks-detail', args=[task3.id])
    
    # Act
    response = api_client.delete(task_detail_url)
    
    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Tasks.objects.filter(id=task3.id).exists()