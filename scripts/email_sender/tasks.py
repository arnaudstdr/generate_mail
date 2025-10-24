"""
Tâches Celery pour l'envoi asynchrone d'emails
Association Gamadji Saré

Ce module définit les tâches asynchrones pour l'envoi d'emails.
"""

import csv
import time
import sys
from pathlib import Path
from typing import Optional

from .celery_config import celery_app

# Ajouter le répertoire parent au path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


@celery_app.task(
    bind=True,
    name='scripts.email_sender.tasks.send_email_task',
    max_retries=3,
    default_retry_delay=60,  # Réessayer après 1 minute
)
def send_email_task(self, recipient_email: str, recipient_name: str, 
                    template_path: Optional[str] = None, 
                    subject: Optional[str] = None,
                    dry_run: bool = False):
    """
    Tâche Celery pour envoyer un email à un destinataire.
    
    Args:
        self: Instance de la tâche Celery (bind=True)
        recipient_email: Adresse email du destinataire
        recipient_name: Nom du destinataire
        template_path: Chemin vers le template HTML (optionnel)
        subject: Sujet de l'email (optionnel)
        dry_run: Si True, simule l'envoi sans envoyer réellement (défaut: False)
    
    Returns:
        dict: Résultat de l'envoi avec statut et informations
    """
    try:
        # Import local pour éviter les problèmes de circular imports
        from .mail import EmailSender
        
        if dry_run:
            print(f"🧪 [TEST] Simulation d'envoi à {recipient_name} <{recipient_email}>...")
            # Simuler un délai d'envoi (rapide pour les tests)
            import time
            time.sleep(0.5)
            print(f"✅ [TEST] Envoi simulé avec succès à {recipient_name}")
            return {
                'status': 'success',
                'recipient': recipient_email,
                'name': recipient_name,
                'task_id': self.request.id,
                'dry_run': True,
                'message': 'Envoi simulé (dry-run mode)'
            }
        
        print(f"📧 Envoi de l'email à {recipient_name} <{recipient_email}>...")
        
        # Créer une instance d'EmailSender
        sender = EmailSender()
        
        # Charger un template spécifique si fourni
        if template_path and Path(template_path).exists():
            with open(template_path, "r", encoding="utf-8") as f:
                html_content = f.read()
        else:
            html_content = sender.html_template
        
        # Envoyer l'email
        success = sender.send_html_email(
            recipient=recipient_email,
            subject=subject,
            html_content=html_content
        )
        
        if success:
            print(f"✅ Email envoyé avec succès à {recipient_name}")
            return {
                'status': 'success',
                'recipient': recipient_email,
                'name': recipient_name,
                'task_id': self.request.id
            }
        else:
            raise Exception("Échec de l'envoi de l'email")
            
    except Exception as exc:
        print(f"❌ Erreur lors de l'envoi à {recipient_name}: {str(exc)}")
        
        # Réessayer en cas d'échec
        if self.request.retries < self.max_retries:
            print(f"🔄 Nouvelle tentative ({self.request.retries + 1}/{self.max_retries})...")
            raise self.retry(exc=exc)
        
        # Échec définitif après toutes les tentatives
        return {
            'status': 'failed',
            'recipient': recipient_email,
            'name': recipient_name,
            'error': str(exc),
            'task_id': self.request.id
        }


@celery_app.task(
    bind=True,
    name='scripts.email_sender.tasks.send_bulk_emails_task'
)
def send_bulk_emails_task(self, csv_path: Optional[str] = None, 
                          template_path: Optional[str] = None,
                          delay_between_emails: int = 5,
                          dry_run: bool = False,
                          limit: Optional[int] = None):
    """
    Tâche Celery pour orchestrer l'envoi en masse d'emails.
    Cette tâche crée des sous-tâches pour chaque destinataire.
    
    Args:
        self: Instance de la tâche Celery (bind=True)
        csv_path: Chemin vers le fichier CSV des destinataires (optionnel)
        template_path: Chemin vers le template HTML (optionnel)
        delay_between_emails: Délai en secondes entre chaque email (défaut: 5)
        dry_run: Si True, simule l'envoi sans envoyer réellement (défaut: False)
        limit: Limite le nombre de destinataires (pour les tests, optionnel)
    
    Returns:
        dict: Résumé de l'envoi en masse avec liste des tâches créées
    """
    try:
        # Import local
        from .mail import EmailSender
        
        print("📬 Démarrage de l'envoi en masse asynchrone...")
        
        # Déterminer le chemin du CSV
        if not csv_path:
            csv_path = Path(__file__).parent / "destinataires.csv"
        else:
            csv_path = Path(csv_path)
        
        if not csv_path.exists():
            raise FileNotFoundError(f"Fichier CSV non trouvé: {csv_path}")
        
        # Lire les destinataires
        destinataires = []
        with open(csv_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if 'email' in row and 'name' in row:
                    destinataires.append({
                        'email': row['email'],
                        'name': row['name']
                    })
        
        # Limiter le nombre de destinataires si demandé (pour les tests)
        if limit and limit > 0:
            destinataires = destinataires[:limit]
            print(f"🧪 Mode test: limitation à {len(destinataires)} destinataires")
        
        print(f"📊 {len(destinataires)} destinataires {'(simulation)' if dry_run else ''}")
        
        if dry_run:
            print("🧪 MODE TEST ACTIVÉ - Aucun email ne sera réellement envoyé")
        
        # Créer une tâche pour chaque destinataire avec délai progressif
        task_ids = []
        for i, destinataire in enumerate(destinataires):
            # Appliquer un délai progressif (countdown en secondes)
            countdown = i * delay_between_emails
            
            task = send_email_task.apply_async(
                args=[
                    destinataire['email'],
                    destinataire['name'],
                    template_path,
                    None,  # subject
                    dry_run  # dry_run parameter
                ],
                countdown=countdown
            )
            
            task_ids.append({
                'task_id': task.id,
                'recipient': destinataire['email'],
                'name': destinataire['name'],
                'scheduled_delay': countdown,
                'dry_run': dry_run
            })
        
        mode_text = "simulées" if dry_run else "créées et planifiées"
        print(f"✅ {len(task_ids)} tâches d'envoi {mode_text}")
        
        return {
            'status': 'scheduled',
            'total_emails': len(destinataires),
            'tasks': task_ids,
            'bulk_task_id': self.request.id,
            'message': f"{len(task_ids)} emails planifiés pour envoi asynchrone"
        }
        
    except Exception as exc:
        print(f"❌ Erreur lors de la planification de l'envoi en masse: {str(exc)}")
        return {
            'status': 'failed',
            'error': str(exc),
            'bulk_task_id': self.request.id
        }


@celery_app.task(name='scripts.email_sender.tasks.get_task_status')
def get_task_status(task_id: str):
    """
    Récupère le statut d'une tâche d'envoi.
    
    Args:
        task_id: ID de la tâche Celery
    
    Returns:
        dict: État et résultat de la tâche
    """
    from celery.result import AsyncResult
    
    result = AsyncResult(task_id, app=celery_app)
    
    return {
        'task_id': task_id,
        'state': result.state,
        'info': result.info if result.info else {},
        'ready': result.ready(),
        'successful': result.successful() if result.ready() else None,
        'failed': result.failed() if result.ready() else None
    }
