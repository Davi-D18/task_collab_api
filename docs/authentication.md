# Autenticação

A API Task Collab utiliza autenticação baseada em JWT (JSON Web Tokens) para proteger seus endpoints. Este documento explica como autenticar-se na API e gerenciar tokens.

## Visão Geral

A autenticação JWT funciona com dois tipos de tokens:

1. **Access Token**: Token de curta duração (15 minutos) usado para autenticar requisições
2. **Refresh Token**: Token de longa duração (1 dia) usado para obter novos access tokens

## Endpoints de Autenticação

### Registro de Usuário

Para criar uma nova conta:

```
POST /api/v1/accounts/register/
```

**Corpo da Requisição:**
```json
{
  "username": "novousuario",
  "email": "usuario@exemplo.com",
  "password": "senhasegura123"
}
```

**Resposta (201 Created):**
```json
{
  "username": "novousuario",
  "email": "usuario@exemplo.com"
}
```

### Login (Obtenção de Tokens)

Para obter tokens de autenticação:

```
POST /api/v1/accounts/login/
```

**Corpo da Requisição:**
```json
{
  "username": "novousuario",
  "password": "senhasegura123"
}
```

**Resposta (200 OK):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Atualização de Token

Quando o access token expirar, use o refresh token para obter um novo:

```
POST /api/v1/accounts/login/refresh/
```

**Corpo da Requisição:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Resposta (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Usando Tokens em Requisições

Para acessar endpoints protegidos, inclua o access token no cabeçalho de autorização:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Exemplo com cURL

```bash
curl -X GET \
  https://api.exemplo.com/api/v1/tasks/ \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
```

## Duração dos Tokens

- **Access Token**: 15 minutos
- **Refresh Token**: 1 dia

Estas configurações podem ser ajustadas no arquivo `core/settings/base.py` através das variáveis `SIMPLE_JWT`.

## Segurança

Algumas recomendações de segurança:

1. **Nunca armazene tokens em localStorage**: Prefira armazenamento seguro como HttpOnly cookies
2. **Renove tokens regularmente**: Implemente renovação automática de tokens antes da expiração
3. **Proteja o refresh token**: Trate-o como uma credencial sensível
4. **Use HTTPS**: Sempre transmita tokens através de conexões seguras

## Erros Comuns

### 401 Unauthorized

Indica problemas de autenticação:
- Token ausente
- Token expirado
- Token inválido

### 403 Forbidden

Indica problemas de permissão:
- Usuário autenticado, mas sem permissão para o recurso solicitado

## Próximos Passos

Agora que você entende como autenticar-se na API, consulte a documentação dos [Endpoints](./endpoints.md) para aprender como usar os recursos disponíveis.