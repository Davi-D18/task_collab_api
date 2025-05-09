# Accounts App

Este é um app do projeto accounts.

## Estrutura do App
```
accounts/
├── controllers/     # Views e ViewSets
├── models/          # Modelos do Django
├── schemas/         # Schemas para validação
├── services/        # Lógica de negócio
├── repository/      # Camada de acesso a dados
├── routes/          # URLs e ViewSets
└── tests/           # Testes unitários
```

## Comandos Úteis

### Migrações
```bash
python manage.py makemigrations accounts
python manage.py migrate
```

### Testes
```bash
python manage.py test apps.accounts
python manage.py test apps.accounts.tests.controllers
```
