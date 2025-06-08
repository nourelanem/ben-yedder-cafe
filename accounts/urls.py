from django.urls import path
from .views import (
    login_view, register_view, logout_view, profile_view, dashboard,
    panier_view, update_panier_quantity, remove_panier_item
)
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Authentification
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # Profil et dashboard
    path('profile/', views.profile_view, name='profile'),
    path('', views.dashboard, name='accounts_dashboard'),

    # Panier
    path('panier/', panier_view, name='panier'),
    path('panier/update/<int:item_id>/', update_panier_quantity, name='update_panier_quantity'),
    path('panier/remove/<int:item_id>/', remove_panier_item, name='remove_panier_item'),

    # Réinitialisation mot de passe
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
