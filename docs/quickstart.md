# Guia de Início Rápido

Este guia fornece instruções passo a passo para configurar e começar a usar a API Task Collab.

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional, para clonar o repositório)

## Instalação

### 1. Clone o repositório (ou baixe o código-fonte)

```bash
git clone https://github.com/Davi-D18/task_collab_api.git
cd task_collab_api
```

### 2. Crie e ative um ambiente virtual

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto baseado no arquivo `.env.example`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure as variáveis necessárias de banco de dados (caso queira usar outro):

```env
DB_NAME=nome-do-banco
DB_USER=usuario
DB_PASSWORD=senha
DB_HOST=url-para-o-banco(ou localhost para um banco de dados local)
DB_PORT=porta
```

### 5. Execute as migrações do banco de dados

```bash
python manage.py migrate
```

### 6. Crie um superusuário (opcional, para acesso ao admin)

```bash
python manage.py createsuperuser
```

### 7. Inicie o servidor de desenvolvimento

```bash
python manage.py runserver
```

O servidor estará disponível em `http://127.0.0.1:8000/api/v1/`.

## Primeiros Passos

### Acessando a documentação interativa

Acesse a documentação interativa da API em:

```
http://127.0.0.1:8000/docs/
```

### Registrando um usuário

Para começar a usar a API, primeiro registre um usuário:

```bash
curl -X POST \
  http://127.0.0.1:8000/api/v1/accounts/register/ \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "usuario_teste",
    "email": "usuario@exemplo.com", # Opcional
    "password": "senha123"
}'
```

### Obtendo tokens de autenticação

Após registrar um usuário, obtenha tokens de autenticação:

```bash
curl -X POST \
  http://127.0.0.1:8000/api/v1/accounts/login/ \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "usuario_teste",
    "password": "senha123"
}'
```

A resposta incluirá tokens de acesso e atualização:

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Criando uma tarefa

Use o token de acesso para criar uma tarefa:

```bash
curl -X POST \
  http://127.0.0.1:8000/api/v1/tasks/ \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...' \
  -H 'Content-Type: application/json' \
  -d '{
    "usuario": "usuario_teste",
    "titulo": "Minha primeira tarefa",
    "descricao": "Descrição da minha primeira tarefa",
    "prioridade": "M",
    "prazo": "2023-12-31",
    "status": "P"
}'
```

### Listando tarefas

Para listar suas tarefas:

```bash
curl -X GET \
  http://127.0.0.1:8000/api/v1/tasks/ \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
```

## Configuração para Produção

Para ambientes de produção, recomendamos:

1. Configurar um servidor web como Nginx ou Apache
2. Usar Gunicorn ou uWSGI como servidor WSGI
3. Configurar um banco de dados PostgreSQL ou MySQL
4. Definir `DEBUG=False` no arquivo `.env`
5. Configurar HTTPS

Exemplo de configuração para produção no arquivo `.env`:

```
DJANGO_SECRET_KEY=chave-secreta-longa-e-aleatoria
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com
DB_NAME=task_collab
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

## Próximos Passos

Agora que você tem a API em execução, consulte:

- [Documentação dos Endpoints](./endpoints.md) para detalhes sobre como usar a API
- [Exemplos de Uso](./examples.md) para casos de uso comuns
- [Modelos de Dados](./models.md) para entender a estrutura de dados