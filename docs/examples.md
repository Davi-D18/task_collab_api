# Exemplos de Uso

Este documento fornece exemplos práticos de uso da API Task Collab para cenários comuns.

## Índice

- [Autenticação](#autenticação)
- [Gerenciamento de Tarefas](#gerenciamento-de-tarefas)

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
[
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

## Próximos Passos

Para mais informações sobre os endpoints disponíveis e seus parâmetros, consulte a [documentação detalhada dos endpoints](./endpoints.md).