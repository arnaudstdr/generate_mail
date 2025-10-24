#!/usr/bin/env python3
"""
Vérificateur de statut des tâches Celery
Association Gamadji Saré

Permet de suivre l'avancement des envois d'emails en arrière-plan.
"""

import sys
import os
import argparse
from pathlib import Path

# Ajouter le dossier racine au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def check_task_status(task_id):
    """Vérifie le statut d'une tâche Celery"""
    try:
        from scripts.email_sender.celery_config import celery_app
        from celery.result import AsyncResult
        
        print(f"🔍 VÉRIFICATION DU STATUT DE LA TÂCHE: {task_id}")
        print("=" * 60)
        
        result = AsyncResult(task_id, app=celery_app)
        
        print(f"État: {result.state}")
        
        if result.state == 'PENDING':
            print("⏳ Tâche en attente de traitement...")
        elif result.state == 'STARTED':
            print("🔄 Tâche en cours d'exécution...")
        elif result.state == 'SUCCESS':
            print("✅ Tâche terminée avec succès!")
            if result.result:
                print(f"\nRésultat:")
                print(result.result)
        elif result.state == 'FAILURE':
            print("❌ Tâche échouée!")
            print(f"Erreur: {result.info}")
        elif result.state == 'RETRY':
            print("🔄 Tâche en cours de nouvelle tentative...")
        else:
            print(f"ℹ️  État: {result.state}")
        
        # Afficher les infos supplémentaires si disponibles
        if result.info:
            print(f"\nInformations supplémentaires:")
            if isinstance(result.info, dict):
                for key, value in result.info.items():
                    print(f"  {key}: {value}")
        
        return result
        
    except ImportError as e:
        print("❌ Erreur: Celery ou Redis n'est pas installé/configuré")
        print(f"   {str(e)}")
        print("\n💡 Solutions:")
        print("   1. Installez les dépendances: pip install -r requirements.txt")
        print("   2. Démarrez Redis: redis-server")
        print("   3. Démarrez le worker Celery: ./start_celery_worker.sh")
        return None
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return None


def check_bulk_status(bulk_task_id):
    """Vérifie le statut d'une tâche d'envoi en masse"""
    print(f"📊 VÉRIFICATION DE L'ENVOI EN MASSE: {bulk_task_id}")
    print("=" * 60)
    
    result = check_task_status(bulk_task_id)
    
    if result and result.state == 'SUCCESS' and isinstance(result.result, dict):
        tasks = result.result.get('tasks', [])
        
        if tasks:
            print(f"\n📧 Détails des envois individuels:")
            print(f"   Total: {len(tasks)} emails")
            
            # Vérifier quelques tâches individuelles
            from scripts.email_sender.celery_config import celery_app
            from celery.result import AsyncResult
            
            success_count = 0
            failed_count = 0
            pending_count = 0
            
            for task_info in tasks:
                task_result = AsyncResult(task_info['task_id'], app=celery_app)
                
                if task_result.state == 'SUCCESS':
                    success_count += 1
                elif task_result.state == 'FAILURE':
                    failed_count += 1
                elif task_result.state in ['PENDING', 'STARTED', 'RETRY']:
                    pending_count += 1
            
            print(f"\n   ✅ Réussis: {success_count}")
            print(f"   ❌ Échoués: {failed_count}")
            print(f"   ⏳ En attente/cours: {pending_count}")


def list_active_tasks():
    """Liste toutes les tâches actives"""
    try:
        from scripts.email_sender.celery_config import celery_app
        
        print("📋 TÂCHES ACTIVES")
        print("=" * 60)
        
        # Obtenir les tâches actives
        inspect = celery_app.control.inspect()
        
        active = inspect.active()
        scheduled = inspect.scheduled()
        reserved = inspect.reserved()
        
        if active:
            print("\n🔄 Tâches en cours d'exécution:")
            for worker, tasks in active.items():
                print(f"\n  Worker: {worker}")
                for task in tasks:
                    print(f"    - {task['name']} (ID: {task['id'][:8]}...)")
        
        if scheduled:
            print("\n⏰ Tâches planifiées:")
            for worker, tasks in scheduled.items():
                print(f"\n  Worker: {worker}")
                for task in tasks:
                    print(f"    - {task['request']['name']} (ID: {task['request']['id'][:8]}...)")
        
        if reserved:
            print("\n📥 Tâches réservées:")
            for worker, tasks in reserved.items():
                print(f"\n  Worker: {worker}")
                for task in tasks:
                    print(f"    - {task['name']} (ID: {task['id'][:8]}...)")
        
        if not active and not scheduled and not reserved:
            print("ℹ️  Aucune tâche active")
            print("\n💡 Si vous attendez des envois:")
            print("   1. Vérifiez que le worker Celery est démarré")
            print("   2. Vérifiez que Redis est accessible")
            print("   3. Relancez l'envoi si nécessaire")
        
    except Exception as e:
        print(f"❌ Impossible de lister les tâches actives: {str(e)}")
        print("\n💡 Assurez-vous que:")
        print("   - Redis est démarré")
        print("   - Le worker Celery est actif")


def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(
        description="Vérifier le statut des tâches d'envoi d'emails Celery"
    )
    parser.add_argument(
        'task_id',
        nargs='?',
        help="ID de la tâche à vérifier (optionnel)"
    )
    parser.add_argument(
        '--list',
        '-l',
        action='store_true',
        help="Lister toutes les tâches actives"
    )
    parser.add_argument(
        '--bulk',
        '-b',
        action='store_true',
        help="Vérifier le statut détaillé d'un envoi en masse"
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_active_tasks()
    elif args.task_id:
        if args.bulk:
            check_bulk_status(args.task_id)
        else:
            check_task_status(args.task_id)
    else:
        print("📊 MONITEUR DE TÂCHES CELERY - ENVOI D'EMAILS")
        print("=" * 60)
        print("\nUtilisation:")
        print("  python check_email_status.py <task_id>        # Vérifier une tâche")
        print("  python check_email_status.py <task_id> --bulk # Envoi en masse détaillé")
        print("  python check_email_status.py --list           # Lister les tâches actives")
        print("\nExemples:")
        print("  python check_email_status.py abc123-def456-...")
        print("  python check_email_status.py --list")
        print()


if __name__ == "__main__":
    main()
