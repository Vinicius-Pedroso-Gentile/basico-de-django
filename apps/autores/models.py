from django.db import models


class Autor(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    nacionalidade = models.CharField(max_length=100, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    biografia = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'autor'
        verbose_name_plural = 'autores'
        ordering = ['nome']

    def __str__(self):
        return self.nome
