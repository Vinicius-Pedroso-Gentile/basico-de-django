from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'livros'

# O router gera automaticamente as rotas do ViewSet (lista, detalhe e @actions)
router = DefaultRouter()
router.register('livros', views.LivroViewSet, basename='livro')

urlpatterns = [
    # Generic views: rotas escritas na mão
    path('categorias/', views.CategoriaListCreateView.as_view(), name='categoria-lista'),
    path('categorias/<int:pk>/', views.CategoriaDetailView.as_view(), name='categoria-detalhe'),

    # ViewSet: rotas geradas pelo router
    path('', include(router.urls)),
]
