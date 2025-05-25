# Task Collab API

## Sobre o Projeto

Task Collab API é uma aplicação de gerenciamento de tarefas desenvolvida como parte do curso Técnico em Informática para Internet do SENAI. Este projeto consiste em uma API RESTful construída com Django REST Framework que permite aos usuários criar, visualizar, atualizar e excluir tarefas pessoais.

## Tecnologias Utilizadas

### Back-end
- **Django**: Framework web Python para desenvolvimento rápido
- **Django REST Framework**: Toolkit para construção de APIs RESTful
- **Simple JWT**: Implementação de autenticação JWT para Django REST Framework
- **SQLite/PostgreSql**: Banco de dados (SQLite para desenvolvimento, PostgreSql para produção)
- **Swagger**: Documentação da API

### Dependências Principais
- Django 5.2.1
- Django REST Framework 3.16.0
- djangorestframework_simplejwt 5.5.0
- drf-yasg 1.21.10 (para documentação Swagger)
- python-dotenv 1.1.0

## Arquitetura

A API segue uma arquitetura RESTful e está organizada em apps Django:

- **accounts**: Gerencia autenticação e usuários
- **tasks**: Gerencia as tarefas dos usuários
- **common**: Componentes compartilhados entre apps
- **core**: Configurações principais do projeto

## Funcionalidades

### Gerenciamento de Usuários
- Registro de novos usuários
- Autenticação via JWT (JSON Web Tokens)
- Login e geração de tokens de acesso e atualização

### Gerenciamento de Tarefas
- Criação de tarefas com título, descrição, prioridade, prazo e status
- Listagem de tarefas com opções de filtragem e ordenação
- Visualização detalhada de tarefas individuais
- Atualização completa ou parcial de tarefas
- Exclusão de tarefas
- Permissões baseadas em propriedade (usuários só podem acessar suas próprias tarefas)

## Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional, para clonar o repositório)

### Passos para Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/Davi-D18/task_collab_api.git
   cd task_collab_api
   ```

2. **Crie e ative um ambiente virtual**
   ```bash
   # Linux/macOS
   python -m venv venv
   source venv/bin/activate
   
   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```

5. **Execute as migrações do banco de dados**
   ```bash
   sh run.sh migrate
   ```

6. **Crie um superusuário (opcional)**
   ```bash
   sh run.sh createsuperuser
   ```

7. **Inicie o servidor de desenvolvimento**
   ```bash
   sh run.sh runserver
   ```

O servidor estará disponível em `http://127.0.0.1:8000/api/v1/`.

## Uso da API

### Documentação Interativa
Acesse a documentação interativa da API em:
```
http://127.0.0.1:8000/docs/
```

## Estrutura do Projeto

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
│   └── permissions/       # Classes de permissão personalizadas
│
├── core/                  # Configurações principais do projeto
│   ├── settings/          # Configurações do Django
│   └── urls.py            # Configuração de URLs principal
│
└── docs/                  # Documentação da API
```

## Documentação Detalhada

Para informações mais detalhadas sobre os endpoints disponíveis e como utilizá-los, consulte a documentação na pasta `docs/`:

- [Visão Geral](docs/overview.md)
- [Guia de Início Rápido](docs/quickstart.md)
- [Endpoints de Usuários](docs/endpoints/users.md)
- [Endpoints de Tarefas](docs/endpoints/tasks.md)

## Front-end

Este projeto é parte de uma solução completa que inclui também um front-end desenvolvido separadamente. O front-end consome esta API para fornecer uma interface gráfica amigável para gerenciamento de tarefas.

Para acessar o front-end, consulte o seguinte repositório [Link](https://github.com/Davi-D18/task_collab_front)