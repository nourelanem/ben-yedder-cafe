# 0001_initial.py - corrigé avec app nommée 'categories'

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statut', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('prix', models.DecimalField(decimal_places=2, max_digits=8)),
                ('image', models.ImageField(upload_to='produits/')),
                ('stock', models.PositiveIntegerField()),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produits', to='categories.categorie')),
            ],
        ),
        migrations.CreateModel(
            name='CommandeProduit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.PositiveIntegerField()),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.commande')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.produit')),
            ],
        ),
        migrations.AddField(
            model_name='commande',
            name='produits',
            field=models.ManyToManyField(through='categories.CommandeProduit', to='categories.Produit'),
        ),
        migrations.CreateModel(
            name='Avis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.IntegerField()),
                ('commentaire', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.Produit')),
            ],
        ),
    ]
