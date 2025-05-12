# Modelos de Dados

Este documento descreve os modelos de dados utilizados na API Task Collab.

## Visão Geral

A API Task Collab utiliza os seguintes modelos principais:

1. **User** - Modelo padrão de usuário do Django
2. **Tasks** - Modelo para representar tarefas

## User

O modelo de usuário é o modelo padrão fornecido pelo Django (`django.contrib.auth.models.User`).

### Campos Principais

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Identificador único do usuário |
| username | String | Nome de usuário único |
| email | String | Endereço de e-mail (opcional) |
| password | String | Senha criptografada |
| is_active | Boolean | Indica se o usuário está ativo |
| date_joined | DateTime | Data e hora de criação da conta |

### Relacionamentos

- Um usuário pode ter várias tarefas (relação um-para-muitos com Tasks)

## Tasks

O modelo Tasks representa as tarefas dos usuários no sistema.

### Definição do Modelo

```python
class Tasks(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    titulo = models.CharField(null=True, max_length=160, verbose_name="Titulo")
    descricao = models.TextField(verbose_name="Descrição", blank=True)
    prioridade = models.CharField(choices=PRIORIDADES, verbose_name="Prioridade")
    prazo = models.DateField(verbose_name="Prazo", null=True)
    status = models.CharField(choices=STATUS, default="P", verbose_name="Status", max_length=2)
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    def get_status(self):
        match self.status:
            case "P":
                return "Pendente"
            case "EA":
                return "Em Andamento"
            case "C":
                return "Concluída"
            case _:
                return "Status desconhecido"

    class Meta:
        ordering = ['id']
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'

    def __str__(self):
        return self.titulo
```

### Campos

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Identificador único da tarefa (gerado automaticamente) |
| usuario | ForeignKey | Referência ao usuário proprietário da tarefa |
| titulo | CharField | Título da tarefa (máximo 160 caracteres) |
| descricao | TextField | Descrição detalhada da tarefa (opcional) |
| prioridade | CharField | Prioridade da tarefa (A: Alta, M: Média, B: Baixa) |
| prazo | DateField | Data limite para conclusão da tarefa (opcional) |
| status | CharField | Status atual da tarefa (P: Pendente, EA: Em Andamento, C: Concluída) |
| criado_em | DateTimeField | Data e hora de criação da tarefa (preenchido automaticamente) |

### Opções de Prioridade

```python
PRIORIDADES = [
    ("B", "Baixa"),
    ("M", "Media"),
    ("A", "Alta")
]
```

### Opções de Status

```python
STATUS = [
    ("P", "Pendente"),
    ("EA", "Em Andamento"),
    ("C", "Concluída")
]
```

### Métodos

#### get_status()

Retorna a representação legível do status da tarefa.

**Retorno:** String representando o status atual da tarefa.

### Meta Opções

- **ordering**: Tarefas são ordenadas por ID por padrão
- **verbose_name**: 'Tarefa'
- **verbose_name_plural**: 'Tarefas'

## Serializers

Os serializers são responsáveis por converter os modelos em representações JSON e vice-versa.

### TaskSerializer

```python
class TaskSerializer(serializers.ModelSerializer):
    usuario = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        write_only=True
    )

    def validate_usuario(self, value):
        try:
            user = User.objects.get(username=value)
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuário não existe")

    class Meta:
        model = Tasks
        fields = '__all__'
```

#### Campos Personalizados

- **usuario**: Campo personalizado que aceita o nome de usuário (username) em vez do ID do usuário

#### Validação

- Verifica se o usuário especificado existe no sistema

## Diagrama de Relacionamento

```
+---------------+       +---------------+
|     User      |       |     Tasks     |
+---------------+       +---------------+
| id            |       | id            |
| username      |       | usuario (FK)  |
| email         |       | titulo        |
| password      |       | descricao     |
| is_active     |       | prioridade    |
| date_joined   |       | prazo         |
+---------------+       | status        |
        |               | criado_em     |
        +---------------+---------------+
                        |
                        v
                 Um usuário pode ter
                 várias tarefas
```

## Próximos Passos

Para entender como interagir com esses modelos através da API, consulte a documentação dos [Endpoints](./endpoints.md).