from django.core.validators import MinValueValidator
from django.db import models

from apps.autores.models import Autor


class Categoria(models.Model):
    nome = models.CharField(max_length=80, unique=True)
    descricao = models.TextField(blank=True)

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    ano_publicacao = models.PositiveIntegerField()
    paginas = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    disponivel = models.BooleanField(default=True)

    # ForeignKey = relação N:1 (muitos livros para um autor)
    # related_name permite fazer: autor.livros.all()
    autor = models.ForeignKey(Autor, on_delete=models.PROTECT, related_name='livros')
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='livros',
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'livro'
        verbose_name_plural = 'livros'
        ordering = ['titulo']

    def __str__(self):
        return f'{self.titulo} ({self.autor})'

