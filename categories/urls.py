from django.urls import path
from . import views

urlpatterns = [
    # HTML Views
    path('produits/', views.liste_produits, name='liste_produits'),
    path('produit/<int:produit_id>/', views.detail_produit, name='detail_produit'),
    path('produit/<int:produit_id>/avis/', views.poster_avis, name='poster_avis'),
    path('ajouter-au-panier/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),

    # API Views
    path('api/produits/', views.api_liste_produits, name='api_liste_produits'),
    path('api/produits/<int:produit_id>/', views.api_detail_produit, name='api_detail_produit'),
    path('api/produits/<int:produit_id>/avis/', views.api_liste_avis_produit, name='api_liste_avis_produit'),
    path('api/produit/<int:produit_id>/avis/', views.api_poster_avis, name='api_poster_avis'),
    path('api/panier/ajouter/', views.api_ajouter_au_panier, name='api_ajouter_au_panier'),
]
