from django.contrib import admin
from django.urls import path, include
from categories.views import home
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Page d'accueil
    path('', home, name='home'),

    # Routes des comptes utilisateurs
    path('accounts/', include('accounts.urls')),

    # Routes des produits et catégories
    path('', include('categories.urls')),

    # Authentification DRF (API)
    path('api-auth/', include('rest_framework.urls')),

    # OAuth2 endpoints
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
