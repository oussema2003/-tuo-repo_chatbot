# Author: Dhaval Patel. Codebasics YouTube Channel
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
        cursor.execute("INSERT OR REPLACE INTO orders (order_id, item_id, quantity, total_price) VALUES (?, ?, ?, ?)", (order_id, item_id, quantity, total_price))
        
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
        
        cursor.execute("INSERT OR REPLACE INTO order_tracking (order_id, status) VALUES (?, ?)", (order_id, status))
        
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
