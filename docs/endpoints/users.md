# Endpoints de Usuários

Este documento detalha os endpoints relacionados a usuários e autenticação na API Task Collab.

## Registro

Cria um novo usuário no sistema.

```
POST /api/v1/accounts/register/
```

### Parâmetros da Requisição

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| username | string | Sim | Nome de usuário único |
| email | string | Não | Endereço de e-mail |
| password | string | Sim | Senha do usuário |

### Exemplo de Requisição

```json
{
  "username": "novousuario",
  "email": "usuario@exemplo.com",
  "password": "senhasegura123"
}
```

### Resposta de Sucesso

**Código:** 201 Created

```json
{
  "username": "novousuario",
  "email": "usuario@exemplo.com"
}
```

### Respostas de Erro

**Código:** 400 Bad Request

```json
{
  "username": [
    "Um usuário com este nome de usuário já existe."
  ]
}
```

### Notas

- A senha não é retornada na resposta por motivos de segurança
- O campo de e-mail é opcional, mas recomendado para recuperação de conta

## Login

Autentica um usuário e retorna tokens de acesso e atualização.

```
POST /api/v1/accounts/login/
```

### Parâmetros da Requisição

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| username | string | Sim | Nome de usuário |
| password | string | Sim | Senha do usuário |

### Exemplo de Requisição

```json
{
  "username": "novousuario",
  "password": "senhasegura123"
}
```

### Resposta de Sucesso

**Código:** 200 OK

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Respostas de Erro

**Código:** 401 Unauthorized

```json
{
  "detail": "Credenciais inválidas."
}
```

### Notas

- O token de acesso (`access`) tem validade de 15 minutos
- O token de atualização (`refresh`) tem validade de 1 dia
- O token de acesso deve ser incluído no cabeçalho `Authorization` como `Bearer {token}`

## Atualização de Token

Obtém um novo token de acesso usando um token de atualização válido.

```
POST /api/v1/accounts/login/refresh/
```

### Parâmetros da Requisição

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| refresh | string | Sim | Token de atualização válido |

### Exemplo de Requisição

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Resposta de Sucesso

**Código:** 200 OK

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Respostas de Erro

**Código:** 401 Unauthorized

```json
{
  "detail": "Token inválido ou expirado.",
  "code": "token_not_valid"
}
```

### Notas

- Use este endpoint quando o token de acesso expirar
- O token de atualização também tem um prazo de validade (1 dia)
- Se o token de atualização expirar, o usuário precisará fazer login novamente

## Boas Práticas de Segurança

1. **Armazenamento de Tokens**:
   - Armazene tokens em cookies HttpOnly ou em armazenamento seguro
   - Evite armazenar tokens em localStorage ou sessionStorage

2. **Renovação de Tokens**:
   - Implemente renovação automática de tokens antes da expiração
   - Monitore a expiração do token de acesso e atualize-o proativamente

3. **Logout**:
   - Para logout, descarte os tokens no cliente
   - Considere implementar uma lista de tokens revogados no servidor para casos de segurança críticos

## Próximos Passos

Agora que você sabe como autenticar usuários, consulte a [documentação de endpoints de tarefas](./tasks.md) para aprender como gerenciar tarefas.