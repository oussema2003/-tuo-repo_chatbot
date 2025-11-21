# Author: Dhaval Patel. Codebasics YouTube Channel

import mysql.connector
import os
from typing import Optional

# Configuration de la base de données
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "pandeyji_eatery"),
    "autocommit": False,
    "charset": "utf8mb4",
    "collation": "utf8mb4_unicode_ci"
}

# Variable globale pour la connexion
cnx: Optional[mysql.connector.connection.MySQLConnection] = None


def get_connection():
    """Établit une connexion à la base de données MySQL avec gestion d'erreurs améliorée"""
    global cnx
    
    try:
        # Vérifier si la connexion existe et est active
        if cnx is not None and cnx.is_connected():
            try:
                cnx.ping(reconnect=True, attempts=3, delay=2)
                return cnx
            except mysql.connector.Error as e:
                print(f"Erreur lors du ping de la connexion: {e}")
                cnx = None
    except Exception as e:
        print(f"Erreur lors de la vérification de la connexion: {e}")
        cnx = None

    # Créer une nouvelle connexion
    try:
        print("Tentative de connexion à la base de données...")
        cnx = mysql.connector.connect(**DB_CONFIG)
        
        # Tester la connexion
        cnx.ping(reconnect=True, attempts=3, delay=2)
        print("Connexion à la base de données établie avec succès!")
        return cnx
        
    except mysql.connector.Error as err:
        print(f"Erreur de connexion à MySQL: {err}")
        print(f"Code d'erreur: {err.errno}")
        print(f"Message d'erreur: {err.msg}")
        cnx = None
        raise
    except Exception as e:
        print(f"Erreur inattendue lors de la connexion: {e}")
        cnx = None
        raise

# Function to call the MySQL stored procedure and insert an order item
def insert_order_item(food_item, quantity, order_id):
    """Insère un article de commande dans la base de données"""
    connection = None
    cursor = None
    
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Calling the stored procedure
        cursor.callproc('insert_order_item', (food_item, int(quantity), order_id))

        # Committing the changes
        connection.commit()
        print(f"Article '{food_item}' (quantité: {quantity}) inséré avec succès pour la commande {order_id}")

        return 1

    except mysql.connector.Error as err:
        print(f"Erreur MySQL lors de l'insertion de l'article de commande: {err}")
        print(f"Code d'erreur: {err.errno}")
        print(f"Message d'erreur: {err.msg}")
        if connection:
            try:
                connection.rollback()
                print("Rollback effectué")
            except Exception as rollback_err:
                print(f"Erreur lors du rollback: {rollback_err}")
        return -1

    except Exception as e:
        print(f"Erreur inattendue lors de l'insertion de l'article: {e}")
        if connection:
            try:
                connection.rollback()
                print("Rollback effectué")
            except Exception as rollback_err:
                print(f"Erreur lors du rollback: {rollback_err}")
        return -1
    
    finally:
        if cursor:
            cursor.close()

# Function to insert a record into the order_tracking table
def insert_order_tracking(order_id, status):
    """Insère un enregistrement de suivi de commande dans la base de données"""
    connection = None
    cursor = None
    
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Inserting the record into the order_tracking table
        insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
        cursor.execute(insert_query, (order_id, status))

        # Committing the changes
        connection.commit()
        print(f"Statut de suivi '{status}' inséré avec succès pour la commande {order_id}")

    except mysql.connector.Error as err:
        print(f"Erreur MySQL lors de l'insertion du suivi de commande: {err}")
        print(f"Code d'erreur: {err.errno}")
        print(f"Message d'erreur: {err.msg}")
        if connection:
            try:
                connection.rollback()
                print("Rollback effectué")
            except Exception as rollback_err:
                print(f"Erreur lors du rollback: {rollback_err}")
        raise
    
    except Exception as e:
        print(f"Erreur inattendue lors de l'insertion du suivi: {e}")
        if connection:
            try:
                connection.rollback()
                print("Rollback effectué")
            except Exception as rollback_err:
                print(f"Erreur lors du rollback: {rollback_err}")
        raise
    
    finally:
        if cursor:
            cursor.close()


def get_total_order_price(order_id):
    """Récupère le prix total d'une commande"""
    connection = None
    cursor = None
    
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Executing the SQL query to get the total order price
        query = "SELECT get_total_order_price(%s)"
        cursor.execute(query, (order_id,))

        # Fetching the result
        result = cursor.fetchone()
        if result:
            total_price = result[0]
            print(f"Prix total récupéré pour la commande {order_id}: {total_price}")
            return total_price
        else:
            print(f"Aucun résultat trouvé pour la commande {order_id}")
            return None

    except mysql.connector.Error as err:
        print(f"Erreur MySQL lors de la récupération du prix total: {err}")
        print(f"Code d'erreur: {err.errno}")
        print(f"Message d'erreur: {err.msg}")
        return None
    
    except Exception as e:
        print(f"Erreur inattendue lors de la récupération du prix: {e}")
        return None
    
    finally:
        if cursor:
            cursor.close()

# Function to get the next available order_id
def get_next_order_id():
    """Récupère le prochain ID de commande disponible"""
    connection = None
    cursor = None
    
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Executing the SQL query to get the next available order_id
        query = "SELECT MAX(order_id) FROM orders"
        cursor.execute(query)

        # Fetching the result
        result = cursor.fetchone()
        if result and result[0] is not None:
            next_id = result[0] + 1
            print(f"Prochain ID de commande: {next_id}")
            return next_id
        else:
            print("Aucune commande existante, premier ID: 1")
            return 1

    except mysql.connector.Error as err:
        print(f"Erreur MySQL lors de la récupération du prochain ID: {err}")
        print(f"Code d'erreur: {err.errno}")
        print(f"Message d'erreur: {err.msg}")
        return 1  # Retourner 1 en cas d'erreur
    
    except Exception as e:
        print(f"Erreur inattendue lors de la récupération du prochain ID: {e}")
        return 1  # Retourner 1 en cas d'erreur
    
    finally:
        if cursor:
            cursor.close()

# Function to fetch the order status from the order_tracking table
def get_order_status(order_id):
    """Récupère le statut d'une commande"""
    connection = None
    cursor = None
    
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Executing the SQL query to fetch the order status
        query = "SELECT status FROM order_tracking WHERE order_id = %s"
        cursor.execute(query, (order_id,))

        # Fetching the result
        result = cursor.fetchone()

        # Returning the order status
        if result:
            status = result[0]
            print(f"Statut récupéré pour la commande {order_id}: {status}")
            return status
        else:
            print(f"Aucun statut trouvé pour la commande {order_id}")
            return None

    except mysql.connector.Error as err:
        print(f"Erreur MySQL lors de la récupération du statut: {err}")
        print(f"Code d'erreur: {err.errno}")
        print(f"Message d'erreur: {err.msg}")
        return None
    
    except Exception as e:
        print(f"Erreur inattendue lors de la récupération du statut: {e}")
        return None
    
    finally:
        if cursor:
            cursor.close()


if __name__ == "__main__":
    print(get_next_order_id())
