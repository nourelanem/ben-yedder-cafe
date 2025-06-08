from django.db import models
from django.conf import settings
from categories.models import Produit


class Client(models.Model):
    utilisateur = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_profile'
    )
    adresse = models.CharField(max_length=255, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.utilisateur.username} - {self.utilisateur.get_full_name() or 'Client'}"

    def se_connecter(self):
        pass  # logique déjà gérée par Django

    def voir_produits(self):
        return Produit.objects.all()

    def passer_commande(self):
        pass  # à implémenter


class Avis(models.Model):
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='avis_utilisateur'
    )
    produit = models.ForeignKey(
        'categories.Produit',
        on_delete=models.CASCADE,
        related_name='avis_produit'
    )
    commentaire = models.TextField()
    note = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avis de {self.utilisateur.username} sur {self.produit.nom}"
