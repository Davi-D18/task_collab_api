from django.test import TestCase
from django.contrib.auth.models import User
from apps.tasks.models.tasks import Tasks
from datetime import date


class TasksModelTestCase(TestCase):
    """
    Testes para o modelo Tasks que representa as tarefas no sistema.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.
        Cria um usuário e tarefas para serem usados nos testes.
        """
        # Cria um usuário para teste
        self.user = User.objects.create_user(
            username='usuario_teste',
            email='teste@example.com',
            password='senha123'
        )
        
        # Cria tarefas com diferentes status
        self.task_pendente = Tasks.objects.create(
            usuario=self.user,
            titulo='Tarefa Pendente',
            descricao='Descrição da tarefa pendente',
            prioridade='A',
            prazo=date.today(),
            status='P'
        )
        
        self.task_em_andamento = Tasks.objects.create(
            usuario=self.user,
            titulo='Tarefa Em Andamento',
            descricao='Descrição da tarefa em andamento',
            prioridade='M',
            prazo=date.today(),
            status='EA'
        )
        
        self.task_concluida = Tasks.objects.create(
            usuario=self.user,
            titulo='Tarefa Concluída',
            descricao='Descrição da tarefa concluída',
            prioridade='B',
            prazo=date.today(),
            status='C'
        )
    
    def test_task_creation(self):
        """
        Testa se as tarefas foram criadas corretamente.
        """
        self.assertEqual(self.task_pendente.titulo, 'Tarefa Pendente')
        self.assertEqual(self.task_em_andamento.titulo, 'Tarefa Em Andamento')
        self.assertEqual(self.task_concluida.titulo, 'Tarefa Concluída')
        
        # Verifica se o usuário foi associado corretamente
        self.assertEqual(self.task_pendente.usuario, self.user)
        self.assertEqual(self.task_em_andamento.usuario, self.user)
        self.assertEqual(self.task_concluida.usuario, self.user)
    
    def test_get_status_method(self):
        """
        Testa o método get_status que retorna o status em formato legível.
        """
        self.assertEqual(self.task_pendente.get_status(), 'Pendente')
        self.assertEqual(self.task_em_andamento.get_status(), 'Em Andamento')
        self.assertEqual(self.task_concluida.get_status(), 'Concluída')
    
    def test_unknown_status(self):
        """
        Testa o comportamento do método get_status com um status desconhecido.
        """
        # Cria uma tarefa com status inválido (apenas para teste)
        task_invalid = Tasks(
            usuario=self.user,
            titulo='Tarefa Inválida',
            descricao='Descrição da tarefa com status inválido',
            prioridade='M',
            prazo=date.today(),
            status='X'  # Status inválido
        )
        
        # Verifica se o método retorna a mensagem de status desconhecido
        self.assertEqual(task_invalid.get_status(), 'Status desconhecido')
    
    def test_str_method(self):
        """
        Testa o método __str__ que deve retornar o título da tarefa.
        """
        self.assertEqual(str(self.task_pendente), 'Tarefa Pendente')
        self.assertEqual(str(self.task_em_andamento), 'Tarefa Em Andamento')
        self.assertEqual(str(self.task_concluida), 'Tarefa Concluída')
    
    def test_meta_options(self):
        """
        Testa as opções de Meta do modelo.
        """
        self.assertEqual(Tasks._meta.verbose_name, 'Tarefa')
        self.assertEqual(Tasks._meta.verbose_name_plural, 'Tarefas')
        self.assertEqual(Tasks._meta.ordering, ['id'])
    
    def test_field_verbose_names(self):
        """
        Testa se os nomes verbosos dos campos estão corretos.
        """
        self.assertEqual(Tasks._meta.get_field('usuario').verbose_name, 'Usuário')
        self.assertEqual(Tasks._meta.get_field('titulo').verbose_name, 'Titulo')
        self.assertEqual(Tasks._meta.get_field('descricao').verbose_name, 'Descrição')
        self.assertEqual(Tasks._meta.get_field('prioridade').verbose_name, 'Prioridade')
        self.assertEqual(Tasks._meta.get_field('prazo').verbose_name, 'Prazo')
        self.assertEqual(Tasks._meta.get_field('status').verbose_name, 'Status')
        self.assertEqual(Tasks._meta.get_field('criado_em').verbose_name, 'Criado em')