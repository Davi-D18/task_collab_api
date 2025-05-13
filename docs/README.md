# Documentação da API Task Collab

Bem-vindo à documentação da API Task Collab, uma API RESTful para gerenciamento de tarefas colaborativas.

## Índice

1. [Visão Geral](./overview.md)
2. [Autenticação](./authentication.md)
3. [Endpoints](./endpoints.md)
   - [Usuários](./endpoints/users.md)
   - [Tarefas](./endpoints/tasks.md)
4. [Modelos de Dados](./models.md)
5. [Guia de Início Rápido](./quickstart.md)
6. [Exemplos de Uso](./examples.md)
7. [FAQ](./faq.md)

## Introdução

A API Task Collab é uma solução para gerenciamento de tarefas pessoais e colaborativas. Ela permite que usuários criem, visualizem, atualizem e excluam tarefas, além de oferecer recursos de filtragem, ordenação e paginação.

## Características Principais

- Autenticação baseada em JWT (JSON Web Tokens)
- Operações CRUD completas para tarefas
- Segurança baseada em propriedade (cada usuário só acessa suas próprias tarefas)

## Requisitos

- Python 3.8+
- Django 4.0+
- Django REST Framework 3.13+
- Outras dependências listadas em `requirements.txt`

## Instalação

Consulte o [Guia de Início Rápido](./quickstart.md) para instruções detalhadas sobre como configurar e executar a API em seu ambiente local.

## Documentação da API

A documentação interativa da API está disponível em `/swagger/` quando o servidor está em execução.

## Suporte

Para questões e suporte, consulte a seção [FAQ](./faq.md) ou abra uma issue no repositório do projeto.