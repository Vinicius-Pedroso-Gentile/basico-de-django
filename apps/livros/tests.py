from rest_framework import status
from rest_framework.test import APITestCase

from apps.autores.models import Autor

from .models import Categoria, Livro


class LivroAPITest(APITestCase):
    def setUp(self):
        self.autor = Autor.objects.create(nome='George Orwell', email='orwell@exemplo.com')
        self.categoria = Categoria.objects.create(nome='Ficção Científica')
        self.livro = Livro.objects.create(
            titulo='1984',
            isbn='9788535914849',
            ano_publicacao=1949,
            paginas=416,
            preco='49.90',
            autor=self.autor,
            categoria=self.categoria,
        )

    def test_listar_paginado(self):
        response = self.client.get('/api/livros/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['autor'], 'George Orwell')

    def test_detalhe_traz_autor_aninhado(self):
        response = self.client.get(f'/api/livros/{self.livro.id}/')
        self.assertEqual(response.data['autor']['nome'], 'George Orwell')

    def test_criar_livro(self):
        payload = {
            'titulo': 'A Revolução dos Bichos',
            'isbn': '9788535909555',
            'ano_publicacao': 1945,
            'paginas': 152,
            'preco': '27.90',
            'autor_id': self.autor.id,
            'categoria_id': self.categoria.id,
        }
        response = self.client.post('/api/livros/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['autor']['id'], self.autor.id)

    def test_isbn_invalido(self):
        response = self.client.patch(f'/api/livros/{self.livro.id}/', {'isbn': 'abc'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_busca(self):
        response = self.client.get('/api/livros/?search=orwell')
        self.assertEqual(response.data['count'], 1)

    def test_alternar_disponibilidade(self):
        response = self.client.post(f'/api/livros/{self.livro.id}/alternar-disponibilidade/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['disponivel'])

    def test_estatisticas(self):
        response = self.client.get('/api/livros/estatisticas/')
        self.assertEqual(response.data, {'total': 1, 'disponiveis': 1, 'indisponiveis': 0})
