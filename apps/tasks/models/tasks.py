from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Usuário", db_index=True)
    titulo = models.CharField(max_length=160, verbose_name="Titulo")
    descricao = models.TextField(verbose_name="Descrição", blank=True)
    prioridade = models.CharField(
        choices=PRIORIDADES, verbose_name="Prioridade", max_length=1)
    prazo = models.DateField(verbose_name="Prazo", null=True, blank=True)
    status = models.CharField(
        choices=STATUS, default="P", verbose_name="Status", max_length=2)
    criado_em = models.DateTimeField(
        auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(
        auto_now=True, verbose_name="Atualizado em")
    concluido_em = models.DateTimeField(
        null=True, blank=True, verbose_name="Concluído em")
        

    def concluir(self):
        if self.status != "C":
            self.status = "C"
            self.concluido_em = timezone.now()
            self.save()

    class Meta:
        ordering = ['id']
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
        indexes = [
            models.Index(fields=['usuario', 'status']),
            models.Index(fields=['prazo']),
        ]

    def __str__(self):
        return self.titulo
