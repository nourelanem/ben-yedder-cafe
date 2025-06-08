from django.contrib import admin
from .models import Client
from django.contrib.auth.models import User

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_full_name', 'get_email', 'telephone', 'adresse', 'date_creation')
    list_filter = ('date_creation',)
    search_fields = ('utilisateur__username', 'utilisateur__first_name', 'utilisateur__last_name', 'utilisateur__email', 'telephone')
    readonly_fields = ('date_creation',)

    def get_username(self, obj):
        return obj.utilisateur.username
    get_username.short_description = 'Nom d\'utilisateur'
    get_username.admin_order_field = 'utilisateur__username'

    def get_full_name(self, obj):
        return f"{obj.utilisateur.first_name} {obj.utilisateur.last_name}".strip() or "Non renseigné"
    get_full_name.short_description = 'Nom complet'
    get_full_name.admin_order_field = 'utilisateur__first_name'

    def get_email(self, obj):
        return obj.utilisateur.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'utilisateur__email'

    fieldsets = (
        ('Informations utilisateur', {
            'fields': ('utilisateur',)
        }),
        ('Informations client', {
            'fields': ('adresse', 'telephone', 'date_creation')
        }),
    )

    def has_add_permission(self, request):
        # Empêcher la création directe de clients depuis l'admin
        # Les clients doivent s'inscrire via le formulaire
        return False
