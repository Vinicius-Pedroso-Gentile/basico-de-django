from datetime import date

from rest_framework import serializers

from apps.autores.models import Autor

from .models import Categoria, Livro


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao']


class AutorResumoSerializer(serializers.ModelSerializer):
    """Versão enxuta do autor, usada aninhada dentro do livro."""

    class Meta:
        model = Autor
        fields = ['id', 'nome', 'nacionalidade']


class LivroListSerializer(serializers.ModelSerializer):
    """
    Usado na LISTAGEM: poucos campos e dados "achatados".
    source='autor.nome' navega pela FK e pega só o nome.
    """

    autor = serializers.CharField(source='autor.nome', read_only=True)
    categoria = serializers.CharField(source='categoria.nome', read_only=True, default=None)

    class Meta:
        model = Livro
        fields = ['id', 'titulo', 'autor', 'categoria', 'ano_publicacao', 'preco', 'disponivel']


class LivroDetailSerializer(serializers.ModelSerializer):
    """
    Usado no DETALHE / CRIAÇÃO / EDIÇÃO.

    Truque comum: para LER mostramos o objeto aninhado (autor / categoria)
    e para ESCREVER recebemos só o id (autor_id / categoria_id).
    """

    # Leitura (saída)
    autor = AutorResumoSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)

    # Escrita (entrada) — write_only não aparece na resposta
    autor_id = serializers.PrimaryKeyRelatedField(
        queryset=Autor.objects.all(), source='autor', write_only=True
    )
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source='categoria',
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Livro
        fields = [
            'id',
            'titulo',
            'isbn',
            'ano_publicacao',
            'paginas',
            'preco',
            'disponivel',
            'autor',
            'autor_id',
            'categoria',
            'categoria_id',
            'criado_em',
            'atualizado_em',
        ]
        read_only_fields = ['criado_em', 'atualizado_em']

    # Validação de um campo
    def validate_isbn(self, value):
        if not value.isdigit() or len(value) not in (10, 13):
            raise serializers.ValidationError('ISBN deve ter 10 ou 13 dígitos numéricos.')
        return value

    def validate_ano_publicacao(self, value):
        if value > date.today().year:
            raise serializers.ValidationError('O ano de publicação não pode estar no futuro.')
        return value

    # Validação envolvendo mais de um campo
    def validate(self, attrs):
        # No PATCH nem todos os campos chegam, então caímos no valor atual (self.instance)
        preco = attrs.get('preco', getattr(self.instance, 'preco', None))
        disponivel = attrs.get('disponivel', getattr(self.instance, 'disponivel', True))
        if disponivel and preco is not None and preco <= 0:
            raise serializers.ValidationError(
                {'preco': 'Um livro disponível precisa ter preço maior que zero.'}
            )
        return attrs
