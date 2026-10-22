"""
Popula o banco com dados de exemplo.

Uso:
    python manage.py popular_banco
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.autores.models import Autor
from apps.livros.models import Categoria, Livro

AUTORES = [
    {'nome': 'Machado de Assis', 'email': 'machado@exemplo.com', 'nacionalidade': 'Brasileira', 'data_nascimento': '1839-06-21'},
    {'nome': 'Clarice Lispector', 'email': 'clarice@exemplo.com', 'nacionalidade': 'Brasileira', 'data_nascimento': '1920-12-10'},
    {'nome': 'George Orwell', 'email': 'orwell@exemplo.com', 'nacionalidade': 'Britânica', 'data_nascimento': '1903-06-25'},
    {'nome': 'J. R. R. Tolkien', 'email': 'tolkien@exemplo.com', 'nacionalidade': 'Britânica', 'data_nascimento': '1892-01-03'},
]

CATEGORIAS = ['Romance', 'Ficção Científica', 'Fantasia', 'Clássico']

LIVROS = [
    ('Dom Casmurro', '9788535910663', 1899, 256, '29.90', 'Machado de Assis', 'Clássico'),
    ('Memórias Póstumas de Brás Cubas', '9788535911664', 1881, 208, '34.90', 'Machado de Assis', 'Clássico'),
    ('A Hora da Estrela', '9788532508120', 1977, 88, '39.90', 'Clarice Lispector', 'Romance'),
    ('1984', '9788535914849', 1949, 416, '49.90', 'George Orwell', 'Ficção Científica'),
    ('A Revolução dos Bichos', '9788535909555', 1945, 152, '27.90', 'George Orwell', 'Ficção Científica'),
    ('O Hobbit', '9788595084742', 1937, 336, '54.90', 'J. R. R. Tolkien', 'Fantasia'),
    ('O Senhor dos Anéis', '9788533613379', 1954, 1216, '149.90', 'J. R. R. Tolkien', 'Fantasia'),
]


class Command(BaseCommand):
    help = 'Cria autores, categorias, livros e um usuário admin (admin/admin123) para o /admin/.'

    def handle(self, *args, **options):
        autores = {}
        for dados in AUTORES:
            autor, _ = Autor.objects.get_or_create(email=dados['email'], defaults=dados)
            autores[autor.nome] = autor

        categorias = {}
        for nome in CATEGORIAS:
            categoria, _ = Categoria.objects.get_or_create(nome=nome)
            categorias[nome] = categoria

        for titulo, isbn, ano, paginas, preco, autor, categoria in LIVROS:
            Livro.objects.get_or_create(
                isbn=isbn,
                defaults={
                    'titulo': titulo,
                    'ano_publicacao': ano,
                    'paginas': paginas,
                    'preco': Decimal(preco),
                    'autor': autores[autor],
                    'categoria': categorias[categoria],
                },
            )

        User = get_user_model()
        user, criado = User.objects.get_or_create(
            username='admin', defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@exemplo.com'}
        )
        if criado:
            user.set_password('admin123')
            user.save()

        self.stdout.write(self.style.SUCCESS('Banco populado!'))
        self.stdout.write(f'  Autores: {Autor.objects.count()}')
        self.stdout.write(f'  Categorias: {Categoria.objects.count()}')
        self.stdout.write(f'  Livros: {Livro.objects.count()}')
        self.stdout.write('  Usuário do /admin/: admin / admin123')
