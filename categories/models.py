from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Admin(models.Model):
    utilisateur = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Admin : {self.utilisateur.username}"


class Utilisateur(AbstractUser):
    telephone = models.CharField(max_length=20, blank=True, null=True)

    # On redéfinit les deux ManyToMany pour éviter le clash
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='cafe_user_set',        # <- changed
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='cafe_user_permissions_set',  # <- changed
        help_text=_('Specific permissions for this user.'),
        related_query_name='user'
    )

    def __str__(self):
        return f"{self.username} ({self.email})"



class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
   

    def __str__(self):
        return self.nom

class Boisson(Produit):
    volume = models.PositiveIntegerField()  # en millilitres

    def get_info(self):
        return f"{self.nom} ({self.volume} ml) - {self.prix} DT"

class Cafe(Produit):
    composition = models.CharField(max_length=255)

    def get_details(self):
        return f"Café {self.nom} - {self.composition} - {self.prix} DT"

class Viennoiserie(Produit):
    composition = models.CharField(max_length=255)

    def get_details(self):
        return f"Viennoiserie {self.nom} - {self.composition} - {self.prix} DT"

class Avis(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    note = models.IntegerField()
    commentaire = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class Commande(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    produits = models.ManyToManyField(Produit, through='CommandeProduit')
    emplacement = models.CharField(max_length=100)
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Commande #{self.id} de {self.utilisateur.username}"

    def calculer_montant(self):
        total = sum([cp.quantite * cp.produit.prix for cp in self.commandeproduit_set.all()])
        self.montant = total
        self.save()

class CommandeProduit(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()


class Panier(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='paniers')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='paniers')
    quantite = models.PositiveIntegerField(default=1)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utilisateur', 'produit')

    def __str__(self):
        return f"{self.utilisateur} — {self.produit.nom} (x{self.quantite})"