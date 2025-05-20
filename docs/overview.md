# Visão Geral da API Task Collab

## Introdução

A API Task Collab é uma solução de gerenciamento de tarefas desenvolvida com Django REST Framework. Ela permite que usuários criem e gerenciem suas tarefas pessoais, com recursos completos de CRUD (Create, Read, Update, Delete).

## Arquitetura

A API segue uma arquitetura RESTful e está organizada em apps Django:

- **accounts**: Gerencia autenticação e usuários
- **tasks**: Gerencia as tarefas dos usuários

### Estrutura do Projeto

```
task_collab_api/
├── apps/
│   ├── accounts/          # App para gerenciamento de usuários e autenticação
│   │   ├── controllers/   # Controladores (views) para operações de usuário
│   │   ├── routes/        # Definição de rotas para endpoints de usuário
│   │   └── schemas/       # Serializadores para modelos de usuário
│   │
│   └── tasks/             # App para gerenciamento de tarefas
│       ├── controllers/   # Controladores (views) para operações de tarefas
│       ├── models/        # Definição do modelo de dados para tarefas
│       ├── routes/        # Definição de rotas para endpoints de tarefas
│       └── schemas/       # Serializadores para modelos de tarefas
│
├── common/                # Componentes compartilhados entre apps
│   ├── permissions/       # Classes de permissão personalizadas
│   └── exceptions/        # Definições de exceções personalizadas e tratamento de erros
│
├── core/                  # Configurações principais do projeto
│   ├── settings/          # Configurações do Django
│   └── urls.py            # Configuração de URLs principal
│
└── docs/                  # Documentação da API
```

## Tecnologias Utilizadas

- **Django**: Framework web Python para desenvolvimento rápido
- **Django REST Framework**: Toolkit para construção de APIs RESTful
- **Simple JWT**: Implementação de autenticação JWT para Django REST Framework
- **SQLite/PostgreSql**: Banco de dados (SQLite para desenvolvimento, PostgreSql para produção)
- **Swagger/OpenAPI**: Documentação interativa da API

## Fluxo de Dados

1. O cliente envia uma requisição HTTP para um endpoint da API
2. O sistema de roteamento do Django direciona a requisição para o controlador apropriado
3. O controlador valida a autenticação e permissões do usuário
4. O controlador processa a requisição, interagindo com os modelos conforme necessário
5. Os dados são serializados para o formato JSON
6. A resposta é enviada de volta ao cliente

## Segurança

A API implementa várias camadas de segurança:

- **Autenticação JWT**: Tokens de acesso e atualização para autenticação segura
- **Permissões baseadas em propriedade**: Usuários só podem acessar suas próprias tarefas
- **Validação de dados**: Todos os dados de entrada são validados antes do processamento

## Versionamento

A API segue o padrão de versionamento semântico e está atualmente na versão v1, acessível através do prefixo `/api/v1/` em todos os endpoints.

## Próximos Passos

Para começar a usar a API, consulte o [Guia de Início Rápido](./quickstart.md) ou vá diretamente para a documentação dos [Endpoints](./endpoints.md).