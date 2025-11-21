#!/usr/bin/env python3
"""
Script pour configurer MariaDB et importer les données du chatbot
"""

import subprocess
import os
import sys

def run_command(command, description):
    """Exécute une commande et affiche le résultat"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Succès")
            if result.stdout:
                print(f"Sortie: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - Échec")
            if result.stderr:
                print(f"Erreur: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def setup_mariadb():
    """Configure MariaDB pour le chatbot"""
    print("🚀 CONFIGURATION DE MARIADB POUR LE CHATBOT")
    print("=" * 50)
    
    # Étape 1: Démarrer le service MariaDB
    print("\n1. Démarrage du service MariaDB...")
    if not run_command("net start mariadb", "Démarrage du service MariaDB"):
        print("⚠️  Le service MariaDB pourrait déjà être démarré")
    
    # Étape 2: Créer la base de données
    print("\n2. Création de la base de données...")
    create_db_sql = """
    CREATE DATABASE IF NOT EXISTS pandeyji_eatery CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    """
    
    # Écrire le SQL dans un fichier temporaire
    with open("temp_create_db.sql", "w") as f:
        f.write(create_db_sql)
    
    if run_command("mysql -u root < temp_create_db.sql", "Création de la base de données"):
        print("✅ Base de données 'pandeyji_eatery' créée")
    else:
        print("⚠️  Tentative de création de la base de données...")
    
    # Nettoyer le fichier temporaire
    if os.path.exists("temp_create_db.sql"):
        os.remove("temp_create_db.sql")
    
    # Étape 3: Importer les données
    print("\n3. Importation des données...")
    sql_file = os.path.join("..", "db", "pandeyji_eatery.sql")
    
    if os.path.exists(sql_file):
        if run_command(f"mysql -u root pandeyji_eatery < \"{sql_file}\"", "Importation des données SQL"):
            print("✅ Données importées avec succès")
        else:
            print("⚠️  Problème lors de l'importation, essayons une approche différente...")
            import_data_manually(sql_file)
    else:
        print(f"❌ Fichier SQL non trouvé: {sql_file}")
        return False
    
    # Étape 4: Vérifier l'importation
    print("\n4. Vérification des données...")
    check_sql = "SELECT COUNT(*) FROM food_items;"
    with open("temp_check.sql", "w") as f:
        f.write(check_sql)
    
    if run_command("mysql -u root pandeyji_eatery < temp_check.sql", "Vérification des données"):
        print("✅ Données vérifiées")
    
    # Nettoyer
    if os.path.exists("temp_check.sql"):
        os.remove("temp_check.sql")
    
    return True

def import_data_manually(sql_file):
    """Importe les données manuellement en cas d'échec"""
    print("📝 Importation manuelle des données...")
    
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Diviser en commandes individuelles
        commands = []
        current_command = ""
        
        for line in sql_content.split('\n'):
            line = line.strip()
            if line and not line.startswith('--') and not line.startswith('/*'):
                current_command += line + " "
                if line.endswith(';'):
                    commands.append(current_command.strip())
                    current_command = ""
        
        # Exécuter chaque commande
        for i, command in enumerate(commands):
            if command:
                with open(f"temp_cmd_{i}.sql", "w") as f:
                    f.write(command)
                
                if run_command(f"mysql -u root pandeyji_eatery < temp_cmd_{i}.sql", f"Commande {i+1}"):
                    print(f"✅ Commande {i+1} exécutée")
                else:
                    print(f"⚠️  Commande {i+1} ignorée")
                
                # Nettoyer
                if os.path.exists(f"temp_cmd_{i}.sql"):
                    os.remove(f"temp_cmd_{i}.sql")
        
        print("✅ Importation manuelle terminée")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'importation manuelle: {e}")

def update_db_helper():
    """Met à jour db_helper.py pour MariaDB"""
    print("\n5. Mise à jour de la configuration...")
    
    try:
        with open("db_helper.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer les paramètres par défaut pour MariaDB
        replacements = [
            ('"password": os.getenv("DB_PASSWORD", "root")', '"password": os.getenv("DB_PASSWORD", "")'),
        ]
        
        for old, new in replacements:
            content = content.replace(old, new)
        
        with open("db_helper.py", 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Configuration mise à jour pour MariaDB")
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")

def test_connection():
    """Teste la connexion à la base de données"""
    print("\n6. Test de la connexion...")
    
    try:
        import db_helper
        
        # Test de connexion
        connection = db_helper.get_connection()
        if connection and connection.is_connected():
            print("✅ Connexion à MariaDB réussie!")
            
            # Test de récupération des données
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM food_items")
            count = cursor.fetchone()[0]
            print(f"✅ {count} articles trouvés dans la base de données")
            
            cursor.close()
            connection.close()
            return True
        else:
            print("❌ Échec de la connexion")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def main():
    """Fonction principale"""
    print("🎯 CONFIGURATION MARIADB POUR VOTRE CHATBOT")
    print("=" * 60)
    
    # Configuration de MariaDB
    if not setup_mariadb():
        print("\n❌ Échec de la configuration de MariaDB")
        return False
    
    # Mise à jour de la configuration
    update_db_helper()
    
    # Test de la connexion
    if test_connection():
        print("\n" + "=" * 60)
        print("🎉 CONFIGURATION TERMINÉE AVEC SUCCÈS!")
        print("Votre chatbot peut maintenant utiliser MariaDB!")
        print("=" * 60)
        return True
    else:
        print("\n❌ Problème de connexion détecté")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n🔧 SOLUTIONS ALTERNATIVES:")
        print("1. Vérifiez que MariaDB est démarré")
        print("2. Configurez un mot de passe pour l'utilisateur root")
        print("3. Créez un utilisateur dédié pour le chatbot")
        sys.exit(1)
