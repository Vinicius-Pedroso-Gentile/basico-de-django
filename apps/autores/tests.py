from rest_framework import status
from rest_framework.test import APITestCase

from .models import Autor


class AutorAPITest(APITestCase):
    def setUp(self):
        self.autor = Autor.objects.create(nome='Machado de Assis', email='machado@exemplo.com')

    def test_listar(self):
        response = self.client.get('/api/autores/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_criar(self):
        response = self.client.post('/api/autores/', {'nome': 'Clarice', 'email': 'c@x.com'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Autor.objects.count(), 2)

    def test_nome_curto_invalido(self):
        response = self.client.post('/api/autores/', {'nome': 'AB', 'email': 'ab@x.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nome', response.data)

    def test_excluir_autor_com_livros_retorna_409(self):
        from apps.livros.models import Livro

        Livro.objects.create(
            titulo='Dom Casmurro', isbn='9788535910663', ano_publicacao=1899,
            paginas=256, preco='29.90', autor=self.autor,
        )
        response = self.client.delete(f'/api/autores/{self.autor.id}/')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_detalhe_inexistente_retorna_404(self):
        response = self.client.get('/api/autores/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
