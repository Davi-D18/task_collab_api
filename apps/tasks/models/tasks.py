from django.db import models


class Tasks(models.Model):
    titulo = models.CharField(null=True, max_length=160)
    descricao = models.TextField()
    prioridade = models.CharField(choices=([("B", "Baixa"), ("M", "Media"), ("A", "Alta")]))
    prazo = models.DateField()
    status = models.CharField(choices=[("P", "Pendente"), ("EA", "Em Andamento"), ("C", "Concluída")], default="P")

    class Meta:
        ordering = ['id']
        verbose_name = '' # nome da tabela no banco

    def __str__(self):
        return self.titulo # Exibe o campo name