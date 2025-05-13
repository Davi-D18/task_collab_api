# Endpoints da API

Este documento fornece uma visão geral dos endpoints disponíveis na API Task Collab. Para detalhes específicos sobre cada grupo de endpoints, consulte os links abaixo.

## Estrutura de URL

Todos os endpoints da API seguem a estrutura:

```
/api/v1/{recurso}/
```

Onde `{recurso}` é o tipo de recurso que você deseja acessar (por exemplo, `tasks` ou `accounts`).

## Grupos de Endpoints

### Autenticação e Usuários

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | [/api/v1/accounts/register/](./endpoints/users.md#registro) | Registra um novo usuário |
| POST | [/api/v1/accounts/login/](./endpoints/users.md#login) | Obtém tokens de autenticação |
| POST | [/api/v1/accounts/login/refresh/](./endpoints/users.md#atualização-de-token) | Atualiza o token de acesso |

Para mais detalhes, consulte a [documentação de endpoints de usuários](./endpoints/users.md).

### Tarefas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | [/api/v1/tasks/](./endpoints/tasks.md#listar-tarefas) | Lista todas as tarefas do usuário |
| POST | [/api/v1/tasks/](./endpoints/tasks.md#criar-tarefa) | Cria uma nova tarefa |
| GET | [/api/v1/tasks/{id}/](./endpoints/tasks.md#obter-tarefa) | Obtém detalhes de uma tarefa específica |
| PUT | [/api/v1/tasks/{id}/](./endpoints/tasks.md#atualizar-tarefa) | Atualiza uma tarefa existente |
| DELETE | [/api/v1/tasks/{id}/](./endpoints/tasks.md#excluir-tarefa) | Exclui uma tarefa |

Para mais detalhes, consulte a [documentação de endpoints de tarefas](./endpoints/tasks.md).

## Formato de Resposta

Todas as respostas da API são retornadas no formato JSON. O formato geral de resposta segue o padrão:

### Respostas de Sucesso

Para requisições bem-sucedidas, a API retorna:

- Código de status HTTP apropriado (200, 201, 204, etc.)
- Corpo da resposta em JSON (exceto para 204 No Content)

Exemplo:
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

Para requisições com erro, a API retorna:

- Código de status HTTP apropriado (400, 401, 403, 404, etc.)
- Corpo da resposta em JSON com detalhes do erro

Exemplo:
```json
{
  "detail": "Não encontrado."
}
```

ou

```json
{
  "titulo": [
    "Este campo é obrigatório."
  ]
}
```

## Próximos Passos

Para exemplos práticos de uso da API, consulte a seção [Exemplos de Uso](./examples.md).