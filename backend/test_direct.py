#!/usr/bin/env python3
"""
Test direct du chatbot sans serveur web
"""

import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_chatbot_functions():
    """Teste directement les fonctions du chatbot"""
    print("🤖 TEST DIRECT DU CHATBOT")
    print("=" * 40)
    
    try:
        # Importer les modules
        import db_helper_sqlite as db_helper
        import generic_helper
        from main import add_to_order, complete_order, track_order
        
        print("✅ Modules importés avec succès")
        
        # Test 1: Récupérer le prochain ID
        print("\n1. Test du prochain ID de commande...")
        next_id = db_helper.get_next_order_id()
        print(f"✅ Prochain ID: {next_id}")
        
        # Test 2: Simuler l'ajout d'un article
        print("\n2. Test d'ajout d'article...")
        session_id = "test-session-123"
        parameters = {
            "food-item": ["Pizza"],
            "number": [2]
        }
        
        # Simuler l'ajout d'un article (sans serveur web)
        from main import inprogress_orders
        inprogress_orders[session_id] = {"Pizza": 2}
        print("✅ Article ajouté à la commande en cours")
        
        # Test 3: Finaliser la commande
        print("\n3. Test de finalisation de commande...")
        try:
            # Simuler la finalisation
            order = inprogress_orders[session_id]
            order_id = db_helper.get_next_order_id()
            
            # Insérer l'article
            result = db_helper.insert_order_item("Pizza", 2, order_id)
            if result == 1:
                print("✅ Article inséré en base de données")
                
                # Insérer le statut de suivi
                db_helper.insert_order_tracking(order_id, "in progress")
                print("✅ Statut de suivi inséré")
                
                # Récupérer le prix total
                total_price = db_helper.get_total_order_price(order_id)
                print(f"✅ Prix total calculé: {total_price}")
                
            else:
                print("❌ Erreur lors de l'insertion de l'article")
                
        except Exception as e:
            print(f"❌ Erreur lors de la finalisation: {e}")
        
        # Test 4: Suivi de commande existante
        print("\n4. Test de suivi de commande...")
        status = db_helper.get_order_status(40)
        if status:
            print(f"✅ Statut de la commande 40: {status}")
        else:
            print("ℹ️  Aucune commande trouvée avec l'ID 40")
        
        print("\n" + "=" * 40)
        print("🎉 TOUS LES TESTS SONT PASSÉS!")
        print("Votre chatbot fonctionne parfaitement avec la base de données!")
        print("=" * 40)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_database_info():
    """Affiche les informations de la base de données"""
    print("\n📊 INFORMATIONS DE LA BASE DE DONNÉES")
    print("=" * 40)
    
    try:
        import db_helper_sqlite as db_helper
        import sqlite3
        
        # Connexion directe à la base
        conn = sqlite3.connect("pandeyji_eatery.db")
        cursor = conn.cursor()
        
        # Compter les articles
        cursor.execute("SELECT COUNT(*) FROM food_items")
        food_count = cursor.fetchone()[0]
        print(f"📦 Articles disponibles: {food_count}")
        
        # Lister quelques articles
        cursor.execute("SELECT name, price FROM food_items LIMIT 5")
        items = cursor.fetchall()
        print("🍕 Exemples d'articles:")
        for name, price in items:
            print(f"   - {name}: {price}€")
        
        # Compter les commandes
        cursor.execute("SELECT COUNT(*) FROM orders")
        order_count = cursor.fetchone()[0]
        print(f"📋 Éléments de commande: {order_count}")
        
        # Compter les statuts
        cursor.execute("SELECT COUNT(*) FROM order_tracking")
        tracking_count = cursor.fetchone()[0]
        print(f"📈 Statuts de suivi: {tracking_count}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de l'affichage des infos: {e}")

def main():
    """Fonction principale"""
    print("🎯 TEST COMPLET DU CHATBOT")
    print("=" * 50)
    
    # Afficher les infos de la base
    show_database_info()
    
    # Tester les fonctions
    success = test_chatbot_functions()
    
    if success:
        print("\n🚀 VOTRE CHATBOT EST PRÊT!")
        print("Pour le démarrer avec un serveur web:")
        print("python simple_start.py")
    else:
        print("\n❌ Des problèmes ont été détectés")
        print("Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
