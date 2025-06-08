from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .serializers import ProduitSerializer, AvisSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Boisson, Cafe, Viennoiserie ,Produit,  Avis, Panier


# ----------------------------------------
# Vues HTML classiques
# ----------------------------------------
def home(request):
    # Récupérer quelques produits pour la page d'accueil
    boissons = Boisson.objects.all()[:3]
    cafes = Cafe.objects.all()[:3]
    viennoiseries = Viennoiserie.objects.all()[:3]

    # Combiner tous les produits
    produits = list(boissons) + list(cafes) + list(viennoiseries)

    context = {
        'produits': produits,
        'total_produits': Produit.objects.count(),
        'total_clients': 1000,  # Exemple
        'moyenne_avis': 4.8,    # Exemple
    }
    return render(request, 'home.html', context)

    
# Vues de connexion supprimées - maintenant gérées par accounts/views.py


def liste_produits(request):
    boissons = Boisson.objects.all()
    cafes = Cafe.objects.all()
    viennoiseries = Viennoiserie.objects.all()

    # Combiner tous les produits
    produits = list(boissons) + list(cafes) + list(viennoiseries)
    produits.sort(key=lambda p: p.nom.lower())

    # Filtrage par catégorie si demandé
    categorie = request.GET.get('categorie')
    if categorie == 'boisson':
        produits = list(boissons)
    elif categorie == 'cafe':
        produits = list(cafes)
    elif categorie == 'viennoiserie':
        produits = list(viennoiseries)

    context = {
        'produits': produits,
        'boissons': boissons,
        'cafes': cafes,
        'viennoiseries': viennoiseries,
        'categorie_active': categorie,
        'total_produits': len(produits)
    }

    return render(request, 'categories/liste_produits.html', context)

def detail_produit(request, produit_id):
   # Récupère le produit de base
    produit = get_object_or_404(Produit, id=produit_id)

    # Détermine dynamiquement le détail selon le sous-type
    if hasattr(produit, 'boisson'):
        # Multi-table inheritance : produit.boisson renvoie l'instance Boisson
        detail = produit.boisson.get_info()
    elif hasattr(produit, 'cafe'):
        detail = produit.cafe.get_details()
    elif hasattr(produit, 'viennoiserie'):
        detail = produit.viennoiserie.get_details()
    else:
        detail = f"{produit.nom} — {produit.prix} DT"

    return render(request, 'templates/cafe/detail_produit.html', {
        'produit': produit,
        'detail': detail
    })

@login_required
def poster_avis(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.method == 'POST':
        note = request.POST.get('note')
        commentaire = request.POST.get('commentaire')
        Avis.objects.create(
            produit=produit,
            utilisateur=request.user,
            note=note,
            commentaire=commentaire
        )
        return redirect('detail_produit', produit_id=produit.id)
    return render(request, 'templates/cafe/poster_avis.html', {
        'produit': produit
    })

@login_required
def ajouter_au_panier(request, produit_id):
    from django.contrib import messages
    from django.http import JsonResponse

    produit = get_object_or_404(Produit, id=produit_id)

    # Vérifier le stock
    if produit.stock <= 0:
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': False, 'message': 'Produit en rupture de stock'})
        messages.error(request, f"❌ {produit.nom} est en rupture de stock")
        return redirect('liste_produits')

    panier_item, created = Panier.objects.get_or_create(
        utilisateur=request.user,
        produit=produit,
        defaults={'quantite': 1}
    )

    if not created:
        # Vérifier si on peut ajouter une unité de plus
        if panier_item.quantite >= produit.stock:
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({'success': False, 'message': 'Stock insuffisant'})
            messages.error(request, f"❌ Stock insuffisant pour {produit.nom}")
            return redirect('liste_produits')

        panier_item.quantite += 1
        panier_item.save()
        message = f"✅ Quantité de {produit.nom} mise à jour dans le panier"
    else:
        message = f"✅ {produit.nom} ajouté au panier"

    # Réponse selon le type de requête
    if request.headers.get('Content-Type') == 'application/json':
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_count': Panier.objects.filter(utilisateur=request.user).count()
        })

    messages.success(request, message)
    return redirect('liste_produits')

# ----------------------------------------
# API REST (JSON)
# ----------------------------------------

@api_view(['GET'])
def api_liste_produits(request):
    produits = Produit.objects.all()
    categorie_id = request.GET.get('categorie')
    if categorie_id:
        produits = produits.filter(categorie_id=categorie_id)
    serializer = ProduitSerializer(produits, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_detail_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    serializer = ProduitSerializer(produit)
    return Response(serializer.data)

@api_view(['GET'])
def api_liste_avis_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    avis = Avis.objects.filter(produit=produit)
    serializer = AvisSerializer(avis, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_poster_avis(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    data = request.data.copy()
    data['utilisateur'] = request.user.id
    data['produit'] = produit.id
    serializer = AvisSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_ajouter_au_panier(request):
    produit_id = request.data.get('produit_id')
    if not produit_id:
        return Response({'error': 'Produit ID requis'}, status=400)
    produit = get_object_or_404(Produit, id=produit_id)
    panier_item, created = Panier.objects.get_or_create(
        utilisateur=request.user,
        produit=produit,
        defaults={'quantite': 1}
    )
    if not created:
        panier_item.quantite += 1
        panier_item.save()
    return Response({'message': 'Produit ajouté au panier'})
