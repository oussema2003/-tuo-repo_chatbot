# Configuration de la Base de Données pour le Chatbot

## Problème Résolu

Votre chatbot ne pouvait pas communiquer avec la base de données MySQL. Les problèmes identifiés et corrigés :

1. **Gestion des erreurs de connexion** : Amélioration de la gestion des erreurs MySQL
2. **Configuration flexible** : Support des variables d'environnement
3. **Logging détaillé** : Messages d'erreur plus informatifs
4. **Gestion des connexions** : Meilleure gestion du cycle de vie des connexions

## Prérequis

1. **MySQL Server** installé et démarré
2. **Python 3.7+** avec les dépendances installées

## Installation

### 1. Installer les dépendances Python

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configurer MySQL

Assurez-vous que MySQL est démarré et accessible avec les paramètres par défaut :
- Host: `localhost`
- User: `root`
- Password: `root`
- Database: `pandeyji_eatery`

### 3. Initialiser la base de données

```bash
python setup_database.py
```

Ce script va :
- Créer la base de données `pandeyji_eatery`
- Importer le fichier SQL `db/pandeyji_eatery.sql`
- Vérifier que tout fonctionne correctement

### 4. Tester la connexion

```bash
python test_db_connection.py
```

## Configuration Personnalisée

Si vos paramètres MySQL sont différents, vous pouvez :

### Option 1: Variables d'environnement

```bash
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=votre_mot_de_passe
export DB_NAME=pandeyji_eatery
```

### Option 2: Modifier directement le fichier

Éditez `backend/db_helper.py` et modifiez la section `DB_CONFIG` :

```python
DB_CONFIG = {
    "host": "votre_host",
    "user": "votre_utilisateur",
    "password": "votre_mot_de_passe",
    "database": "pandeyji_eatery",
    "autocommit": False,
    "charset": "utf8mb4",
    "collation": "utf8mb4_unicode_ci"
}
```

## Démarrer le Chatbot

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Fonctionnalités de la Base de Données

Le chatbot peut maintenant :

1. **Ajouter des articles** à une commande
2. **Supprimer des articles** d'une commande
3. **Finaliser une commande** et l'enregistrer en base
4. **Suivre le statut** d'une commande
5. **Calculer le prix total** d'une commande

## Tables de la Base de Données

- `food_items` : Catalogue des articles disponibles
- `orders` : Détails des commandes (articles et quantités)
- `order_tracking` : Statut de suivi des commandes

## Dépannage

### Erreur de connexion MySQL

```
Erreur de connexion à MySQL: 2003 (HY000): Can't connect to MySQL server
```

**Solutions :**
1. Vérifiez que MySQL est démarré
2. Vérifiez les paramètres de connexion
3. Vérifiez que le port 3306 est accessible

### Base de données n'existe pas

```
Erreur MySQL: 1049 (42000): Unknown database 'pandeyji_eatery'
```

**Solution :**
```bash
python setup_database.py
```

### Permissions insuffisantes

```
Erreur MySQL: 1045 (28000): Access denied for user 'root'@'localhost'
```

**Solutions :**
1. Vérifiez le mot de passe MySQL
2. Créez un utilisateur dédié avec les bonnes permissions
3. Modifiez les paramètres de connexion

## Logs et Debug

Le chatbot affiche maintenant des logs détaillés :
- Tentatives de connexion
- Opérations réussies
- Erreurs avec codes et messages
- Rollbacks automatiques en cas d'erreur

Consultez les logs de votre serveur pour diagnostiquer les problèmes.
