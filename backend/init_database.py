#!/usr/bin/env python3
"""
Script simple pour initialiser la base de données avec les données existantes
"""

import mysql.connector
import os
import sys

def get_mysql_password():
    """Demande le mot de passe MySQL à l'utilisateur"""
    print("Configuration de la base de données MySQL")
    print("=" * 40)
    
    # Essayer d'abord avec le mot de passe par défaut
    default_password = "root"
    
    print(f"Tentative avec le mot de passe par défaut: {default_password}")
    
    # Demander à l'utilisateur
    password = input(f"Entrez votre mot de passe MySQL (ou appuyez sur Entrée pour '{default_password}'): ").strip()
    
    if not password:
        password = default_password
    
    return password

def test_mysql_connection(password):
    """Teste la connexion MySQL"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password
        )
        print("✅ Connexion MySQL réussie!")
        connection.close()
        return True
    except mysql.connector.Error as err:
        print(f"❌ Erreur de connexion: {err}")
        return False

def create_database(password):
    """Crée la base de données"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password
        )
        
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS pandeyji_eatery")
        print("✅ Base de données 'pandeyji_eatery' créée/vérifiée")
        
        cursor.close()
        connection.close()
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ Erreur lors de la création de la base: {err}")
        return False

def import_sql_data(password):
    """Importe les données SQL"""
    sql_file = os.path.join("..", "db", "pandeyji_eatery.sql")
    
    if not os.path.exists(sql_file):
        print(f"❌ Fichier SQL non trouvé: {sql_file}")
        return False
    
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database="pandeyji_eatery"
        )
        
        cursor = connection.cursor()
        
        # Lire le fichier SQL
        with open(sql_file, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Exécuter les commandes SQL
        for statement in sql_content.split(';'):
            statement = statement.strip()
            if statement and not statement.startswith('--') and not statement.startswith('/*'):
                try:
                    cursor.execute(statement)
                except mysql.connector.Error as e:
                    # Ignorer les erreurs de tables existantes
                    if "already exists" not in str(e).lower():
                        print(f"⚠️  Avertissement: {e}")
        
        connection.commit()
        print("✅ Données SQL importées avec succès!")
        
        # Vérifier les données
        cursor.execute("SELECT COUNT(*) FROM food_items")
        count = cursor.fetchone()[0]
        print(f"✅ {count} articles de nourriture trouvés dans la base")
        
        cursor.close()
        connection.close()
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ Erreur lors de l'importation: {err}")
        return False

def update_db_config(password):
    """Met à jour la configuration de la base de données"""
    config_file = "db_helper.py"
    
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remplacer le mot de passe par défaut
        old_config = '"password": os.getenv("DB_PASSWORD", "root")'
        new_config = f'"password": os.getenv("DB_PASSWORD", "{password}")'
        
        if old_config in content:
            content = content.replace(old_config, new_config)
            
            with open(config_file, 'w', encoding='utf-8') as file:
                file.write(content)
            
            print("✅ Configuration mise à jour dans db_helper.py")
            return True
        else:
            print("⚠️  Configuration non trouvée dans db_helper.py")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour de la config: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 INITIALISATION DE LA BASE DE DONNÉES")
    print("=" * 50)
    
    # Étape 1: Obtenir le mot de passe
    password = get_mysql_password()
    
    # Étape 2: Tester la connexion
    print("\n1. Test de connexion MySQL...")
    if not test_mysql_connection(password):
        print("\n❌ Impossible de se connecter à MySQL")
        print("Vérifiez que MySQL est démarré et que le mot de passe est correct")
        return False
    
    # Étape 3: Créer la base de données
    print("\n2. Création de la base de données...")
    if not create_database(password):
        return False
    
    # Étape 4: Importer les données
    print("\n3. Importation des données...")
    if not import_sql_data(password):
        return False
    
    # Étape 5: Mettre à jour la configuration
    print("\n4. Mise à jour de la configuration...")
    update_db_config(password)
    
    print("\n" + "=" * 50)
    print("🎉 INITIALISATION TERMINÉE!")
    print("Votre chatbot peut maintenant utiliser la base de données.")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
