#!/usr/bin/env python3
"""
Script pour trouver la configuration MySQL correcte
"""

import mysql.connector

def test_mysql_config(host, user, password, database=None):
    """Teste une configuration MySQL"""
    try:
        config = {
            "host": host,
            "user": user,
            "password": password
        }
        if database:
            config["database"] = database
            
        connection = mysql.connector.connect(**config)
        print(f"✅ SUCCÈS: {user}@{host} avec mot de passe '{password}'")
        connection.close()
        return True
    except mysql.connector.Error as err:
        print(f"❌ ÉCHEC: {user}@{host} avec mot de passe '{password}' - {err}")
        return False

def main():
    """Teste différentes configurations MySQL communes"""
    print("🔍 RECHERCHE DE LA CONFIGURATION MYSQL")
    print("=" * 50)
    
    # Configurations à tester
    configs = [
        # (host, user, password, database)
        ("localhost", "root", "", None),           # Mot de passe vide
        ("localhost", "root", "root", None),       # Mot de passe "root"
        ("localhost", "root", "password", None),   # Mot de passe "password"
        ("localhost", "root", "123456", None),     # Mot de passe "123456"
        ("localhost", "root", "mysql", None),      # Mot de passe "mysql"
        ("127.0.0.1", "root", "", None),           # IP locale avec mot de passe vide
        ("127.0.0.1", "root", "root", None),       # IP locale avec mot de passe "root"
    ]
    
    successful_configs = []
    
    for host, user, password, database in configs:
        if test_mysql_config(host, user, password, database):
            successful_configs.append((host, user, password, database))
    
    print("\n" + "=" * 50)
    
    if successful_configs:
        print(f"🎉 {len(successful_configs)} configuration(s) trouvée(s):")
        for i, (host, user, password, database) in enumerate(successful_configs, 1):
            print(f"{i}. Host: {host}, User: {user}, Password: '{password}'")
        
        # Utiliser la première configuration réussie
        host, user, password, database = successful_configs[0]
        
        print(f"\n📝 Configuration recommandée:")
        print(f"   Host: {host}")
        print(f"   User: {user}")
        print(f"   Password: {password}")
        
        # Mettre à jour db_helper.py
        update_db_helper(host, user, password)
        
    else:
        print("❌ Aucune configuration MySQL trouvée")
        print("\n🔧 SOLUTIONS POSSIBLES:")
        print("1. Vérifiez que MySQL est démarré")
        print("2. Installez MySQL si ce n'est pas fait")
        print("3. Configurez un utilisateur MySQL avec les bonnes permissions")
        print("4. Utilisez MySQL Workbench pour vérifier vos paramètres")

def update_db_helper(host, user, password):
    """Met à jour le fichier db_helper.py avec la configuration trouvée"""
    try:
        with open("db_helper.py", 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remplacer les valeurs par défaut
        replacements = [
            ('"host": os.getenv("DB_HOST", "localhost")', f'"host": os.getenv("DB_HOST", "{host}")'),
            ('"user": os.getenv("DB_USER", "root")', f'"user": os.getenv("DB_USER", "{user}")'),
            ('"password": os.getenv("DB_PASSWORD", "root")', f'"password": os.getenv("DB_PASSWORD", "{password}")')
        ]
        
        for old, new in replacements:
            content = content.replace(old, new)
        
        with open("db_helper.py", 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"\n✅ Configuration mise à jour dans db_helper.py")
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")

if __name__ == "__main__":
    main()
