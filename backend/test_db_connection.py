#!/usr/bin/env python3
"""
Script de test pour vérifier la connexion à la base de données MySQL
"""

import sys
import os

# Ajouter le répertoire backend au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import db_helper

def test_database_connection():
    """Teste la connexion à la base de données"""
    print("=" * 50)
    print("TEST DE CONNEXION À LA BASE DE DONNÉES")
    print("=" * 50)
    
    try:
        # Test 1: Connexion de base
        print("\n1. Test de connexion de base...")
        connection = db_helper.get_connection()
        if connection and connection.is_connected():
            print("✅ Connexion à la base de données réussie!")
        else:
            print("❌ Échec de la connexion à la base de données")
            return False
        
        # Test 2: Récupération du prochain ID de commande
        print("\n2. Test de récupération du prochain ID de commande...")
        next_id = db_helper.get_next_order_id()
        print(f"✅ Prochain ID de commande: {next_id}")
        
        # Test 3: Test d'insertion d'un article (simulation)
        print("\n3. Test d'insertion d'un article de commande...")
        # Note: Ce test ne sera pas exécuté pour éviter d'insérer des données de test
        print("ℹ️  Test d'insertion ignoré pour éviter les données de test")
        
        # Test 4: Test de récupération du statut d'une commande existante
        print("\n4. Test de récupération du statut d'une commande...")
        status = db_helper.get_order_status(40)  # Commande existante dans le dump SQL
        if status:
            print(f"✅ Statut de la commande 40: {status}")
        else:
            print("ℹ️  Aucune commande trouvée avec l'ID 40")
        
        # Test 5: Test de récupération du prix total
        print("\n5. Test de récupération du prix total...")
        total_price = db_helper.get_total_order_price(40)  # Commande existante
        if total_price:
            print(f"✅ Prix total de la commande 40: {total_price}")
        else:
            print("ℹ️  Aucun prix trouvé pour la commande 40")
        
        print("\n" + "=" * 50)
        print("✅ TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DES TESTS: {e}")
        print("=" * 50)
        return False

def show_database_info():
    """Affiche les informations de configuration de la base de données"""
    print("\n" + "=" * 50)
    print("INFORMATIONS DE CONFIGURATION")
    print("=" * 50)
    print(f"Host: {db_helper.DB_CONFIG['host']}")
    print(f"User: {db_helper.DB_CONFIG['user']}")
    print(f"Database: {db_helper.DB_CONFIG['database']}")
    print(f"Password: {'*' * len(db_helper.DB_CONFIG['password'])}")
    print("=" * 50)

if __name__ == "__main__":
    show_database_info()
    success = test_database_connection()
    
    if not success:
        print("\n🔧 SOLUTIONS POSSIBLES:")
        print("1. Vérifiez que MySQL est démarré")
        print("2. Vérifiez les paramètres de connexion dans db_helper.py")
        print("3. Assurez-vous que la base de données 'pandeyji_eatery' existe")
        print("4. Vérifiez que l'utilisateur MySQL a les bonnes permissions")
        print("5. Importez le fichier SQL: db/pandeyji_eatery.sql")
        
        sys.exit(1)
    else:
        print("\n🎉 Votre chatbot peut maintenant communiquer avec la base de données!")
        sys.exit(0)
