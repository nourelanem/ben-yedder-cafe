#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BenYedder.settings')
django.setup()

from categories.models import Cafe, Boisson, Viennoiserie

def create_test_products():
    print("🔄 Création des produits de test...")
    
    # Créer des cafés
    cafes_data = [
        {
            'nom': 'Espresso Classique',
            'description': 'Un espresso traditionnel avec une crème parfaite',
            'prix': 3.50,
            'stock': 100,
            'composition': 'Arabica 100%, torréfaction moyenne, origine Italie'
        },
        {
            'nom': 'Café Tunisien',
            'description': 'Café traditionnel tunisien aux épices',
            'prix': 4.00,
            'stock': 80,
            'composition': 'Mélange arabica et robusta, épices traditionnelles'
        },
        {
            'nom': 'Cappuccino',
            'description': 'Espresso avec mousse de lait onctueuse',
            'prix': 5.00,
            'stock': 90,
            'composition': 'Espresso, lait vapeur, mousse de lait'
        },
        {
            'nom': 'Café Turc',
            'description': 'Café turc traditionnel finement moulu',
            'prix': 4.50,
            'stock': 60,
            'composition': 'Café finement moulu, préparation traditionnelle turque'
        }
    ]
    
    for cafe_data in cafes_data:
        cafe, created = Cafe.objects.get_or_create(
            nom=cafe_data['nom'],
            defaults=cafe_data
        )
        if created:
            print(f"✅ Café créé: {cafe.nom}")
        else:
            print(f"⚠️ Café existe déjà: {cafe.nom}")
    
    # Créer des boissons
    boissons_data = [
        {
            'nom': 'Thé à la Menthe',
            'description': 'Thé vert traditionnel à la menthe fraîche',
            'prix': 2.50,
            'stock': 120,
            'volume': 250
        },
        {
            'nom': 'Jus d\'Orange Frais',
            'description': 'Jus d\'orange pressé à la minute',
            'prix': 3.00,
            'stock': 50,
            'volume': 350
        },
        {
            'nom': 'Limonade Maison',
            'description': 'Limonade fraîche faite maison',
            'prix': 2.80,
            'stock': 70,
            'volume': 300
        },
        {
            'nom': 'Chocolat Chaud',
            'description': 'Chocolat chaud onctueux avec chantilly',
            'prix': 4.20,
            'stock': 40,
            'volume': 250
        }
    ]
    
    for boisson_data in boissons_data:
        boisson, created = Boisson.objects.get_or_create(
            nom=boisson_data['nom'],
            defaults=boisson_data
        )
        if created:
            print(f"✅ Boisson créée: {boisson.nom}")
        else:
            print(f"⚠️ Boisson existe déjà: {boisson.nom}")
    
    # Créer des viennoiseries
    viennoiseries_data = [
        {
            'nom': 'Croissant au Beurre',
            'description': 'Croissant traditionnel français au beurre',
            'prix': 2.00,
            'stock': 30,
            'composition': 'Pâte feuilletée, beurre français, nature'
        },
        {
            'nom': 'Pain au Chocolat',
            'description': 'Viennoiserie avec chocolat noir',
            'prix': 2.50,
            'stock': 25,
            'composition': 'Pâte feuilletée, chocolat noir 70%'
        },
        {
            'nom': 'Makroudh',
            'description': 'Pâtisserie tunisienne aux dattes',
            'prix': 1.80,
            'stock': 40,
            'composition': 'Semoule fine, dattes fraîches, miel'
        },
        {
            'nom': 'Baklawa',
            'description': 'Pâtisserie orientale aux amandes et miel',
            'prix': 3.00,
            'stock': 20,
            'composition': 'Pâte phyllo, amandes, miel, pistaches'
        },
        {
            'nom': 'Chausson aux Pommes',
            'description': 'Pâte feuilletée garnie de compote de pommes',
            'prix': 2.80,
            'stock': 15,
            'composition': 'Pâte feuilletée, compote de pommes maison'
        }
    ]
    
    for viennoiserie_data in viennoiseries_data:
        viennoiserie, created = Viennoiserie.objects.get_or_create(
            nom=viennoiserie_data['nom'],
            defaults=viennoiserie_data
        )
        if created:
            print(f"✅ Viennoiserie créée: {viennoiserie.nom}")
        else:
            print(f"⚠️ Viennoiserie existe déjà: {viennoiserie.nom}")
    
    print("\n🎉 Création des produits terminée !")
    print(f"📊 Total produits:")
    print(f"   ☕ Cafés: {Cafe.objects.count()}")
    print(f"   🥤 Boissons: {Boisson.objects.count()}")
    print(f"   🥐 Viennoiseries: {Viennoiserie.objects.count()}")

if __name__ == '__main__':
    create_test_products()
