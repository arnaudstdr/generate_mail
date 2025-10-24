#!/usr/bin/env python3
"""
Point d'entrée pour l'envoi des templates email
Arnaud STADLER - Dev Python | 🌍 Association Gamadji Saré
"""

import sys
import os

# Ajouter le dossier racine au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scripts.email_sender.mail import EmailSender

def main():
    """Fonction principale avec choix du mode d'envoi"""
    print("📧 ENVOI D'EMAILS - ASSOCIATION GAMADJI SARÉ")
    print("=" * 60)
    print()
    print("Choisissez le mode d'envoi :")
    print()
    print("1) 🚀 Envoi ASYNCHRONE (recommandé)")
    print("   ✅ Non bloquant - vous pouvez continuer à travailler")
    print("   ✅ Traitement en arrière-plan avec Celery")
    print("   ✅ Idéal pour envoyer à de nombreux destinataires")
    print("   ⚠️  Nécessite Redis et le worker Celery actif")
    print()
    print("2) 💻 Envoi SYNCHRONE (classique)")
    print("   ⏳ Bloquant - attend la fin de tous les envois")
    print("   ⚠️  Peut prendre beaucoup de temps (200+ destinataires)")
    print("   ✅ Ne nécessite pas de configuration supplémentaire")
    print()
    
    choice = input("Votre choix (1-2, défaut 1) : ").strip()
    choice = choice if choice else "1"
    
    try:
        sender = EmailSender()
        
        if choice == "1":
            print()
            print("🚀 MODE ASYNCHRONE SÉLECTIONNÉ")
            print("-" * 60)
            
            # Vérifications préalables
            print("🔍 Vérifications préalables...")
            
            try:
                import celery
                import redis
                print("✅ Celery et Redis sont installés")
            except ImportError as e:
                print(f"❌ Dépendance manquante: {e}")
                print("💡 Installez les dépendances: pip install -r requirements.txt")
                return
            
            # Vérifier Redis
            try:
                import redis as redis_lib
                r = redis_lib.Redis(host='localhost', port=6379, db=0)
                r.ping()
                print("✅ Redis est accessible")
            except Exception:
                print("❌ Redis n'est pas accessible")
                print("💡 Démarrez Redis:")
                print("   - Sur macOS: brew services start redis")
                print("   - Sur Linux: sudo systemctl start redis")
                print("   - Manuellement: redis-server")
                return
            
            # Avertissement sur le worker
            print()
            print("⚠️  IMPORTANT: Le worker Celery doit être démarré pour traiter les emails")
            print()
            response = input("Le worker Celery est-il démarré? (o/n) : ").strip().lower()
            
            if response not in ['o', 'oui', 'y', 'yes']:
                print()
                print("💡 Pour démarrer le worker Celery:")
                print("   ./start_celery_worker.sh")
                print()
                print("   Dans un autre terminal, ou en mode daemon")
                return
            
            print()
            print("📬 Lancement de l'envoi asynchrone...")
            
            # Personnalisation du délai
            delay_input = input("Délai entre chaque email en secondes (défaut: 5) : ").strip()
            delay = int(delay_input) if delay_input.isdigit() else 5
            
            result = sender.send_bulk_emails_async(delay_between_emails=delay)
            
            if result.get('status') == 'scheduled':
                print()
                print("=" * 60)
                print("✅ ENVOI PLANIFIÉ AVEC SUCCÈS!")
                print("=" * 60)
                print(f"🆔 ID de la tâche: {result['task_id']}")
                print()
                print("💡 Pour suivre l'avancement:")
                print(f"   python check_email_status.py {result['task_id']} --bulk")
                print()
                print("💡 Pour lister toutes les tâches actives:")
                print("   python check_email_status.py --list")
                print()
                print("⏳ Les emails sont envoyés en arrière-plan.")
                print("   Vous pouvez fermer cette fenêtre sans problème.")
            else:
                print()
                print("❌ Erreur lors de la planification de l'envoi")
                print(f"   {result.get('message', 'Erreur inconnue')}")
        
        elif choice == "2":
            print()
            print("💻 MODE SYNCHRONE SÉLECTIONNÉ")
            print("-" * 60)
            print("⚠️  ATTENTION: Cette opération peut prendre beaucoup de temps")
            print("   et bloquera votre terminal jusqu'à la fin des envois.")
            print()
            
            response = input("Continuer avec le mode synchrone? (o/n) : ").strip().lower()
            
            if response in ['o', 'oui', 'y', 'yes']:
                print()
                print("📬 Démarrage de l'envoi synchrone...")
                print("⏳ Veuillez patienter...")
                print()
                sender.send_bulk_emails()
                print()
                print("=" * 60)
                print("✅ TOUS LES EMAILS ONT ÉTÉ ENVOYÉS!")
                print("=" * 60)
            else:
                print("❌ Envoi annulé")
        
        else:
            print("❌ Choix invalide. Veuillez choisir 1 ou 2.")
    
    except KeyboardInterrupt:
        print("\n\n❌ Envoi annulé par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}")

if __name__ == "__main__":
    main()