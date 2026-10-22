from rest_framework import serializers

from .models import Autor


class AutorSerializer(serializers.ModelSerializer):
    """
    ModelSerializer: gera os campos automaticamente a partir do model.
    Ele converte Model -> JSON (saída) e JSON -> Model (entrada, com validação).
    """

    # Campo calculado: não existe no model, é montado pelo método get_total_livros
    total_livros = serializers.SerializerMethodField()

    class Meta:
        model = Autor
        fields = [
            'id',
            'nome',
            'email',
            'nacionalidade',
            'data_nascimento',
            'biografia',
            'total_livros',
            'criado_em',
            'atualizado_em',
        ]
        read_only_fields = ['criado_em', 'atualizado_em']

    def get_total_livros(self, obj):
        return obj.livros.count()

    def validate_nome(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError('O nome precisa ter pelo menos 3 caracteres.')
        return value.strip()
