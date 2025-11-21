#!/usr/bin/env python3
"""
Script de démarrage simple pour le chatbot
"""

import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Teste que tous les imports fonctionnent"""
    try:
        print("🔍 Test des imports...")
        
        import db_helper_sqlite as db_helper
        print("✅ db_helper_sqlite importé")
        
        import generic_helper
        print("✅ generic_helper importé")
        
        import main
        print("✅ main importé")
        
        return True
    except Exception as e:
        print(f"❌ Erreur d'import: {e}")
        return False

def test_database():
    """Teste la base de données"""
    try:
        print("\n🔍 Test de la base de données...")
        
        import db_helper_sqlite as db_helper
        
        # Test de connexion
        next_id = db_helper.get_next_order_id()
        print(f"✅ Prochain ID: {next_id}")
        
        # Test de récupération d'un statut
        status = db_helper.get_order_status(40)
        if status:
            print(f"✅ Statut commande 40: {status}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur de base de données: {e}")
        return False

def start_server():
    """Démarre le serveur"""
    try:
        print("\n🚀 Démarrage du serveur...")
        
        import uvicorn
        from main import app
        
        print("✅ Application FastAPI chargée")
        print("🌐 Démarrage sur http://127.0.0.1:8000")
        print("📖 Documentation: http://127.0.0.1:8000/docs")
        print("🛑 Appuyez sur Ctrl+C pour arrêter")
        
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ Erreur de démarrage: {e}")
        return False

def main():
    """Fonction principale"""
    print("🤖 DÉMARRAGE DU CHATBOT")
    print("=" * 40)
    
    # Test des imports
    if not test_imports():
        print("\n❌ Problème d'import détecté")
        return False
    
    # Test de la base de données
    if not test_database():
        print("\n❌ Problème de base de données détecté")
        return False
    
    print("\n✅ Tous les tests sont passés!")
    
    # Démarrer le serveur
    start_server()
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)
