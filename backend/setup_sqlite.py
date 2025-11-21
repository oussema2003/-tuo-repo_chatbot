#!/usr/bin/env python3
"""
Script pour configurer SQLite comme base de données alternative
SQLite est plus simple et ne nécessite pas de serveur séparé
"""

import sqlite3
import os
import sys

def create_sqlite_database():
    """Crée la base de données SQLite et importe les données"""
    print("🚀 CONFIGURATION DE SQLITE POUR LE CHATBOT")
    print("=" * 50)
    
    db_path = "pandeyji_eatery.db"
    
    try:
        # Créer la connexion SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("✅ Connexion SQLite établie")
        
        # Créer les tables
        print("\n1. Création des tables...")
        
        # Table food_items
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS food_items (
            item_id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL
        )
        ''')
        
        # Table orders
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER,
            item_id INTEGER,
            quantity INTEGER,
            total_price REAL,
            PRIMARY KEY (order_id, item_id),
            FOREIGN KEY (item_id) REFERENCES food_items (item_id)
        )
        ''')
        
        # Table order_tracking
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_tracking (
            order_id INTEGER PRIMARY KEY,
            status TEXT
        )
        ''')
        
        print("✅ Tables créées")
        
        # Insérer les données initiales
        print("\n2. Insertion des données initiales...")
        
        # Données des articles de nourriture
        food_items = [
            (1, 'Pav Bhaji', 6.00),
            (2, 'Chole Bhature', 7.00),
            (3, 'Pizza', 8.00),
            (4, 'Mango Lassi', 5.00),
            (5, 'Masala Dosa', 6.00),
            (6, 'Vegetable Biryani', 9.00),
            (7, 'Vada Pav', 4.00),
            (8, 'Rava Dosa', 7.00),
            (9, 'Samosa', 5.00)
        ]
        
        cursor.executemany('''
        INSERT OR REPLACE INTO food_items (item_id, name, price) 
        VALUES (?, ?, ?)
        ''', food_items)
        
        # Données de commandes existantes
        orders = [
            (40, 1, 2, 12.00),
            (40, 3, 1, 8.00),
            (41, 4, 3, 15.00),
            (41, 6, 2, 18.00),
            (41, 9, 4, 20.00)
        ]
        
        cursor.executemany('''
        INSERT OR REPLACE INTO orders (order_id, item_id, quantity, total_price) 
        VALUES (?, ?, ?, ?)
        ''', orders)
        
        # Données de suivi des commandes
        order_tracking = [
            (40, 'delivered'),
            (41, 'in transit')
        ]
        
        cursor.executemany('''
        INSERT OR REPLACE INTO order_tracking (order_id, status) 
        VALUES (?, ?)
        ''', order_tracking)
        
        conn.commit()
        print("✅ Données initiales insérées")
        
        # Vérifier les données
        print("\n3. Vérification des données...")
        cursor.execute("SELECT COUNT(*) FROM food_items")
        food_count = cursor.fetchone()[0]
        print(f"✅ {food_count} articles de nourriture")
        
        cursor.execute("SELECT COUNT(*) FROM orders")
        order_count = cursor.fetchone()[0]
        print(f"✅ {order_count} éléments de commande")
        
        cursor.execute("SELECT COUNT(*) FROM order_tracking")
        tracking_count = cursor.fetchone()[0]
        print(f"✅ {tracking_count} statuts de commande")
        
        cursor.close()
        conn.close()
        
        print(f"\n✅ Base de données SQLite créée: {db_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de la base SQLite: {e}")
        return False

def create_sqlite_helper():
    """Crée un helper SQLite pour remplacer db_helper.py"""
    print("\n4. Création du helper SQLite...")
    
    sqlite_helper_content = '''# Author: Dhaval Patel. Codebasics YouTube Channel
# Modifié pour utiliser SQLite au lieu de MySQL

import sqlite3
import os
from typing import Optional

# Chemin vers la base de données SQLite
DB_PATH = os.path.join(os.path.dirname(__file__), "pandeyji_eatery.db")

def get_connection():
    """Établit une connexion à la base de données SQLite"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
        return conn
    except sqlite3.Error as err:
        print(f"Erreur de connexion SQLite: {err}")
        raise

def insert_order_item(food_item, quantity, order_id):
    """Insère un article de commande dans la base de données"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Récupérer l'item_id et le prix
        cursor.execute("SELECT item_id, price FROM food_items WHERE name = ?", (food_item,))
        result = cursor.fetchone()
        
        if not result:
            print(f"Article non trouvé: {food_item}")
            return -1
        
        item_id, price = result
        total_price = price * int(quantity)
        
        # Insérer dans la table orders
        cursor.execute('''
        INSERT OR REPLACE INTO orders (order_id, item_id, quantity, total_price) 
        VALUES (?, ?, ?, ?)
        ''', (order_id, item_id, quantity, total_price))
        
        conn.commit()
        print(f"Article '{food_item}' (quantité: {quantity}) inséré avec succès pour la commande {order_id}")
        
        cursor.close()
        conn.close()
        return 1
        
    except sqlite3.Error as err:
        print(f"Erreur SQLite lors de l'insertion: {err}")
        return -1
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        return -1

def insert_order_tracking(order_id, status):
    """Insère un enregistrement de suivi de commande"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO order_tracking (order_id, status) 
        VALUES (?, ?)
        ''', (order_id, status))
        
        conn.commit()
        print(f"Statut de suivi '{status}' inséré avec succès pour la commande {order_id}")
        
        cursor.close()
        conn.close()
        
    except sqlite3.Error as err:
        print(f"Erreur SQLite lors de l'insertion du suivi: {err}")
        raise
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        raise

def get_total_order_price(order_id):
    """Récupère le prix total d'une commande"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT SUM(total_price) FROM orders WHERE order_id = ?", (order_id,))
        result = cursor.fetchone()
        
        if result and result[0] is not None:
            total_price = result[0]
            print(f"Prix total récupéré pour la commande {order_id}: {total_price}")
            return total_price
        else:
            print(f"Aucun prix trouvé pour la commande {order_id}")
            return None
        
        cursor.close()
        conn.close()
        
    except sqlite3.Error as err:
        print(f"Erreur SQLite lors de la récupération du prix: {err}")
        return None
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        return None

def get_next_order_id():
    """Récupère le prochain ID de commande disponible"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT MAX(order_id) FROM orders")
        result = cursor.fetchone()
        
        if result and result[0] is not None:
            next_id = result[0] + 1
            print(f"Prochain ID de commande: {next_id}")
            return next_id
        else:
            print("Aucune commande existante, premier ID: 1")
            return 1
        
        cursor.close()
        conn.close()
        
    except sqlite3.Error as err:
        print(f"Erreur SQLite lors de la récupération du prochain ID: {err}")
        return 1
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        return 1

def get_order_status(order_id):
    """Récupère le statut d'une commande"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT status FROM order_tracking WHERE order_id = ?", (order_id,))
        result = cursor.fetchone()
        
        if result:
            status = result[0]
            print(f"Statut récupéré pour la commande {order_id}: {status}")
            return status
        else:
            print(f"Aucun statut trouvé pour la commande {order_id}")
            return None
        
        cursor.close()
        conn.close()
        
    except sqlite3.Error as err:
        print(f"Erreur SQLite lors de la récupération du statut: {err}")
        return None
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        return None

if __name__ == "__main__":
    print(get_next_order_id())
'''
    
    try:
        with open("db_helper_sqlite.py", "w", encoding="utf-8") as f:
            f.write(sqlite_helper_content)
        print("✅ Helper SQLite créé: db_helper_sqlite.py")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création du helper: {e}")
        return False

def update_main_py():
    """Met à jour main.py pour utiliser SQLite"""
    print("\n5. Mise à jour de main.py...")
    
    try:
        with open("main.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Remplacer l'import de db_helper par db_helper_sqlite
        content = content.replace("import db_helper", "import db_helper_sqlite as db_helper")
        
        with open("main.py", "w", encoding="utf-8") as f:
            f.write(content)
        
        print("✅ main.py mis à jour pour utiliser SQLite")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour de main.py: {e}")
        return False

def test_sqlite_connection():
    """Teste la connexion SQLite"""
    print("\n6. Test de la connexion SQLite...")
    
    try:
        import db_helper_sqlite as db_helper
        
        # Test de récupération du prochain ID
        next_id = db_helper.get_next_order_id()
        print(f"✅ Prochain ID de commande: {next_id}")
        
        # Test de récupération du statut
        status = db_helper.get_order_status(40)
        if status:
            print(f"✅ Statut de la commande 40: {status}")
        
        # Test de récupération du prix total
        total_price = db_helper.get_total_order_price(40)
        if total_price:
            print(f"✅ Prix total de la commande 40: {total_price}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def main():
    """Fonction principale"""
    print("🎯 CONFIGURATION SQLITE POUR VOTRE CHATBOT")
    print("=" * 60)
    
    # Créer la base de données SQLite
    if not create_sqlite_database():
        return False
    
    # Créer le helper SQLite
    if not create_sqlite_helper():
        return False
    
    # Mettre à jour main.py
    if not update_main_py():
        return False
    
    # Tester la connexion
    if not test_sqlite_connection():
        return False
    
    print("\n" + "=" * 60)
    print("🎉 CONFIGURATION SQLITE TERMINÉE AVEC SUCCÈS!")
    print("Votre chatbot utilise maintenant SQLite comme base de données!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Échec de la configuration SQLite")
        sys.exit(1)
