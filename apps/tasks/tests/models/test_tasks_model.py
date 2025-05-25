import pytest
from django.contrib.auth.models import User
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
def task_pendente(user):
    """Fixture para criar uma tarefa com status pendente."""
    return Tasks.objects.create(
        usuario=user,
        titulo='Tarefa Pendente',
        descricao='Descrição da tarefa pendente',
        prioridade='A',
        prazo=date.today(),
        status='P'
    )


@pytest.fixture
def task_em_andamento(user):
    """Fixture para criar uma tarefa com status em andamento."""
    return Tasks.objects.create(
        usuario=user,
        titulo='Tarefa Em Andamento',
        descricao='Descrição da tarefa em andamento',
        prioridade='M',
        prazo=date.today(),
        status='EA'
    )


@pytest.fixture
def task_concluida(user):
    """Fixture para criar uma tarefa com status concluída."""
    return Tasks.objects.create(
        usuario=user,
        titulo='Tarefa Concluída',
        descricao='Descrição da tarefa concluída',
        prioridade='B',
        prazo=date.today(),
        status='C'
    )


@pytest.fixture
def task_invalid(user):
    """Fixture para criar uma tarefa com status inválido."""
    return Tasks(
        usuario=user,
        titulo='Tarefa Inválida',
        descricao='Descrição da tarefa com status inválido',
        prioridade='M',
        prazo=date.today(),
        status='X'  # Status inválido
    )


@pytest.mark.django_db
def test_task_creation_creates_tasks_correctly(task_pendente, task_em_andamento, task_concluida, user):
    """Testa se as tarefas são criadas corretamente com os atributos esperados."""
    # Arrange - já feito pelas fixtures
    
    # Assert
    assert task_pendente.titulo == 'Tarefa Pendente'
    assert task_em_andamento.titulo == 'Tarefa Em Andamento'
    assert task_concluida.titulo == 'Tarefa Concluída'
    
    # Verifica se o usuário foi associado corretamente
    assert task_pendente.usuario == user
    assert task_em_andamento.usuario == user
    assert task_concluida.usuario == user


@pytest.mark.django_db
def test_get_status_display_returns_readable_status(task_pendente, task_em_andamento, task_concluida):
    """Testa se o método get_status_display retorna o status em formato legível."""
    # Act & Assert
    assert task_pendente.get_status_display() == 'Pendente'
    assert task_em_andamento.get_status_display() == 'Em Andamento'
    assert task_concluida.get_status_display() == 'Concluída'


@pytest.mark.django_db
def test_unknown_status_returns_original_value(task_invalid):
    """Testa se um status desconhecido retorna o valor original."""
    # Act & Assert
    assert task_invalid.get_status_display() == 'X'


@pytest.mark.django_db
def test_str_method_returns_task_title(task_pendente, task_em_andamento, task_concluida):
    """Testa se o método __str__ retorna o título da tarefa."""
    # Act & Assert
    assert str(task_pendente) == 'Tarefa Pendente'
    assert str(task_em_andamento) == 'Tarefa Em Andamento'
    assert str(task_concluida) == 'Tarefa Concluída'


@pytest.mark.django_db
def test_meta_options_are_correctly_defined():
    """Testa se as opções de Meta do modelo estão definidas corretamente."""
    # Act & Assert
    assert Tasks._meta.verbose_name == 'Tarefa'
    assert Tasks._meta.verbose_name_plural == 'Tarefas'
    assert Tasks._meta.ordering == ['id']


@pytest.mark.django_db
def test_field_verbose_names_are_correctly_defined():
    """Testa se os nomes verbosos dos campos estão definidos corretamente."""
    # Act & Assert
    assert Tasks._meta.get_field('usuario').verbose_name == 'Usuário'
    assert Tasks._meta.get_field('titulo').verbose_name == 'Titulo'
    assert Tasks._meta.get_field('descricao').verbose_name == 'Descrição'
    assert Tasks._meta.get_field('prioridade').verbose_name == 'Prioridade'
    assert Tasks._meta.get_field('prazo').verbose_name == 'Prazo'
    assert Tasks._meta.get_field('status').verbose_name == 'Status'
    assert Tasks._meta.get_field('criado_em').verbose_name == 'Criado em'