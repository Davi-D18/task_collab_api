# Tasks App

Este app gerencia o sistema de tarefas da aplicação Task Collab, permitindo que usuários criem, visualizem, atualizem e excluam suas tarefas pessoais.

## Estrutura do App
```
tasks/
├── controllers/     # Views e ViewSets para manipulação de tarefas
├── models/          # Modelos de dados para tarefas
├── schemas/         # Serializadores para conversão de dados
├── routes/          # Configuração de URLs e rotas da API
└── tests/           # Testes unitários e de integração
    ├── controllers/ # Testes para os controladores
    ├── models/      # Testes para os modelos
    ├── permissions/ # Testes para as permissões
    └── schemas/     # Testes para os serializadores
```

## Componentes Principais

### Modelo de Dados (models/tasks.py)

O modelo `Tasks` representa uma tarefa no sistema com os seguintes campos:
- `usuario`: Usuário proprietário da tarefa (ForeignKey para User)
- `titulo`: Título da tarefa (CharField)
- `descricao`: Descrição detalhada da tarefa (TextField)
- `prioridade`: Nível de prioridade (A: Alta, M: Média, B: Baixa)
- `prazo`: Data limite para conclusão (DateField)
- `status`: Estado atual da tarefa (P: Pendente, EA: Em Andamento, C: Concluída)
- `criado_em`: Data e hora de criação (DateTimeField)
- `atualizado_em`: Data e hora da última atualização (DateTimeField)
- `concluido_em`: Data e hora da conclusão da tarefa (DateTimeField)
### Serializador (schemas/task_schema.py)

O `TaskSerializer` converte objetos do modelo Tasks para JSON e vice-versa, com recursos como:
- Validação de dados de entrada
- Conversão de campos para formatos legíveis (status_display, prioridade_display)
- Controle de acesso a campos (write_only, read_only)

### Controlador (controllers/tasks_controller.py)

O `TasksViewSet` gerencia as operações CRUD para tarefas:
- Lista tarefas do usuário autenticado
- Cria novas tarefas
- Recupera detalhes de tarefas específicas
- Atualiza tarefas existentes
- Exclui tarefas

### Rotas (routes/tasks_routes.py)

Configura os endpoints da API para tarefas:
- `GET /api/v1/tasks/`: Lista todas as tarefas do usuário
- `POST /api/v1/tasks/`: Cria uma nova tarefa
- `GET /api/v1/tasks/{id}/`: Obtém detalhes de uma tarefa específica
- `PUT /api/v1/tasks/{id}/`: Atualiza uma tarefa existente
- `DELETE /api/v1/tasks/{id}/`: Exclui uma tarefa

### Permissões

O app utiliza a permissão personalizada `IsOwner` que:
- Garante que apenas usuários autenticados possam acessar as tarefas
- Restringe o acesso às tarefas apenas ao seu proprietário
- Impede a criação de tarefas para outros usuários

## Testes

O app inclui testes abrangentes para todos os componentes:
- Testes de modelo: Validam o comportamento do modelo Tasks
- Testes de serializador: Verificam a serialização/deserialização correta
- Testes de controlador: Testam os endpoints da API
- Testes de permissão: Garantem que as regras de acesso sejam aplicadas

### Executando os Testes
```bash
# Executar todos os testes do app
pytest apps.tasks -v
```

## Comandos Úteis

### Migrações
```bash
sh run.sh makemigrations tasks
sh run.sh migrate
```

### Shell para Depuração
```bash
sh run.sh shell

# Exemplo de uso no shell
from apps.tasks.models.tasks import Tasks
from django.contrib.auth.models import User
user = User.objects.first()
tasks = Tasks.objects.filter(usuario=user)
```