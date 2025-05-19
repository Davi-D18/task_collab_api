# Accounts App

Este app gerencia a autenticação e o registro de usuários na aplicação Task Collab, implementando um sistema de autenticação baseado em JWT (JSON Web Tokens).

## Estrutura do App
```
accounts/
├── controllers/     # Views para autenticação e registro de usuários
├── schemas/         # Serializadores para usuários e tokens
├── routes/          # Configuração de URLs e rotas da API
└── tests/           # Testes unitários e de integração
    ├── controllers/ # Testes para os controladores
    └── schemas/     # Testes para os serializadores
```

## Componentes Principais

### Serializadores (schemas/account_schema.py)

#### UserSerializer
Gerencia a serialização e criação de usuários:
- Campos: username, email, password
- Validação de dados de usuário (username e email únicos)
- Criptografia segura de senhas

#### TokenObtainPairSerializer
Serializador personalizado para autenticação:
- Permite login com username ou email
- Gera tokens JWT de acesso e atualização
- Adiciona informações do usuário ao payload do token

### Controladores (controllers/accounts_controller.py)

#### RegisterView
Gerencia o registro de novos usuários:
- Cria novos usuários no sistema
- Valida dados de entrada
- Retorna informações do usuário criado

#### CustomTokenObtainPairView
Gerencia a autenticação de usuários:
- Valida credenciais de usuário
- Gera tokens JWT
- Suporta login com username ou email

#### TokenRefreshView
Gerencia a atualização de tokens:
- Valida tokens de atualização
- Gera novos tokens de acesso
- Estende a sessão do usuário

### Rotas (routes/accounts_routes.py)

Configura os endpoints da API para autenticação:
- `POST /api/v1/accounts/register/`: Registra um novo usuário
- `POST /api/v1/accounts/login/`: Autentica um usuário e retorna tokens
- `POST /api/v1/accounts/login/refresh/`: Atualiza um token de acesso expirado

## Fluxo de Autenticação

1. **Registro**: O usuário se registra fornecendo username, email e senha
2. **Login**: O usuário faz login com username/email e senha, recebendo tokens JWT
3. **Uso da API**: O token de acesso é incluído no cabeçalho de autorização das requisições
4. **Atualização de Token**: Quando o token de acesso expira, o token de atualização é usado para obter um novo

## Segurança

- **Senhas**: Armazenadas com hash seguro usando o sistema do Django
- **Tokens JWT**: Configurados com tempos de expiração apropriados
  - Token de acesso: 15 minutos
  - Token de atualização: 1 dia
- **Validação**: Verificação rigorosa de credenciais e dados de usuário
- **Emails Únicos**: Validação para garantir que cada email seja usado apenas uma vez

## Funcionalidades

- **Registro de Usuários**: Criação de novas contas
- **Autenticação Flexível**: Login com username ou email
- **Atualização de Tokens**: Extensão segura de sessões

## Testes

O app inclui testes abrangentes para todos os componentes:
- Testes de serializador: Verificam a serialização/deserialização e validação
- Testes de controlador: Testam os endpoints de registro e autenticação

### Executando os Testes
```bash
# Executar todos os testes do app usando Django test runner
python manage.py test apps.accounts

# Executar testes específicos
python manage.py test apps.accounts.tests.controllers
python manage.py test apps.accounts.tests.schemas

# Executar testes com pytest (caminho direto)
pytest apps/accounts/tests/
pytest apps/accounts/tests/controllers/
pytest apps/accounts/tests/schemas/
```

## Observações sobre os Testes

- **Emails Únicos**: O sistema agora valida a unicidade dos emails durante o registro
- **Credenciais Inválidas**: Ao tentar fazer login com credenciais inválidas, o sistema retorna um erro 400 (Bad Request) em vez de 401 (Unauthorized)
- **Validação de Usuário**: A validação de nome de usuário único funciona corretamente

## Comandos Úteis

### Shell para Depuração
```bash
python manage.py shell

# Exemplo de uso no shell
from django.contrib.auth.models import User
User.objects.create_user(username='testuser', email='test@example.com', password='password123')
```