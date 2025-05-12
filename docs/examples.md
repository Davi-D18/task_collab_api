# Exemplos de Uso

Este documento fornece exemplos práticos de uso da API Task Collab para cenários comuns.

## Índice

- [Autenticação](#autenticação)
- [Gerenciamento de Tarefas](#gerenciamento-de-tarefas)
- [Filtragem e Ordenação](#filtragem-e-ordenação)
- [Paginação](#paginação)
- [Exemplos com Diferentes Ferramentas](#exemplos-com-diferentes-ferramentas)

## Autenticação

### Registro de Usuário

**Requisição:**
```bash
curl -X POST \
  http://localhost:8000/api/v1/accounts/register/ \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "novousuario",
    "email": "usuario@exemplo.com",
    "password": "senhasegura123"
}'
```

**Resposta:**
```json
{
  "username": "novousuario",
  "email": "usuario@exemplo.com"
}
```

### Login e Obtenção de Tokens

**Requisição:**
```bash
curl -X POST \
  http://localhost:8000/api/v1/accounts/login/ \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "novousuario",
    "password": "senhasegura123"
}'
```

**Resposta:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Atualização de Token

**Requisição:**
```bash
curl -X POST \
  http://localhost:8000/api/v1/accounts/login/refresh/ \
  -H 'Content-Type: application/json' \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}'
```

**Resposta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Gerenciamento de Tarefas

### Criar uma Nova Tarefa

**Requisição:**
```bash
curl -X POST \
  http://localhost:8000/api/v1/tasks/ \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...' \
  -H 'Content-Type: application/json' \
  -d '{
    "usuario": "novousuario",
    "titulo": "Implementar nova funcionalidade",
    "descricao": "Adicionar sistema de notificações ao aplicativo",
    "prioridade": "A",
    "prazo": "2023-06-30",
    "status": "P"
}'
```

**Resposta:**
```json
{
  "id": 1,
  "titulo": "Implementar nova funcionalidade",
  "descricao": "Adicionar sistema de notificações ao aplicativo",
  "prioridade": "A",
  "prazo": "2023-06-30",
  "status": "P",
  "criado_em": "2023-05-05T10:00:00Z"
}
```

### Listar Todas as Tarefas

**Requisição:**
```bash
curl -X GET \
  http://localhost:8000/api/v1/tasks/ \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
```

**Resposta:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "titulo": "Implementar nova funcionalidade",
      "descricao": "Adicionar sistema de notificações ao aplicativo",
      "prioridade": "A",
      "prazo": "2023-06-30",
      "status": "P",
      "criado_em": "2023-05-05T10:00:00Z"
    },
    {
      "id": 2,
      "titulo": "Revisar documentação",
      "descricao": "Atualizar a documentação da API",
      "prioridade": "M",
      "prazo": "2023-05-20",
      "status": "EA",
      "criado_em": "2023-05-06T14:30:00Z"
    }
  ]
}
```

### Obter Detalhes de uma Tarefa

**Requisição:**
```bash
curl -X GET \
  http://localhost:8000/api/v1/tasks/1/ \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
```

**Resposta:**
```json
{
  "id": 1,
  "titulo": "Implementar nova funcionalidade",
  "descricao": "Adicionar sistema de notificações ao aplicativo",
  "prioridade": "A",
  "prazo": "2023-06-30",
  "status": "P",
  "criado_em": "2023-05-05T10:00:00Z"
}
```

### Atualizar uma Tarefa

**Requisição:**
```bash
curl -X PUT \
  http://localhost:8000/api/v1/tasks/1/ \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...' \
  -H 'Content-Type: application/json' \
  -d '{
    "usuario": "novousuario",
    "titulo": "Implementar nova funcionalidade",
    "descricao": "Adicionar sistema de notificações ao aplicativo com suporte a push notifications",
    "prioridade": "A",
    "prazo": "2023-07-15",
    "status": "EA"
}'
```

**Resposta:**
```json
{
  "id": 1,
  "titulo": "Implementar nova funcionalidade",
  "descricao": "Adicionar sistema de notificações ao aplicativo com suporte a push notifications",
  "prioridade": "A",
  "prazo": "2023-07-15",
  "status": "EA",
  "criado_em": "2023-05-05T10:00:00Z"
}
```

### Atualização Parcial de uma Tarefa

**Requisição:**
```bash
curl -X PATCH \
  http://localhost:8000/api/v1/tasks/1/ \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...' \
  -H 'Content-Type: application/json' \
  -d '{
    "status": "C"
}'
```

**Resposta:**
```json
{
  "id": 1,
  "titulo": "Implementar nova funcionalidade",
  "descricao": "Adicionar sistema de notificações ao aplicativo com suporte a push notifications",
  "prioridade": "A",
  "prazo": "2023-07-15",
  "status": "C",
  "criado_em": "2023-05-05T10:00:00Z"
}
```

### Excluir uma Tarefa

**Requisição:**
```bash
curl -X DELETE \
  http://localhost:8000/api/v1/tasks/1/ \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
```

**Resposta:**
```
204 No Content
```

## Filtragem e Ordenação

### Filtrar por Status

**Requisição:**
```bash
curl -X GET \
  'http://localhost:8000/api/v1/tasks/?status=P' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
```

### Filtrar por Prioridade

**Requisição:**
```bash
curl -X GET \
  'http://localhost:8000/api/v1/tasks/?prioridade=A' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
```

### Filtrar por Título (Busca Parcial)

**Requisição:**
```bash
curl -X GET \
  'http://localhost:8000/api/v1/tasks/?titulo=Implementar' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
```

### Ordenar por Prazo (Ascendente)

**Requisição:**
```bash
curl -X GET \
  'http://localhost:8000/api/v1/tasks/?ordering=prazo' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
```

### Ordenar por Prioridade (Descendente)

**Requisição:**
```bash
curl -X GET \
  'http://localhost:8000/api/v1/tasks/?ordering=-prioridade' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
```

### Combinando Filtros e Ordenação

**Requisição:**
```bash
curl -X GET \
  'http://localhost:8000/api/v1/tasks/?status=EA&prioridade=A&ordering=prazo' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
```

## Paginação

### Especificar Página e Tamanho

**Requisição:**
```bash
curl -X GET \
  'http://localhost:8000/api/v1/tasks/?page=2&page_size=5' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
```

**Resposta:**
```json
{
  "count": 12,
  "next": "http://localhost:8000/api/v1/tasks/?page=3&page_size=5",
  "previous": "http://localhost:8000/api/v1/tasks/?page=1&page_size=5",
  "results": [
    // 5 tarefas
  ]
}
```

## Exemplos com Diferentes Ferramentas

### Usando JavaScript/Fetch

```javascript
// Registro de usuário
async function registerUser() {
  const response = await fetch('http://localhost:8000/api/v1/accounts/register/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username: 'novousuario',
      email: 'usuario@exemplo.com',
      password: 'senhasegura123'
    }),
  });
  
  return await response.json();
}

// Login
async function login() {
  const response = await fetch('http://localhost:8000/api/v1/accounts/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username: 'novousuario',
      password: 'senhasegura123'
    }),
  });
  
  return await response.json();
}

// Criar tarefa
async function createTask(token) {
  const response = await fetch('http://localhost:8000/api/v1/tasks/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      usuario: 'novousuario',
      titulo: 'Nova tarefa via JavaScript',
      descricao: 'Criada usando Fetch API',
      prioridade: 'M',
      prazo: '2023-06-15',
      status: 'P'
    }),
  });
  
  return await response.json();
}

// Listar tarefas
async function listTasks(token) {
  const response = await fetch('http://localhost:8000/api/v1/tasks/', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  
  return await response.json();
}
```

### Usando Python/Requests

```python
import requests

# Configuração base
base_url = 'http://localhost:8000/api/v1'

# Registro de usuário
def register_user():
    url = f'{base_url}/accounts/register/'
    data = {
        'username': 'novousuario',
        'email': 'usuario@exemplo.com',
        'password': 'senhasegura123'
    }
    response = requests.post(url, json=data)
    return response.json()

# Login
def login():
    url = f'{base_url}/accounts/login/'
    data = {
        'username': 'novousuario',
        'password': 'senhasegura123'
    }
    response = requests.post(url, json=data)
    return response.json()

# Criar tarefa
def create_task(token):
    url = f'{base_url}/tasks/'
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'usuario': 'novousuario',
        'titulo': 'Nova tarefa via Python',
        'descricao': 'Criada usando Requests',
        'prioridade': 'M',
        'prazo': '2023-06-15',
        'status': 'P'
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Listar tarefas
def list_tasks(token):
    url = f'{base_url}/tasks/'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    return response.json()

# Exemplo de uso
if __name__ == '__main__':
    # Registrar usuário (apenas na primeira vez)
    # register_user()
    
    # Login e obter token
    tokens = login()
    access_token = tokens['access']
    
    # Criar uma tarefa
    task = create_task(access_token)
    print(f"Tarefa criada: {task['titulo']}")
    
    # Listar tarefas
    tasks = list_tasks(access_token)
    print(f"Total de tarefas: {tasks['count']}")
    for task in tasks['results']:
        print(f"- {task['titulo']} ({task['status']})")
```

## Próximos Passos

Para mais informações sobre os endpoints disponíveis e seus parâmetros, consulte a [documentação detalhada dos endpoints](./endpoints.md).