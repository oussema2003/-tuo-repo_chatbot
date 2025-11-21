#!/usr/bin/env python3
"""
Script de démarrage pour le chatbot avec base de données SQLite
"""

import uvicorn
import os
import sys

def check_database():
    """Vérifie que la base de données SQLite existe"""
    db_path = "pandeyji_eatery.db"
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        print("Exécutez d'abord: python setup_sqlite_fixed.py")
        return False
    
    print(f"✅ Base de données trouvée: {db_path}")
    return True

def check_dependencies():
    """Vérifie que les dépendances sont installées"""
    try:
        import fastapi
        import sqlite3
        print("✅ Dépendances installées")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("Installez avec: pip install -r requirements.txt")
        return False

def main():
    """Démarre le chatbot"""
    print("🚀 DÉMARRAGE DU CHATBOT")
    print("=" * 40)
    
    # Vérifications préalables
    if not check_dependencies():
        return False
    
    if not check_database():
        return False
    
    print("\n✅ Toutes les vérifications sont passées")
    print("🌐 Démarrage du serveur sur http://localhost:8000")
    print("📖 Documentation: http://localhost:8000/docs")
    print("🛑 Appuyez sur Ctrl+C pour arrêter")
    print("=" * 40)
    
    try:
        # Démarrer le serveur
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Serveur arrêté par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du démarrage: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
