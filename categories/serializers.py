from rest_framework import serializers
from .models import (
    Produit,
    Boisson,
    Cafe,
    Viennoiserie,
    Avis,
    CommandeProduit,
    Commande,
)

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = ['id', 'nom', 'prix']

class BoissonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boisson
        fields = ['id', 'nom', 'prix', 'volume']

class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe
        fields = ['id', 'nom', 'prix', 'composition']

class ViennoiserieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viennoiserie
        fields = ['id', 'nom', 'prix', 'composition']

class AvisSerializer(serializers.ModelSerializer):
    utilisateur = serializers.StringRelatedField(read_only=True)
    produit = serializers.PrimaryKeyRelatedField(read_only=True)
    produit_id = serializers.PrimaryKeyRelatedField(
        queryset=Produit.objects.all(), source='produit', write_only=True
    )

    class Meta:
        model = Avis
        fields = ['id', 'utilisateur', 'produit', 'produit_id', 'note', 'commentaire', 'date']

class CommandeProduitSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer(read_only=True)
    produit_id = serializers.PrimaryKeyRelatedField(
        queryset=Produit.objects.all(), source='produit', write_only=True
    )

    class Meta:
        model = CommandeProduit
        fields = ['id', 'commande', 'produit', 'produit_id', 'quantite']

class CommandeSerializer(serializers.ModelSerializer):
    utilisateur = serializers.StringRelatedField(read_only=True)
    produits = CommandeProduitSerializer(source='commandeproduit_set', many=True, read_only=True)

    class Meta:
        model = Commande
        fields = ['id', 'utilisateur', 'produits', 'emplacement', 'date_commande', 'statut', 'montant']
