from django.db import models
from django.contrib.auth.models import User

PRIORIDADES = [
    ("B", "Baixa"),
    ("M", "Media"),
    ("A", "Alta")
]

STATUS = [
    ("P", "Pendente"),
    ("EA", "Em Andamento"),
    ("C", "Concluída")
]

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
        verbose_name = 'Tarefa' # nome da tabela no banco
        verbose_name_plural = 'Tarefas'

    def __str__(self):
        return self.titulo # Exibe o campo titulo