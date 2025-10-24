"""
Configuration Celery pour l'envoi asynchrone d'emails
Association Gamadji Saré

Ce module configure Celery avec Redis comme broker et backend de résultats.
"""

from celery import Celery
import os
from pathlib import Path

# Charger les variables d'environnement
def load_env_file():
    env_vars = {}
    env_path = Path(__file__).parent.parent.parent / ".env"
    
    if env_path.exists():
        with open(env_path, "r") as env_file:
            for line in env_file:
                line = line.strip()
                if line and not line.startswith("#"):
                    if "=" in line:
                        key, value = line.split("=", 1)
                        env_vars[key.strip()] = value.strip()
    
    return env_vars

env_vars = load_env_file()

# URL de connexion Redis (depuis .env ou par défaut localhost)
REDIS_HOST = env_vars.get("REDIS_HOST", "localhost")
REDIS_PORT = env_vars.get("REDIS_PORT", "6379")
REDIS_DB = env_vars.get("REDIS_DB", "0")
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

# Créer l'instance Celery
celery_app = Celery(
    'email_sender',
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=['scripts.email_sender.tasks']
)

# Configuration Celery
celery_app.conf.update(
    # Timezone
    timezone='Europe/Paris',
    enable_utc=True,
    
    # Sérialisation
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    
    # Résultats
    result_expires=3600,  # Les résultats expirent après 1 heure
    result_persistent=True,
    
    # Rate limiting pour éviter le spam
    task_default_rate_limit='10/m',  # Maximum 10 tâches par minute
    
    # Retry policy
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    
    # Worker
    worker_prefetch_multiplier=1,  # Une tâche à la fois par worker
    worker_max_tasks_per_child=50,  # Redémarrer le worker après 50 tâches
    
    # Concurrence
    worker_concurrency=2,  # 2 workers en parallèle (ajustable)
    
    # Logging
    worker_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
    worker_task_log_format='[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s',
)

# Routes des tâches (optionnel, pour organisation future)
celery_app.conf.task_routes = {
    'scripts.email_sender.tasks.send_email_task': {'queue': 'email_queue'},
    'scripts.email_sender.tasks.send_bulk_emails_task': {'queue': 'bulk_email_queue'},
}

if __name__ == '__main__':
    celery_app.start()
