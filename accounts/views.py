from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .decorators import admin_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Client


def register_view(request):
    """Vue d'inscription pour les clients"""
    if request.method == 'POST':
        # Récupérer les données du formulaire
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        adresse = request.POST.get('adresse', '')
        telephone = request.POST.get('telephone', '')

        # Validation avancée
        errors = []

        if not username:
            errors.append("Le nom d'utilisateur est requis.")
        elif User.objects.filter(username=username).exists():
            errors.append("Ce nom d'utilisateur est déjà utilisé.")

        if not email:
            errors.append("L'email est requis.")
        elif User.objects.filter(email=email).exists():
            errors.append("Cet email est déjà utilisé.")

        if not password1:
            errors.append("Le mot de passe est requis.")
        elif len(password1) < 6:
            errors.append("Le mot de passe doit contenir au moins 6 caractères.")

        if password1 != password2:
            errors.append("Les mots de passe ne correspondent pas.")

        # Vérifier uniquement l'email (les noms peuvent être en doublon)
        # Le téléphone peut aussi être en doublon (plusieurs personnes peuvent partager un numéro)

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'accounts/register.html', {
                'form_data': request.POST
            })

        try:
            # Créer l'utilisateur (client normal, pas staff)
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                is_staff=False,  # Pas d'accès admin
                is_superuser=False  # Pas de droits superutilisateur
            )

            # Créer le profil client
            Client.objects.create(
                utilisateur=user,
                adresse=adresse,
                telephone=telephone
            )

            messages.success(request, "🎉 Inscription réussie ! Vous êtes maintenant connecté.")
            # Connecter automatiquement l'utilisateur après inscription
            login(request, user)
            return redirect('home')  # Redirection vers la page d'accueil

        except Exception as e:
            messages.error(request, f"Erreur lors de l'inscription : {str(e)}")
            return render(request, 'accounts/register.html', {
                'form_data': request.POST
            })

    return render(request, 'accounts/register.html')


def login_view(request):
    """Vue de connexion pour les utilisateurs"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        if not username or not password:
            messages.error(request, "❌ Veuillez remplir tous les champs.")
            return render(request, 'accounts/login.html')

        # Authentification
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)

            # Gestion du "Se souvenir de moi"
            if not remember_me:
                request.session.set_expiry(0)  # Session expire à la fermeture du navigateur
            else:
                request.session.set_expiry(1209600)  # 2 semaines

            messages.success(request, f"🎉 Bienvenue {user.first_name or user.username} !")

            # Redirection selon le type d'utilisateur
            if user.is_superuser:
                # Seuls les superutilisateurs peuvent accéder à l'admin
                return redirect('/admin/')
            else:
                # Tous les autres utilisateurs (clients) vont à l'accueil
                return redirect('home')
        else:
            messages.error(request, "❌ Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'accounts/login.html')


def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    messages.success(request, "👋 Vous avez été déconnecté avec succès.")
    return redirect('login')


@login_required
def dashboard(request):
    """Tableau de bord utilisateur"""
    return render(request, 'accounts/dashboard.html', {
        'user': request.user
    })


@login_required
def profile_view(request):
    """Vue du profil utilisateur"""
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })


@admin_required
def admin_profile_view(request):
    """Vue du profil admin"""
    return render(request, 'accounts/admin_profile.html')


@login_required
def panier_view(request):
    """Vue du panier"""
    from categories.models import Panier

    # Récupérer les articles du panier de l'utilisateur connecté
    panier_items = Panier.objects.filter(utilisateur=request.user).select_related('produit')

    # Calculer les totaux
    from decimal import Decimal
    subtotal = sum(item.quantite * item.produit.prix for item in panier_items)
    shipping_cost = Decimal('5.00') if subtotal > 0 and subtotal < 50 else Decimal('0')  # Livraison gratuite > 50 DT
    total = subtotal + shipping_cost

    # Ajouter une propriété total_price à chaque item
    for item in panier_items:
        item.total_price = item.quantite * item.produit.prix

    context = {
        'panier_items': panier_items,
        'total_items': sum(item.quantite for item in panier_items),
        'subtotal': subtotal,
        'total': total,
        'shipping_cost': shipping_cost if shipping_cost > 0 else "Gratuit",
    }

    return render(request, 'accounts/panier.html', context)


@login_required
def update_panier_quantity(request, item_id):
    """Mettre à jour la quantité d'un article dans le panier"""
    from django.http import JsonResponse
    from categories.models import Panier
    import json

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))

            panier_item = get_object_or_404(Panier, id=item_id, utilisateur=request.user)

            if quantity <= 0:
                panier_item.delete()
                return JsonResponse({'success': True, 'message': 'Article supprimé du panier'})

            if quantity > panier_item.produit.stock:
                return JsonResponse({'success': False, 'message': 'Stock insuffisant'})

            panier_item.quantite = quantity
            panier_item.save()

            return JsonResponse({'success': True, 'message': 'Quantité mise à jour'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})


@login_required
def remove_panier_item(request, item_id):
    """Supprimer un article du panier"""
    from django.http import JsonResponse
    from categories.models import Panier

    if request.method == 'POST':
        try:
            panier_item = get_object_or_404(Panier, id=item_id, utilisateur=request.user)
            produit_nom = panier_item.produit.nom
            panier_item.delete()

            return JsonResponse({
                'success': True,
                'message': f'{produit_nom} supprimé du panier'
            })

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})
