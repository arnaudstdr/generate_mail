# Configuration Celery + Redis pour l'envoi asynchrone d'emails

## 🎯 Pourquoi Celery + Redis ?

Lorsque vous envoyez des emails à 200+ destinataires, le processus **bloque votre application** pendant plusieurs minutes (environ 17 minutes avec un délai de 5 secondes entre chaque email).

**Avec Celery + Redis**, l'envoi devient **asynchrone** :
- ✅ **Non bloquant** : vous continuez à utiliser votre application immédiatement
- ✅ **Traitement en arrière-plan** : les emails sont envoyés par un worker dédié
- ✅ **Monitoring** : suivez l'avancement en temps réel
- ✅ **Retry automatique** : en cas d'échec, les emails sont réessayés automatiquement
- ✅ **Rate limiting** : contrôle du débit pour éviter les problèmes avec les fournisseurs de messagerie

## 📋 Installation

### 1. Installer Redis

**Sur macOS :**
```bash
# Avec Homebrew
brew install redis

# Démarrer Redis
brew services start redis

# Ou manuellement
redis-server
```

**Sur Linux (Ubuntu/Debian) :**
```bash
# Installer Redis
sudo apt-get update
sudo apt-get install redis-server

# Démarrer Redis
sudo systemctl start redis
sudo systemctl enable redis  # Démarrage automatique

# Vérifier le statut
sudo systemctl status redis
```

**Sur Windows :**
```bash
# Télécharger Redis depuis https://github.com/microsoftarchive/redis/releases
# Ou utiliser WSL (Windows Subsystem for Linux)
```

### 2. Vérifier que Redis fonctionne

```bash
redis-cli ping
# Devrait répondre: PONG
```

### 3. Installer les dépendances Python

```bash
# Si vous utilisez l'environnement virtuel du projet
.venv/bin/pip install -r requirements.txt

# Ou avec pip global
pip install -r requirements.txt
```

Les dépendances installées :
- `celery>=5.3.0` - Framework de tâches asynchrones
- `redis>=5.0.0` - Client Python pour Redis
- `celery[redis]` - Support Redis pour Celery

## 🚀 Utilisation

### Étape 1 : Démarrer le worker Celery

Le worker Celery est un processus qui écoute les tâches et les exécute en arrière-plan.

**Option A - Mode normal (foreground, avec logs en temps réel) :**
```bash
./start_celery_worker.sh
# Choisir option 1
```

**Option B - Mode daemon (background, logs dans fichier) :**
```bash
./start_celery_worker.sh
# Choisir option 2
```

Le worker affichera :
```
🚀 DÉMARRAGE DU WORKER CELERY - ENVOI D'EMAILS ASYNCHRONE
==========================================================

🐍 Interpréteur Python: .venv/bin/python
🔍 Vérification de Redis...
✅ Redis est accessible
🔍 Vérification de Celery...
✅ Celery est installé

🎯 Configuration du worker:
   - Concurrence: 2 workers
   - Log level: INFO
   - Queues: email_queue, bulk_email_queue

🔄 Démarrage du worker en mode normal...
💡 Appuyez sur Ctrl+C pour arrêter

[2025-01-24 12:00:00,000: INFO/MainProcess] Connected to redis://localhost:6379/0
[2025-01-24 12:00:00,000: INFO/MainProcess] celery@hostname ready.
```

### Étape 2 : Lancer l'envoi asynchrone

Dans un **nouveau terminal** (ou en mode daemon pour le worker) :

```bash
python send_emails.py
```

Choisissez l'option **1) Envoi ASYNCHRONE** :

```
📧 ENVOI D'EMAILS - ASSOCIATION GAMADJI SARÉ
============================================================

Choisissez le mode d'envoi :

1) 🚀 Envoi ASYNCHRONE (recommandé)
   ✅ Non bloquant - vous pouvez continuer à travailler
   ✅ Traitement en arrière-plan avec Celery
   ✅ Idéal pour envoyer à de nombreux destinataires
   ⚠️  Nécessite Redis et le worker Celery actif

2) 💻 Envoi SYNCHRONE (classique)
   ⏳ Bloquant - attend la fin de tous les envois
   ⚠️  Peut prendre beaucoup de temps (200+ destinataires)
   ✅ Ne nécessite pas de configuration supplémentaire

Votre choix (1-2, défaut 1) : 1
```

Le script vérifie automatiquement :
- ✅ Celery et Redis installés
- ✅ Redis accessible
- ⚠️ Worker Celery actif

Résultat :
```
============================================================
✅ ENVOI PLANIFIÉ AVEC SUCCÈS!
============================================================
🆔 ID de la tâche: abc123-def456-ghi789

💡 Pour suivre l'avancement:
   python check_email_status.py abc123-def456-ghi789 --bulk

💡 Pour lister toutes les tâches actives:
   python check_email_status.py --list

⏳ Les emails sont envoyés en arrière-plan.
   Vous pouvez fermer cette fenêtre sans problème.
```

### Étape 3 : Suivre l'avancement

**Vérifier une tâche spécifique :**
```bash
python check_email_status.py abc123-def456-ghi789
```

**Vérifier un envoi en masse (avec détails) :**
```bash
python check_email_status.py abc123-def456-ghi789 --bulk
```

Affiche :
```
📊 VÉRIFICATION DE L'ENVOI EN MASSE: abc123-def456-ghi789
============================================================
État: SUCCESS
✅ Tâche terminée avec succès!

📧 Détails des envois individuels:
   Total: 200 emails

   ✅ Réussis: 198
   ❌ Échoués: 2
   ⏳ En attente/cours: 0
```

**Lister toutes les tâches actives :**
```bash
python check_email_status.py --list
```

## ⚙️ Configuration avancée

### Variables d'environnement (.env)

Ajoutez ces variables à votre fichier `.env` pour personnaliser Redis :

```bash
# Configuration Redis (optionnel - par défaut localhost)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

### Personnaliser le délai entre emails

```bash
python send_emails.py
# Choisir option 1
# Quand demandé, saisir le délai souhaité (en secondes)
```

Exemple : pour un délai de 3 secondes au lieu de 5 :
```
Délai entre chaque email en secondes (défaut: 5) : 3
```

### Ajuster la concurrence du worker

Éditez `scripts/email_sender/celery_config.py` :

```python
celery_app.conf.update(
    # ...
    worker_concurrency=4,  # Par défaut: 2 workers en parallèle
    # ...
)
```

⚠️ **Attention** : Plus de workers = plus d'emails en parallèle, mais risque d'être bloqué par votre fournisseur de messagerie pour spam.

## 🔧 Arrêter le worker Celery

**Mode foreground :**
```bash
# Dans le terminal du worker
Ctrl+C
```

**Mode daemon :**
```bash
# Trouver le PID
cat logs/celery_worker.pid

# Arrêter le worker
kill $(cat logs/celery_worker.pid)
```

## 📊 Architecture technique

```
┌─────────────────┐
│  send_emails.py │  ← Vous lancez cette commande
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ send_bulk_emails_   │  ← Crée une tâche dans Redis
│ async()             │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│      REDIS          │  ← File d'attente des tâches
│   (Message Broker)  │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Celery Worker      │  ← Traite les tâches en arrière-plan
│  (start_celery_     │
│   worker.sh)        │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  send_email_task()  │  ← Envoie chaque email individuellement
│  (pour chaque       │     avec retry automatique
│   destinataire)     │
└─────────────────────┘
```

## 🐛 Dépannage

### Redis ne démarre pas

**Erreur :** `Could not connect to Redis`

**Solution :**
```bash
# Vérifier que Redis est installé
redis-cli --version

# Démarrer Redis
redis-server

# Tester la connexion
redis-cli ping
```

### Le worker ne démarre pas

**Erreur :** `ImportError: No module named celery`

**Solution :**
```bash
# Réinstaller les dépendances
pip install -r requirements.txt

# Vérifier l'installation
python -c "import celery; print(celery.__version__)"
```

### Les emails ne sont pas envoyés

**Vérifications :**

1. **Redis est-il actif ?**
   ```bash
   redis-cli ping
   # Doit répondre: PONG
   ```

2. **Le worker est-il démarré ?**
   ```bash
   python check_email_status.py --list
   # Doit lister les workers actifs
   ```

3. **Les tâches sont-elles créées ?**
   ```bash
   python check_email_status.py <task_id>
   ```

4. **Vérifier les logs du worker**
   - Mode foreground : dans le terminal du worker
   - Mode daemon : `tail -f logs/celery_worker.log`

### Tâche bloquée en PENDING

**Cause :** Le worker n'est pas démarré ou ne peut pas se connecter à Redis.

**Solution :**
1. Vérifier que Redis est accessible
2. Redémarrer le worker Celery
3. Relancer l'envoi

## 📚 Ressources

- [Documentation Celery](https://docs.celeryq.dev/)
- [Documentation Redis](https://redis.io/docs/)
- [Guide des meilleures pratiques Celery](https://docs.celeryq.dev/en/stable/userguide/tasks.html#best-practices)

## 🆘 Support

Si vous rencontrez des problèmes :

1. ✅ Vérifiez que vous avez suivi toutes les étapes d'installation
2. 📋 Consultez la section Dépannage ci-dessus
3. 🔍 Vérifiez les logs du worker Celery
4. 📧 Contactez l'équipe avec les détails de l'erreur

---

**✨ Avec Celery + Redis, vous pouvez envoyer des milliers d'emails sans bloquer votre application !**
