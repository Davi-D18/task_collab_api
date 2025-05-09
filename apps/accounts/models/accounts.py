from django.db import models

# Create your models here.


class Accounts(models.Model):
    # adicione aqui os demais campos

    class Meta:
        ordering = ['name']
        verbose_name = '' # nome da tabela no banco

    def __str__(self):
        return self.name # Exibe o campo name
