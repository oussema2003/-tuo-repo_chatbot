#!/usr/bin/env python3
"""
Script de test pour vérifier que le chatbot fonctionne avec la base de données
"""

import requests
import json

def test_chatbot():
    """Teste le chatbot avec des requêtes d'exemple"""
    print("🤖 TEST DU CHATBOT AVEC BASE DE DONNÉES")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Ajouter un article à la commande
    print("\n1. Test d'ajout d'article...")
    test_payload = {
        "queryResult": {
            "intent": {
                "displayName": "order.add"
            },
            "parameters": {
                "food-item": ["Pizza"],
                "number": [2]
            },
            "outputContexts": [
                {
                    "name": "projects/test/sessions/test-session/contexts/ongoing-order"
                }
            ]
        }
    }
    
    try:
        response = requests.post(f"{base_url}/", json=test_payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Réponse du chatbot: {result.get('fulfillmentText', 'Pas de texte')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au chatbot")
        print("Vérifiez que le serveur est démarré sur http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False
    
    # Test 2: Finaliser la commande
    print("\n2. Test de finalisation de commande...")
    complete_payload = {
        "queryResult": {
            "intent": {
                "displayName": "order.complete"
            },
            "parameters": {},
            "outputContexts": [
                {
                    "name": "projects/test/sessions/test-session/contexts/ongoing-order"
                }
            ]
        }
    }
    
    try:
        response = requests.post(f"{base_url}/", json=complete_payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Réponse du chatbot: {result.get('fulfillmentText', 'Pas de texte')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test de finalisation: {e}")
        return False
    
    # Test 3: Suivi de commande
    print("\n3. Test de suivi de commande...")
    track_payload = {
        "queryResult": {
            "intent": {
                "displayName": "track.order"
            },
            "parameters": {
                "order_id": 40
            },
            "outputContexts": [
                {
                    "name": "projects/test/sessions/test-session/contexts/ongoing-order"
                }
            ]
        }
    }
    
    try:
        response = requests.post(f"{base_url}/", json=track_payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Réponse du chatbot: {result.get('fulfillmentText', 'Pas de texte')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors du test de suivi: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 TOUS LES TESTS SONT PASSÉS!")
    print("Votre chatbot fonctionne correctement avec la base de données SQLite!")
    print("=" * 50)
    
    return True

def check_server_status():
    """Vérifie si le serveur est en cours d'exécution"""
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Fonction principale"""
    print("🔍 VÉRIFICATION DU STATUT DU SERVEUR")
    print("=" * 40)
    
    if check_server_status():
        print("✅ Serveur FastAPI démarré sur http://localhost:8000")
        print("📖 Documentation disponible sur http://localhost:8000/docs")
    else:
        print("❌ Serveur non accessible")
        print("Démarrez le serveur avec: uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        return False
    
    print("\n" + "=" * 40)
    
    # Tester le chatbot
    return test_chatbot()

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n🔧 SOLUTIONS:")
        print("1. Démarrez le serveur: uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        print("2. Vérifiez que la base de données SQLite est créée")
        print("3. Vérifiez les logs du serveur pour les erreurs")
        exit(1)
