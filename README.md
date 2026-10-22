# Biblioteca API — Django + Django REST Framework

Projeto de estudo: uma API de biblioteca com **autores**, **categorias** e **livros**.

## Como rodar

```powershell
# 1. Ativar o ambiente virtual (o venv já está criado)
.\venv\Scripts\Activate.ps1

# (se for uma máquina nova: python -m venv venv  e depois  pip install -r requirements.txt)

# 2. Criar as tabelas
python manage.py migrate

# 3. Popular o banco com dados de exemplo + usuário admin
python manage.py popular_banco

# 4. Subir o servidor
python manage.py runserver
```

- API: http://127.0.0.1:8000/api/
- Admin: http://127.0.0.1:8000/admin/ (usuário `admin` / senha `admin123`)
- Testes: `python manage.py test`

> Se o PowerShell bloquear o `Activate.ps1`, rode uma vez:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## Postman

Importe o arquivo `postman/Biblioteca API.postman_collection.json` e saia batendo.

A API é **aberta**: não tem login nem token, qualquer método funciona direto.

Dica: abrir as URLs no navegador também funciona (API navegável do DRF).

## Estrutura

```
config/                 # configuração do projeto
├── settings.py         # INSTALLED_APPS separado em DJANGO / THIRD_PARTY / LOCAL + config do DRF
└── urls.py             # URLs raiz: só faz include() das urls de cada app

apps/
├── autores/            # CBV nível 1: APIView (tudo na mão)
│   ├── models.py       # Autor
│   ├── serializers.py  # ModelSerializer + SerializerMethodField + validate_<campo>
│   ├── views.py        # APIView com get/post/put/patch/delete
│   ├── urls.py         # rotas escritas com path()
│   ├── admin.py
│   └── tests.py
│
└── livros/             # CBV níveis 2 e 3: Generic Views e ViewSet
    ├── models.py       # Categoria, Livro (ForeignKey para Autor e Categoria)
    ├── serializers.py  # serializer de lista x detalhe, aninhado, autor_id/categoria_id, validate()
    ├── views.py        # Categoria = generics | Livro = ModelViewSet + @action
    ├── urls.py         # path() para categorias + DefaultRouter para livros
    ├── admin.py
    ├── tests.py
    └── management/commands/popular_banco.py
```

## Endpoints

| Método | URL | View | O que faz |
|---|---|---|---|
| GET, POST | `/api/autores/` | APIView | lista (`?nacionalidade=`) / cria |
| GET, PUT, PATCH, DELETE | `/api/autores/<id>/` | APIView | detalhe / edita / apaga (409 se tiver livros) |
| GET | `/api/autores/<id>/livros/` | APIView | livros de um autor |
| GET, POST | `/api/categorias/` | ListCreateAPIView | lista (`?search=`) / cria |
| GET, PUT, PATCH, DELETE | `/api/categorias/<id>/` | RetrieveUpdateDestroyAPIView | detalhe / edita / apaga |
| GET, POST | `/api/livros/` | ModelViewSet | lista paginada / cria |
| GET, PUT, PATCH, DELETE | `/api/livros/<id>/` | ModelViewSet | detalhe / edita / apaga |
| GET | `/api/livros/estatisticas/` | `@action(detail=False)` | totais |
| POST | `/api/livros/<id>/alternar-disponibilidade/` | `@action(detail=True)` | liga/desliga `disponivel` |

Filtros de livros: `?search=orwell`, `?ordering=-preco`, `?disponivel=true`, `?categoria=1`, `?autor=1`, `?page=2`.

Exemplo de body para criar livro (repare que na **escrita** vai `autor_id`, e na **leitura** volta o objeto `autor` completo):

```json
{
  "titulo": "Quincas Borba",
  "isbn": "9788508133059",
  "ano_publicacao": 1891,
  "paginas": 312,
  "preco": "32.50",
  "autor_id": 1,
  "categoria_id": 1
}
```

## Roteiro de aula sugerido

1. **Projeto x App** — `config/` vs `apps/`, `INSTALLED_APPS`, `manage.py`.
2. **Models** — `apps/autores/models.py` e `apps/livros/models.py`: campos, `Meta`, `__str__`, `ForeignKey`, `related_name`, `on_delete` (PROTECT x SET_NULL).
3. **Migrations** — `makemigrations` / `migrate`; abrir o arquivo em `migrations/`.
4. **Admin** — `admin.py`, entrar em `/admin/`.
5. **Serializers** — Model ↔ JSON, `read_only` / `write_only`, `source=`, serializer aninhado, `validate_<campo>` e `validate()`.
6. **Views (a evolução dos CBVs)**
   - `autores/views.py` → **APIView**: escrevemos cada verbo na mão.
   - `livros/views.py` (categorias) → **Generic Views**: o mesmo CRUD em ~4 linhas.
   - `livros/views.py` (livros) → **ModelViewSet**: uma classe só, + `get_queryset`, `get_serializer_class`, `@action`.
7. **URLs** — `include()`, `app_name`, `path()` manual x `DefaultRouter`.
8. **Config do DRF** — permissões, paginação, search/ordering (`REST_FRAMEWORK` no settings).
9. **Testes** — `APITestCase` em `tests.py`.

### Exercícios para o aluno

- Adicionar um campo `sinopse` em `Livro` (model → migration → serializer).
- Reescrever `autores/views.py` usando generics e depois um `ModelViewSet`.
- Criar um app `emprestimos` (Emprestimo: livro, nome do leitor, data, devolvido).
- Criar uma `@action` `GET /api/livros/mais-caros/` retornando os 3 livros mais caros.
- Fazer `GET /api/autores/` ter paginação (dica: na APIView isso é manual; nas generics é automático).
