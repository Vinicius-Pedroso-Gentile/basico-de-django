"""
Aqui mostramos os dois níveis "acima" da APIView (usada no app autores):

1. Generic views (Categoria): cada classe já implementa os verbos HTTP.
   Você só informa queryset + serializer_class.

2. ViewSet (Livro): UMA classe faz o CRUD inteiro e o Router gera as URLs.
"""
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Categoria, Livro
from .serializers import CategoriaSerializer, LivroDetailSerializer, LivroListSerializer


# --------------------------------------------------------------------------
# 1) Generic views
# --------------------------------------------------------------------------
class CategoriaListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/categorias/  -> lista
    POST /api/categorias/  -> cria
    """

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    search_fields = ['nome']  # ?search=ficcao


class CategoriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET / PUT / PATCH / DELETE  /api/categorias/<id>/
    """

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


# --------------------------------------------------------------------------
# 2) ViewSet
# --------------------------------------------------------------------------
class LivroViewSet(viewsets.ModelViewSet):
    """
    O ModelViewSet já entrega:
        list            GET     /api/livros/
        create          POST    /api/livros/
        retrieve        GET     /api/livros/<id>/
        update          PUT     /api/livros/<id>/
        partial_update  PATCH   /api/livros/<id>/
        destroy         DELETE  /api/livros/<id>/
    """

    queryset = Livro.objects.select_related('autor', 'categoria')

    search_fields = ['titulo', 'isbn', 'autor__nome']
    ordering_fields = ['titulo', 'preco', 'ano_publicacao']

    def get_serializer_class(self):
        if self.action == 'list':
            return LivroListSerializer
        return LivroDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        disponivel = self.request.query_params.get('disponivel')
        if disponivel is not None:
            queryset = queryset.filter(disponivel=disponivel.lower() in ('true', '1'))

        categoria = self.request.query_params.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)

        autor = self.request.query_params.get('autor')
        if autor:
            queryset = queryset.filter(autor_id=autor)

        return queryset

    # ---- Rotas extras com @action ----

    # detail=False -> rota na coleção: GET /api/livros/estatisticas/
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        queryset = self.get_queryset()
        return Response(
            {
                'total': queryset.count(),
                'disponiveis': queryset.filter(disponivel=True).count(),
                'indisponiveis': queryset.filter(disponivel=False).count(),
            }
        )

    # detail=True -> rota em um item: POST /api/livros/<id>/alternar-disponibilidade/
    @action(detail=True, methods=['post'], url_path='alternar-disponibilidade')
    def alternar_disponibilidade(self, request, pk=None):
        livro = self.get_object()
        livro.disponivel = not livro.disponivel
        livro.save(update_fields=['disponivel', 'atualizado_em'])
        serializer = LivroDetailSerializer(livro)
        return Response(serializer.data, status=status.HTTP_200_OK)
