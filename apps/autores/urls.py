from django.urls import path

from . import views

app_name = 'autores'

urlpatterns = [
    path('autores/', views.AutorListCreateView.as_view(), name='lista'),
    path('autores/<int:pk>/', views.AutorDetailView.as_view(), name='detalhe'),
    path('autores/<int:pk>/livros/', views.AutorLivrosView.as_view(), name='livros'),
]
