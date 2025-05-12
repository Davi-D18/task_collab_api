# Endpoints de Tarefas

Este documento detalha os endpoints relacionados ao gerenciamento de tarefas na API Task Collab.

## Listar Tarefas

Retorna uma lista paginada das tarefas do usuário autenticado.

```
GET /api/v1/tasks/
```

### Parâmetros de Consulta

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| page | integer | Não | Número da página (padrão: 1) |
| page_size | integer | Não | Itens por página (padrão: 10, máximo: 100) |
| status | string | Não | Filtrar por status (P, EA, C) |
| prioridade | string | Não | Filtrar por prioridade (A, M, B) |
| titulo | string | Não | Filtrar por título (busca parcial) |
| ordering | string | Não | Campo para ordenação (ex: prazo, -prioridade) |

### Cabeçalhos da Requisição

| Cabeçalho | Valor |
|-----------|-------|
| Authorization | Bearer {token} |

### Resposta de Sucesso

**Código:** 200 OK

```json
{
  "count": 15,
  "next": "http://api.exemplo.com/api/v1/tasks/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "titulo": "Completar relatório",
      "descricao": "Finalizar o relatório mensal de vendas",
      "prioridade": "A",
      "prazo": "2023-05-15",
      "status": "P",
      "criado_em": "2023-05-01T14:30:00Z"
    },
    {
      "id": 2,
      "titulo": "Reunião com cliente",
      "descricao": "Preparar apresentação para reunião",
      "prioridade": "M",
      "prazo": "2023-05-10",
      "status": "EA",
      "criado_em": "2023-05-02T09:15:00Z"
    }
    // ... mais tarefas
  ]
}
```

### Respostas de Erro

**Código:** 401 Unauthorized

```json
{
  "detail": "As credenciais de autenticação não foram fornecidas."
}
```

### Notas

- Os resultados são paginados por padrão
- Apenas tarefas do usuário autenticado são retornadas
- Use os parâmetros de consulta para filtrar e ordenar os resultados

## Criar Tarefa

Cria uma nova tarefa para o usuário autenticado.

```
POST /api/v1/tasks/
```

### Parâmetros da Requisição

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| usuario | string | Sim | Nome de usuário (deve ser o mesmo do usuário autenticado) |
| titulo | string | Sim | Título da tarefa |
| descricao | string | Não | Descrição detalhada da tarefa |
| prioridade | string | Sim | Prioridade da tarefa (A: Alta, M: Média, B: Baixa) |
| prazo | date | Não | Data limite no formato YYYY-MM-DD |
| status | string | Não | Status da tarefa (P: Pendente, EA: Em Andamento, C: Concluída) |

### Cabeçalhos da Requisição

| Cabeçalho | Valor |
|-----------|-------|
| Authorization | Bearer {token} |
| Content-Type | application/json |

### Exemplo de Requisição

```json
{
  "usuario": "novousuario",
  "titulo": "Implementar nova funcionalidade",
  "descricao": "Adicionar sistema de notificações ao aplicativo",
  "prioridade": "A",
  "prazo": "2023-06-30",
  "status": "P"
}
```

### Resposta de Sucesso

**Código:** 201 Created

```json
{
  "id": 3,
  "titulo": "Implementar nova funcionalidade",
  "descricao": "Adicionar sistema de notificações ao aplicativo",
  "prioridade": "A",
  "prazo": "2023-06-30",
  "status": "P",
  "criado_em": "2023-05-05T10:00:00Z"
}
```

### Respostas de Erro

**Código:** 400 Bad Request

```json
{
  "titulo": [
    "Este campo é obrigatório."
  ],
  "prioridade": [
    "Valor inválido. As opções são: 'A', 'M', 'B'."
  ]
}
```

**Código:** 403 Forbidden

```json
{
  "detail": "Você não pode criar tarefa para outro usuário."
}
```

### Notas

- O campo `usuario` deve corresponder ao nome de usuário autenticado
- O status padrão é "P" (Pendente) se não for especificado
- A data de criação (`criado_em`) é gerada automaticamente

## Obter Tarefa

Retorna os detalhes de uma tarefa específica.

```
GET /api/v1/tasks/{id}/
```

### Parâmetros de URL

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| id | integer | ID da tarefa |

### Cabeçalhos da Requisição

| Cabeçalho | Valor |
|-----------|-------|
| Authorization | Bearer {token} |

### Resposta de Sucesso

**Código:** 200 OK

```json
{
  "id": 1,
  "titulo": "Completar relatório",
  "descricao": "Finalizar o relatório mensal de vendas",
  "prioridade": "A",
  "prazo": "2023-05-15",
  "status": "P",
  "criado_em": "2023-05-01T14:30:00Z"
}
```

### Respostas de Erro

**Código:** 404 Not Found

```json
{
  "detail": "Não encontrado."
}
```

### Notas

- Se a tarefa não pertencer ao usuário autenticado, a API retornará 404
- Isso é uma medida de segurança para não revelar a existência de tarefas de outros usuários

## Atualizar Tarefa

Atualiza uma tarefa existente.

```
PUT /api/v1/tasks/{id}/
```

### Parâmetros de URL

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| id | integer | ID da tarefa |

### Parâmetros da Requisição

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| usuario | string | Sim | Nome de usuário (deve ser o mesmo do usuário autenticado) |
| titulo | string | Sim | Título da tarefa |
| descricao | string | Não | Descrição detalhada da tarefa |
| prioridade | string | Sim | Prioridade da tarefa (A: Alta, M: Média, B: Baixa) |
| prazo | date | Não | Data limite no formato YYYY-MM-DD |
| status | string | Sim | Status da tarefa (P: Pendente, EA: Em Andamento, C: Concluída) |

### Cabeçalhos da Requisição

| Cabeçalho | Valor |
|-----------|-------|
| Authorization | Bearer {token} |
| Content-Type | application/json |

### Exemplo de Requisição

```json
{
  "usuario": "novousuario",
  "titulo": "Completar relatório (atualizado)",
  "descricao": "Finalizar o relatório mensal de vendas com dados atualizados",
  "prioridade": "M",
  "prazo": "2023-05-20",
  "status": "EA"
}
```

### Resposta de Sucesso

**Código:** 200 OK

```json
{
  "id": 1,
  "titulo": "Completar relatório (atualizado)",
  "descricao": "Finalizar o relatório mensal de vendas com dados atualizados",
  "prioridade": "M",
  "prazo": "2023-05-20",
  "status": "EA",
  "criado_em": "2023-05-01T14:30:00Z"
}
```

### Respostas de Erro

**Código:** 404 Not Found

```json
{
  "detail": "Não encontrado."
}
```

### Notas

- Todos os campos obrigatórios devem ser incluídos na requisição
- Para atualizações parciais, use o método PATCH em vez de PUT
- A data de criação não pode ser alterada

## Atualização Parcial de Tarefa

Atualiza parcialmente uma tarefa existente.

```
PATCH /api/v1/tasks/{id}/
```

### Parâmetros de URL

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| id | integer | ID da tarefa |

### Parâmetros da Requisição

Inclua apenas os campos que deseja atualizar.

### Cabeçalhos da Requisição

| Cabeçalho | Valor |
|-----------|-------|
| Authorization | Bearer {token} |
| Content-Type | application/json |

### Exemplo de Requisição

```json
{
  "status": "C"
}
```

### Resposta de Sucesso

**Código:** 200 OK

```json
{
  "id": 1,
  "titulo": "Completar relatório (atualizado)",
  "descricao": "Finalizar o relatório mensal de vendas com dados atualizados",
  "prioridade": "M",
  "prazo": "2023-05-20",
  "status": "C",
  "criado_em": "2023-05-01T14:30:00Z"
}
```

## Excluir Tarefa

Remove uma tarefa existente.

```
DELETE /api/v1/tasks/{id}/
```

### Parâmetros de URL

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| id | integer | ID da tarefa |

### Cabeçalhos da Requisição

| Cabeçalho | Valor |
|-----------|-------|
| Authorization | Bearer {token} |

### Resposta de Sucesso

**Código:** 204 No Content

### Respostas de Erro

**Código:** 404 Not Found

```json
{
  "detail": "Não encontrado."
}
```

### Notas

- A exclusão é permanente e não pode ser desfeita
- Apenas o proprietário da tarefa pode excluí-la

## Próximos Passos

Para exemplos práticos de uso destes endpoints, consulte a seção [Exemplos de Uso](../examples.md).