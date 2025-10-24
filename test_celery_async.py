#!/usr/bin/env python3
"""
Script de test rapide pour l'envoi asynchrone d'emails
Association Gamadji Saré

Ce script permet de tester rapidement le système Celery + Redis
sans envoyer de vrais emails.
"""

import sys
import os
import argparse

# Ajouter le dossier racine au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scripts.email_sender.mail import EmailSender


def test_async_system(limit=5, delay=1):
    """
    Teste le système d'envoi asynchrone en mode dry-run.
    
    Args:
        limit: Nombre de destinataires à tester (défaut: 5)
        delay: Délai entre chaque email en secondes (défaut: 1)
    """
    print("🧪 TEST DU SYSTÈME D'ENVOI ASYNCHRONE")
    print("=" * 60)
    print()
    print(f"Configuration du test:")
    print(f"  - Destinataires: {limit}")
    print(f"  - Délai: {delay} seconde(s)")
    print(f"  - Mode: DRY-RUN (simulation)")
    print()
    
    # Vérifications préalables
    print("🔍 Vérifications préalables...")
    
    try:
        import celery
        import redis
        print("✅ Celery et Redis sont installés")
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("💡 Installez les dépendances: pip install -r requirements.txt")
        return False
    
    # Vérifier Redis
    try:
        import redis as redis_lib
        r = redis_lib.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("✅ Redis est accessible")
    except Exception as e:
        print(f"❌ Redis n'est pas accessible: {e}")
        print("💡 Démarrez Redis:")
        print("   - Sur macOS: brew services start redis")
        print("   - Sur Linux: sudo systemctl start redis")
        print("   - Manuellement: redis-server")
        return False
    
    # Vérifier le worker Celery
    print()
    print("⚠️  IMPORTANT: Le worker Celery doit être démarré")
    print("💡 Si ce n'est pas le cas, lancez dans un autre terminal:")
    print("   ./start_celery_worker.sh")
    print()
    
    response = input("Continuer le test? (o/n) : ").strip().lower()
    if response not in ['o', 'oui', 'y', 'yes']:
        print("❌ Test annulé")
        return False
    
    print()
    print("🚀 Lancement du test...")
    print("-" * 60)
    
    try:
        # Créer l'instance EmailSender
        sender = EmailSender()
        
        # Lancer le test asynchrone
        result = sender.send_bulk_emails_async(
            delay_between_emails=delay,
            dry_run=True,
            limit=limit
        )
        
        if result.get('status') == 'scheduled':
            print()
            print("=" * 60)
            print("✅ TEST LANCÉ AVEC SUCCÈS!")
            print("=" * 60)
            print(f"🆔 ID de la tâche: {result['task_id']}")
            print(f"📊 {limit} tâches de test créées")
            print()
            print("💡 Pour suivre l'avancement:")
            print(f"   python check_email_status.py {result['task_id']} --bulk")
            print()
            print("💡 Pour lister toutes les tâches actives:")
            print("   python check_email_status.py --list")
            print()
            print("🧪 Surveillez les logs du worker Celery pour voir:")
            print("   - Les tâches qui s'exécutent")
            print("   - Les messages '[TEST] Simulation d'envoi...'")
            print("   - Les messages '[TEST] Envoi simulé avec succès'")
            print()
            print(f"⏱️  Temps estimé: ~{limit * delay} secondes")
            print()
            return True
        else:
            print()
            print("❌ Erreur lors du lancement du test")
            print(f"   {result.get('message', 'Erreur inconnue')}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False


def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(
        description="Tester le système d'envoi asynchrone sans envoyer de vrais emails"
    )
    parser.add_argument(
        '--limit',
        '-l',
        type=int,
        default=5,
        help="Nombre de destinataires à tester (défaut: 5)"
    )
    parser.add_argument(
        '--delay',
        '-d',
        type=int,
        default=1,
        help="Délai entre chaque email en secondes (défaut: 1)"
    )
    
    args = parser.parse_args()
    
    # Valider les arguments
    if args.limit < 1:
        print("❌ Le nombre de destinataires doit être au moins 1")
        return
    
    if args.delay < 0:
        print("❌ Le délai ne peut pas être négatif")
        return
    
    # Lancer le test
    success = test_async_system(limit=args.limit, delay=args.delay)
    
    if success:
        print("✨ Test terminé avec succès!")
        print()
        print("💡 Prochaines étapes:")
        print("   1. Vérifiez les logs du worker Celery")
        print("   2. Utilisez check_email_status.py pour vérifier les résultats")
        print("   3. Si tout fonctionne, lancez l'envoi réel avec send_emails.py")
    else:
        print("❌ Le test a échoué")
        print()
        print("💡 Consultez CELERY_SETUP.md pour plus d'informations")


if __name__ == "__main__":
    main()
