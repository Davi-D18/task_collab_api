# Perguntas Frequentes (FAQ)

## Geral

### O que é a API Task Collab?

A API Task Collab é uma API RESTful para gerenciamento de tarefas pessoais. Ela permite que usuários criem, visualizem, atualizem e excluam tarefas, além de oferecer recursos de filtragem, ordenação e paginação.

### Quais tecnologias são utilizadas?

A API é construída com Django e Django REST Framework, utilizando SQLite para desenvolvimento e MySQL para produção. A autenticação é baseada em JWT (JSON Web Tokens).

### A API é gratuita para uso?

Sim, a API Task Collab é um projeto de código aberto e pode ser usada gratuitamente.

## Autenticação

### Como funciona a autenticação?

A API utiliza autenticação baseada em JWT (JSON Web Tokens). Após o registro, você pode fazer login para obter tokens de acesso e atualização. O token de acesso deve ser incluído no cabeçalho `Authorization` de todas as requisições protegidas.

### Por quanto tempo os tokens são válidos?

O token de acesso é válido por 15 minutos, enquanto o token de atualização é válido por 1 dia. Quando o token de acesso expirar, você pode usar o token de atualização para obter um novo.

### O que fazer se meu token expirar?

Se o token de acesso expirar, você pode usar o endpoint `/api/v1/accounts/login/refresh/` com o token de atualização para obter um novo token de acesso. Se o token de atualização também expirar, você precisará fazer login novamente.

### Como faço logout?

A API utiliza tokens JWT, que são stateless. Para fazer logout, basta descartar os tokens no cliente. O servidor não mantém registro dos tokens ativos.

## Tarefas

### Posso ver tarefas de outros usuários?

Não, a API implementa um sistema de permissões baseado em propriedade. Cada usuário só pode ver, editar e excluir suas próprias tarefas.

### Quais são os valores válidos para prioridade e status?

- **Prioridade**: A (Alta), M (Média), B (Baixa)
- **Status**: P (Pendente), EA (Em Andamento), C (Concluída)

### Como filtrar tarefas por data?

Você pode usar parâmetros de consulta para filtrar tarefas por data. Por exemplo:
- Para tarefas com prazo até uma data específica: `?prazo_ate=2023-05-31`
- Para tarefas com prazo a partir de uma data específica: `?prazo_apos=2023-05-01`

### Existe um limite para o número de tarefas que posso criar?

Não há um limite específico para o número de tarefas que um usuário pode criar. No entanto, as respostas são paginadas por padrão para melhorar o desempenho.

## Erros e Solução de Problemas

### Por que estou recebendo erro 401 Unauthorized?

O erro 401 indica problemas de autenticação. Verifique se:
- Você incluiu o token de acesso no cabeçalho `Authorization`
- O token está no formato correto: `Bearer {token}`
- O token não expirou

### Por que estou recebendo erro 403 Forbidden?

O erro 403 indica problemas de permissão. Isso pode ocorrer se:
- Você está tentando acessar uma tarefa que não pertence a você
- Você está tentando criar uma tarefa para outro usuário

### Por que estou recebendo erro 404 Not Found?

O erro 404 pode ocorrer se:
- O endpoint solicitado não existe
- Você está tentando acessar uma tarefa que não existe
- Você está tentando acessar uma tarefa que pertence a outro usuário (por segurança, a API retorna 404 em vez de 403 neste caso)

### Como posso reportar bugs ou solicitar novas funcionalidades?

Você pode reportar bugs ou solicitar novas funcionalidades abrindo uma issue no repositório do projeto no GitHub.

## Desenvolvimento e Integração

### Posso usar a API em meu próprio aplicativo?

Sim, a API foi projetada para ser facilmente integrada a outros aplicativos. Consulte a seção [Exemplos de Uso](./examples.md) para ver exemplos de integração com diferentes linguagens e frameworks.

### A API suporta CORS?

Sim, a API suporta CORS (Cross-Origin Resource Sharing), permitindo que aplicativos web em diferentes domínios façam requisições para a API.

### Existe uma versão hospedada da API que posso usar?

Atualmente, não há uma versão hospedada oficial da API. Você precisa hospedar sua própria instância.

### Como posso contribuir para o projeto?

Contribuições são bem-vindas! Você pode contribuir de várias formas:
- Reportando bugs
- Sugerindo novas funcionalidades
- Enviando pull requests com melhorias ou correções
- Melhorando a documentação

## Segurança

### A API é segura?

A API implementa várias medidas de segurança:
- Autenticação baseada em JWT
- Permissões baseadas em propriedade
- Validação de dados de entrada
- Proteção contra ataques comuns (CSRF, XSS, etc.)

No entanto, como qualquer sistema, a segurança depende também de como você implementa e configura a API em seu ambiente.

### As senhas são armazenadas de forma segura?

Sim, as senhas são armazenadas de forma segura usando o sistema de hash do Django, que utiliza algoritmos seguros como PBKDF2 com SHA-256.

### A API suporta HTTPS?

A API pode e deve ser configurada para usar HTTPS em ambientes de produção. Isso não é configurado por padrão e depende do seu servidor web e configuração de hospedagem.