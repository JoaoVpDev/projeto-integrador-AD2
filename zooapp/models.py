from django.db import models


class Item(models.Model):
    nome = models.CharField(max_length=100)
    especime = models.CharField(max_length=100, default="desconhecido")
    data_coleta = models.DateField(default="2025-01-01")

    def __str__(self):
        return self.nome
