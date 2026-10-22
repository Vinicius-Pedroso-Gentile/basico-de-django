from django.contrib import admin

from .models import Categoria, Livro


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    search_fields = ['nome']


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'autor', 'categoria', 'ano_publicacao', 'preco', 'disponivel']
    list_filter = ['disponivel', 'categoria']
    search_fields = ['titulo', 'isbn', 'autor__nome']
    list_select_related = ['autor', 'categoria']
