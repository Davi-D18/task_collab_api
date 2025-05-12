from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from apps.tasks.models.tasks import Tasks
import json
from datetime import date


class TasksViewSetTestCase(TestCase):
    """
    Testes para o TasksViewSet que gerencia as operações CRUD de tarefas.
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
        
        # Cria tarefas para o usuário 1
        self.task1 = Tasks.objects.create(
            usuario=self.user1,
            titulo='Tarefa 1',
            descricao='Descrição da tarefa 1',
            prioridade='A',
            prazo=date.today(),
            status='P'
        )
        
        self.task2 = Tasks.objects.create(
            usuario=self.user1,
            titulo='Tarefa 2',
            descricao='Descrição da tarefa 2',
            prioridade='M',
            prazo=date.today(),
            status='EA'
        )
        
        # Cria uma tarefa para o usuário 2
        self.task3 = Tasks.objects.create(
            usuario=self.user2,
            titulo='Tarefa 3',
            descricao='Descrição da tarefa 3',
            prioridade='B',
            prazo=date.today(),
            status='C'
        )
        
        # Cliente API para fazer requisições
        self.client = APIClient()
        
        # URLs para os endpoints
        self.tasks_url = reverse('tasks-list')
    
    def test_list_tasks_authenticated(self):
        """
        Testa se um usuário autenticado consegue listar apenas suas próprias tarefas.
        """
        # Autentica o usuário 1
        self.client.force_authenticate(user=self.user1)
        
        # Faz a requisição GET para listar tarefas
        response = self.client.get(self.tasks_url)
        
        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se apenas as tarefas do usuário 1 foram retornadas
        self.assertEqual(len(response.data), 2)
        
        # Verifica se os títulos das tarefas estão corretos
        task_titles = [task['titulo'] for task in response.data]
        self.assertIn('Tarefa 1', task_titles)
        self.assertIn('Tarefa 2', task_titles)
        self.assertNotIn('Tarefa 3', task_titles)
    
    def test_list_tasks_unauthenticated(self):
        """
        Testa se um usuário não autenticado não consegue listar tarefas.
        """
        # Faz a requisição GET sem autenticação
        response = self.client.get(self.tasks_url)
        
        # Verifica se a resposta foi não autorizada
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_task_authenticated(self):
        """
        Testa se um usuário autenticado consegue criar uma tarefa para si mesmo.
        """
        # Autentica o usuário 1
        self.client.force_authenticate(user=self.user1)
        
        # Dados para criar uma nova tarefa
        task_data = {
            'usuario': 'usuario_teste1',
            'titulo': 'Nova Tarefa',
            'descricao': 'Descrição da nova tarefa',
            'prioridade': 'M',
            'prazo': date.today().isoformat(),
            'status': 'P'
        }
        
        # Faz a requisição POST para criar a tarefa
        response = self.client.post(
            self.tasks_url,
            data=json.dumps(task_data),
            content_type='application/json'
        )
        
        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verifica se a tarefa foi criada no banco de dados
        self.assertTrue(Tasks.objects.filter(titulo='Nova Tarefa').exists())
    
    def test_create_task_for_another_user(self):
        """
        Testa se um usuário não consegue criar uma tarefa para outro usuário.
        """
        # Autentica o usuário 1
        self.client.force_authenticate(user=self.user1)
        
        # Tenta criar uma tarefa para o usuário 2
        task_data = {
            'usuario': 'usuario_teste2',
            'titulo': 'Tarefa Não Permitida',
            'descricao': 'Tentativa de criar tarefa para outro usuário',
            'prioridade': 'B',
            'prazo': date.today().isoformat(),
            'status': 'P'
        }
        
        # Faz a requisição POST
        response = self.client.post(
            self.tasks_url,
            data=json.dumps(task_data),
            content_type='application/json'
        )
        
        # Verifica se a resposta foi proibida
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verifica se a tarefa não foi criada
        self.assertFalse(Tasks.objects.filter(titulo='Tarefa Não Permitida').exists())
    
    def test_retrieve_own_task(self):
        """
        Testa se um usuário consegue recuperar detalhes de sua própria tarefa.
        """
        # Autentica o usuário 1
        self.client.force_authenticate(user=self.user1)
        
        # URL para a tarefa específica
        task_detail_url = reverse('tasks-detail', args=[self.task1.id])
        
        # Faz a requisição GET
        response = self.client.get(task_detail_url)
        
        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se os dados da tarefa estão corretos
        self.assertEqual(response.data['titulo'], 'Tarefa 1')
        self.assertEqual(response.data['descricao'], 'Descrição da tarefa 1')
    
    def test_retrieve_another_users_task(self):
        """
        Testa se um usuário não consegue recuperar detalhes de uma tarefa de outro usuário.
        """
        # Autentica o usuário 1
        self.client.force_authenticate(user=self.user1)
        
        # URL para a tarefa do usuário 2
        task_detail_url = reverse('tasks-detail', args=[self.task3.id])
        
        # Faz a requisição GET
        response = self.client.get(task_detail_url)
        
        # Verifica se a resposta foi não encontrada (404)
        # Isso ocorre porque o get_queryset filtra apenas as tarefas do usuário autenticado
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_own_task(self):
        """
        Testa se um usuário consegue atualizar sua própria tarefa.
        """
        # Autentica o usuário 1
        self.client.force_authenticate(user=self.user1)
        
        # URL para a tarefa específica
        task_detail_url = reverse('tasks-detail', args=[self.task1.id])
        
        # Dados para atualização
        update_data = {
            'usuario': 'usuario_teste1',
            'titulo': 'Tarefa 1 Atualizada',
            'descricao': 'Descrição atualizada',
            'prioridade': 'B',
            'prazo': date.today().isoformat(),
            'status': 'EA'
        }
        
        # Faz a requisição PUT
        response = self.client.put(
            task_detail_url,
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se a tarefa foi atualizada no banco de dados
        updated_task = Tasks.objects.get(id=self.task1.id)
        self.assertEqual(updated_task.titulo, 'Tarefa 1 Atualizada')
        self.assertEqual(updated_task.status, 'EA')
    
    def test_delete_own_task(self):
        """
        Testa se um usuário consegue excluir sua própria tarefa.
        """
        # Autentica o usuário 1
        self.client.force_authenticate(user=self.user1)
        
        # URL para a tarefa específica
        task_detail_url = reverse('tasks-detail', args=[self.task1.id])
        
        # Faz a requisição DELETE
        response = self.client.delete(task_detail_url)
        
        # Verifica se a resposta foi bem-sucedida (204 No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verifica se a tarefa foi removida do banco de dados
        self.assertFalse(Tasks.objects.filter(id=self.task1.id).exists())
    
    def test_delete_another_users_task(self):
        """
        Testa se um usuário não consegue excluir a tarefa de outro usuário.
        """
        # Autentica o usuário 1
        self.client.force_authenticate(user=self.user1)
        
        # URL para a tarefa do usuário 2
        task_detail_url = reverse('tasks-detail', args=[self.task3.id])
        
        # Faz a requisição DELETE
        response = self.client.delete(task_detail_url)
        
        # Verifica se a resposta foi não encontrada (404)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Verifica se a tarefa ainda existe no banco de dados
        self.assertTrue(Tasks.objects.filter(id=self.task3.id).exists())