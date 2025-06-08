# ☕ Ben Yedder - Système de Gestion de Café

Un système de gestion complet pour café développé avec Django, permettant la gestion des produits, clients, commandes et panier d'achat.

## 🌟 Fonctionnalités

### 👥 Gestion des Utilisateurs
- **Inscription/Connexion** des clients
- **Profils clients** avec informations personnelles
- **Séparation** admin/client
- **Validation** anti-doublons (email unique)

### 📦 Gestion des Produits
- **Catalogue** de produits (cafés, boissons, viennoiseries)
- **Gestion du stock** en temps réel
- **Prix et descriptions** détaillés
- **Catégories** de produits

### 🛒 Système de Panier
- **Ajout/suppression** de produits
- **Gestion des quantités**
- **Calcul automatique** des totaux
- **Frais de livraison** intelligents

### 🔧 Administration
- **Interface admin** Django complète
- **Gestion des clients** depuis l'admin
- **Suivi des commandes**
- **Statistiques** et rapports

## 🚀 Installation

### Prérequis
- Python 3.8+
- Django 4.2+
- SQLite (inclus) ou PostgreSQL

### Installation rapide

```bash
# Cloner le projet
git clone https://github.com/votre-username/ben-yedder.git
cd ben-yedder

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

## 🔗 URLs Principales

- **Accueil** : `http://127.0.0.1:8000/`
- **Inscription** : `http://127.0.0.1:8000/accounts/register/`
- **Connexion** : `http://127.0.0.1:8000/accounts/login/`
- **Produits** : `http://127.0.0.1:8000/produits/`
- **Panier** : `http://127.0.0.1:8000/accounts/panier/`
- **Admin** : `http://127.0.0.1:8000/admin/`

## 👤 Comptes de Test

### Clients
| Username | Password | Email |
|----------|----------|-------|
| `sirine` | `test123` | elanemnour@gmail.com |
| `client1` | `test123` | client1@test.com |
| `lilia` | `test123` | lilia@gmail.com |

### Admin
| Username | Password | Email |
|----------|----------|-------|
| `admin` | `admin123` | admin@benyedder.com |

## 📁 Structure du Projet

```
BenYedder/
├── BenYedder/          # Configuration principale
│   ├── settings.py     # Paramètres Django
│   ├── urls.py         # URLs principales
│   └── wsgi.py         # Configuration WSGI
├── accounts/           # Gestion des utilisateurs
│   ├── models.py       # Modèles Client, Avis
│   ├── views.py        # Vues d'authentification
│   └── urls.py         # URLs des comptes
├── categories/         # Gestion des produits
│   ├── models.py       # Modèles Produit, Panier
│   ├── views.py        # Vues produits et panier
│   └── urls.py         # URLs des produits
├── templates/          # Templates HTML
│   ├── base.html       # Template de base
│   ├── home.html       # Page d'accueil
│   └── accounts/       # Templates des comptes
└── static/             # Fichiers statiques (CSS, JS)
```

## 🛠️ Technologies Utilisées

- **Backend** : Django 4.2, Python 3.8+
- **Base de données** : SQLite (développement)
- **Frontend** : HTML5, CSS3, JavaScript
- **Authentification** : Django Auth
- **API** : Django REST Framework
- **Admin** : Django Admin Interface

## 🔧 Configuration

### Variables d'environnement
Créez un fichier `.env` :

```env
SECRET_KEY=votre-clé-secrète
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
```

### Base de données
Le projet utilise SQLite par défaut. Pour PostgreSQL :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'benyedder_db',
        'USER': 'votre_user',
        'PASSWORD': 'votre_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📝 API Endpoints

### Produits
- `GET /api/produits/` - Liste des produits
- `GET /api/produits/{id}/` - Détail d'un produit
- `POST /api/panier/ajouter/` - Ajouter au panier

### Authentification
- `POST /api-auth/login/` - Connexion API
- `POST /api-auth/logout/` - Déconnexion API

## 🧪 Tests

```bash
# Lancer les tests
python manage.py test

# Tests avec couverture
coverage run --source='.' manage.py test
coverage report
```

## 🚀 Déploiement

### Heroku
```bash
# Installer Heroku CLI
# Créer une app Heroku
heroku create ben-yedder-app

# Configurer les variables
heroku config:set SECRET_KEY=votre-clé
heroku config:set DEBUG=False

# Déployer
git push heroku main
heroku run python manage.py migrate
```

### Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🤝 Contribution

1. Fork le projet
2. Créez une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

**Votre Nom**
- GitHub: [@votre-username](https://github.com/votre-username)
- Email: votre.email@example.com

## 🙏 Remerciements

- Django Community
- Bootstrap pour le design
- Tous les contributeurs

---

⭐ **N'hésitez pas à donner une étoile si ce projet vous a aidé !**
