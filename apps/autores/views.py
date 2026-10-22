"""
Views de Autor usando APIView.

APIView é a CBV mais "crua" do DRF: você escreve um método pra cada verbo HTTP
(get, post, put, patch, delete) e faz tudo na mão. É ótima pra entender o que
as generics e os ViewSets (usados no app "livros") fazem por baixo dos panos.
"""
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.livros.serializers import LivroListSerializer

from .models import Autor
from .serializers import AutorSerializer


class AutorListCreateView(APIView):
    """
    GET  /api/autores/  -> lista todos os autores
    POST /api/autores/  -> cria um autor
    """

    def get(self, request):
        nacionalidade = request.query_params.get('nacionalidade')

        if nacionalidade:
            autores = Autor.objects.filter(nacionalidade__iexact=nacionalidade)

        else:
            autores = Autor.objects.all()

        serializer = AutorSerializer(autores, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AutorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # se inválido, retorna 400 automaticamente
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AutorDetailView(APIView):
    """
    GET    /api/autores/<id>/  -> detalhe
    PUT    /api/autores/<id>/  -> atualização completa
    PATCH  /api/autores/<id>/  -> atualização parcial
    DELETE /api/autores/<id>/  -> remove
    """

    def get_object(self, pk):
        return get_object_or_404(Autor, pk=pk)  # 404 se não existir

    def get(self, request, pk):
        autor = self.get_object(pk)
        serializer = AutorSerializer(autor)
        return Response(serializer.data)

    def put(self, request, pk):
        autor = self.get_object(pk)
        serializer = AutorSerializer(autor, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        autor = self.get_object(pk)
        serializer = AutorSerializer(autor, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        autor = self.get_object(pk)
        try:
            autor.delete()
        except ProtectedError:
            # Livro.autor usa on_delete=PROTECT: não deixa apagar autor com livros
            return Response(
                {'detail': 'Não é possível excluir um autor que possui livros cadastrados.'},
                status=status.HTTP_409_CONFLICT,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class AutorLivrosView(APIView):
    """
    GET /api/autores/<id>/livros/  -> livros de um autor (rota "aninhada")
    """

    def get(self, request, pk):
        autor = get_object_or_404(Autor, pk=pk)
        livros = autor.livros.select_related('autor', 'categoria')
        serializer = LivroListSerializer(livros, many=True)
        return Response(serializer.data)
