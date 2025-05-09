# Tasks App

Este é um app do projeto tasks.

## Estrutura do App
```
tasks/
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
python manage.py makemigrations tasks
python manage.py migrate
```

### Testes
```bash
python manage.py test apps.tasks
python manage.py test apps.tasks.tests.controllers
```
