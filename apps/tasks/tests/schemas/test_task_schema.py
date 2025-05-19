from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from apps.tasks.schemas.task_schema import TaskSerializer
from apps.tasks.models.tasks import Tasks
from datetime import date


class TaskSerializerTestCase(TestCase):
    """
    Testes para o TaskSerializer que serializa e deserializa objetos do modelo Tasks.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.
        Cria usuários e tarefas para serem usados nos testes.
        """
        # Cria usuários para teste
        self.user = User.objects.create_user(
            username='usuario_teste',
            email='teste@example.com',
            password='senha123'
        )
        
        # Cria uma tarefa para teste
        self.task = Tasks.objects.create(
            usuario=self.user,
            titulo='Tarefa de Teste',
            descricao='Descrição da tarefa de teste',
            prioridade='M',
            prazo=date.today(),
            status='P'
        )
    
    def test_task_serialization(self):
        """
        Testa se a serialização de uma tarefa funciona corretamente.
        """
        serializer = TaskSerializer(self.task)
        data = serializer.data
        
        # Verifica se os campos foram serializados corretamente
        self.assertEqual(data['titulo'], 'Tarefa de Teste')
        self.assertEqual(data['descricao'], 'Descrição da tarefa de teste')
        self.assertEqual(data['status_display'], 'Pendente')
        self.assertEqual(data['prioridade_display'], 'Media')
        
        # Verifica se o campo 'usuario' não está presente (é write_only)
        self.assertNotIn('usuario', data)
        
        # Verifica se os campos originais não estão presentes (são write_only)
        self.assertNotIn('status', data)
        self.assertNotIn('prioridade', data)
    
    def test_task_deserialization_valid_data(self):
        """
        Testa se a deserialização de dados válidos funciona corretamente.
        """
        data = {
            'usuario': 'usuario_teste',
            'titulo': 'Nova Tarefa',
            'descricao': 'Descrição da nova tarefa',
            'prioridade': 'A',
            'prazo': date.today().isoformat(),
            'status': 'EA'
        }
        
        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        # Salva a tarefa e verifica se foi criada corretamente
        task = serializer.save()
        self.assertEqual(task.titulo, 'Nova Tarefa')
        self.assertEqual(task.usuario, self.user)
        self.assertEqual(task.status, 'EA')
    
    def test_task_deserialization_invalid_user(self):
        """
        Testa se a deserialização falha quando um usuário inválido é fornecido.
        """
        data = {
            'usuario': 'usuario_inexistente',
            'titulo': 'Tarefa Inválida',
            'descricao': 'Descrição da tarefa inválida',
            'prioridade': 'B',
            'prazo': date.today().isoformat(),
            'status': 'P'
        }
        
        serializer = TaskSerializer(data=data)
        
        # Verifica se a validação falha
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
    
    def test_task_update(self):
        """
        Testa se a atualização de uma tarefa funciona corretamente.
        """
        data = {
            'usuario': 'usuario_teste',
            'titulo': 'Tarefa Atualizada',
            'descricao': 'Descrição atualizada',
            'prioridade': 'A',
            'prazo': date.today().isoformat(),
            'status': 'C'
        }
        
        serializer = TaskSerializer(self.task, data=data)
        self.assertTrue(serializer.is_valid())
        
        # Atualiza a tarefa e verifica se foi modificada corretamente
        updated_task = serializer.save()
        self.assertEqual(updated_task.titulo, 'Tarefa Atualizada')
        self.assertEqual(updated_task.status, 'C')
        
        # Verifica se o objeto no banco de dados foi atualizado
        db_task = Tasks.objects.get(id=self.task.id)
        self.assertEqual(db_task.titulo, 'Tarefa Atualizada')
        self.assertEqual(db_task.status, 'C')