from django.contrib import admin
from .models import Utilisateur, Produit, Commande, CommandeProduit, Avis, Panier, Boisson, Cafe, Viennoiserie

@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'date_joined')


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'stock')  # Remplacé 'en_stock' par 'stock'
    search_fields = ('stock',)


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'utilisateur', 'date', 'statut')  # Remplacé 'date_commande' par 'date'
    list_filter = ('statut', 'date')                        # Ajouté 'date' comme filtre
    search_fields = ('utilisateur__username',)
    date_hierarchy = 'date'                                 # Corrigé 'date_commande' → 'date'


@admin.register(CommandeProduit)
class CommandeProduitAdmin(admin.ModelAdmin):
    list_display = ('commande', 'produit', 'quantite')
    list_filter = ('produit',)


@admin.register(Avis)
class AvisAdmin(admin.ModelAdmin):
    list_display = ('produit', 'utilisateur', 'note', 'date')
    list_filter = ('note',)
    search_fields = ('produit__nom', 'utilisateur__username')

admin.site.register(Boisson)
admin.site.register(Cafe)
admin.site.register(Viennoiserie)
admin.site.register(Panier)
