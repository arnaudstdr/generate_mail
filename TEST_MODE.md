# Guide de Test du Système d'Envoi Asynchrone

## 🎯 Objectif

Ce guide explique comment tester le système d'envoi asynchrone d'emails avec Celery et Redis **sans envoyer de vrais emails** à vos destinataires.

## 🧪 Qu'est-ce que le mode TEST ?

Le mode TEST (ou **dry-run**) simule entièrement le processus d'envoi d'emails sans réellement envoyer de messages. C'est parfait pour :

- ✅ Vérifier que Redis fonctionne correctement
- ✅ Vérifier que le worker Celery traite les tâches
- ✅ Tester la configuration sans risque
- ✅ Valider le flux complet avant un envoi réel
- ✅ Éviter d'envoyer accidentellement des emails de test aux 200 destinataires

## 🚀 Prérequis

Avant de lancer un test, assurez-vous que :

1. **Redis est installé et démarré**
   ```bash
   # Vérifier si Redis fonctionne
   redis-cli ping
   # Doit répondre: PONG
   ```

2. **Les dépendances Python sont installées**
   ```bash
   pip install -r requirements.txt
   ```

3. **Le worker Celery est démarré** (dans un terminal séparé)
   ```bash
   ./start_celery_worker.sh
   ```

## 📋 Méthodes de Test

### Méthode 1 : Via send_emails.py (Recommandée)

C'est la méthode la plus simple et interactive.

**Étapes :**

1. **Démarrer le worker Celery** (Terminal 1)
   ```bash
   ./start_celery_worker.sh
   # Choisir option 1 (mode normal)
   ```

2. **Lancer l'envoi** (Terminal 2)
   ```bash
   python send_emails.py
   ```

3. **Choisir l'option de test**
   ```
   Votre choix (1-3, défaut 1) : 2
   ```
   
   Option 2 = 🧪 TEST ASYNCHRONE (simulation)

4. **Configurer le test**
   ```
   Le worker Celery est-il démarré? (o/n) : o
   
   Limiter le nombre de destinataires? 
   (laissez vide pour tous, ou entrez un nombre) : 5
   
   Délai entre chaque email en secondes (défaut: 1 pour test) : 1
   ```

5. **Le test se lance !**
   ```
   ============================================================
   ✅ TEST PLANIFIÉ AVEC SUCCÈS!
   ============================================================
   🆔 ID de la tâche: abc123-def456-ghi789
   📊 Limitation: 5 destinataires
   
   💡 Pour suivre l'avancement du test:
      python check_email_status.py abc123-def456-ghi789 --bulk
   ```

### Méthode 2 : Via test_celery_async.py (Script dédié)

Pour les tests rapides et automatisés.

**Syntaxe de base :**
```bash
python test_celery_async.py [OPTIONS]
```

**Options disponibles :**

| Option | Description | Défaut |
|--------|-------------|--------|
| `--limit` ou `-l` | Nombre de destinataires à tester | 5 |
| `--delay` ou `-d` | Délai entre chaque email (secondes) | 1 |

**Exemples d'utilisation :**

```bash
# Test basique avec 5 destinataires
python test_celery_async.py

# Test avec 10 destinataires
python test_celery_async.py --limit 10

# Test avec 3 destinataires et 2 secondes de délai
python test_celery_async.py -l 3 -d 2

# Test rapide avec tous les destinataires et 0.5 seconde de délai
python test_celery_async.py --limit 200 --delay 0.5
```

**Flux d'exécution :**

```
🧪 TEST DU SYSTÈME D'ENVOI ASYNCHRONE
============================================================

Configuration du test:
  - Destinataires: 5
  - Délai: 1 seconde(s)
  - Mode: DRY-RUN (simulation)

🔍 Vérifications préalables...
✅ Celery et Redis sont installés
✅ Redis est accessible

⚠️  IMPORTANT: Le worker Celery doit être démarré
💡 Si ce n'est pas le cas, lancez dans un autre terminal:
   ./start_celery_worker.sh

Continuer le test? (o/n) : o

🚀 Lancement du test...
------------------------------------------------------------

============================================================
✅ TEST LANCÉ AVEC SUCCÈS!
============================================================
🆔 ID de la tâche: abc123-def456
📊 5 tâches de test créées

💡 Pour suivre l'avancement:
   python check_email_status.py abc123-def456 --bulk
```

## 📊 Surveiller le Test

### Option 1 : Logs du Worker Celery

Dans le terminal où vous avez lancé le worker, vous verrez :

```
[2025-10-24 12:00:00] 🧪 [TEST] Simulation d'envoi à Jean Dupont <jean@example.com>...
[2025-10-24 12:00:00] ✅ [TEST] Envoi simulé avec succès à Jean Dupont

[2025-10-24 12:00:01] 🧪 [TEST] Simulation d'envoi à Marie Martin <marie@example.com>...
[2025-10-24 12:00:01] ✅ [TEST] Envoi simulé avec succès à Marie Martin

[2025-10-24 12:00:02] 🧪 [TEST] Simulation d'envoi à Pierre Durand <pierre@example.com>...
[2025-10-24 12:00:02] ✅ [TEST] Envoi simulé avec succès à Pierre Durand
```

**Points à noter :**
- Les messages contiennent `[TEST]` pour indiquer qu'il s'agit d'une simulation
- Chaque envoi prend environ 0.5 seconde (au lieu de 5+ secondes en mode réel)
- Aucun serveur SMTP n'est contacté

### Option 2 : Vérification de l'état d'une tâche

```bash
# Vérifier le statut d'une tâche spécifique
python check_email_status.py <task_id>
```

**Exemple de résultat :**
```
🔍 VÉRIFICATION DU STATUT DE LA TÂCHE: abc123-def456
============================================================
État: SUCCESS
✅ Tâche terminée avec succès!

Résultat:
{
  'status': 'success',
  'recipient': 'jean@example.com',
  'name': 'Jean Dupont',
  'task_id': 'xyz789',
  'dry_run': True,
  'message': 'Envoi simulé (dry-run mode)'
}
```

### Option 3 : Vérification détaillée d'un envoi en masse

```bash
# Vérifier tous les sous-envois d'une tâche d'envoi en masse
python check_email_status.py <task_id> --bulk
```

**Exemple de résultat :**
```
📊 VÉRIFICATION DE L'ENVOI EN MASSE: abc123-def456
============================================================
État: SUCCESS
✅ Tâche terminée avec succès!

📧 Détails des envois individuels:
   Total: 5 emails

   ✅ Réussis: 5
   ❌ Échoués: 0
   ⏳ En attente/cours: 0
```

### Option 4 : Lister toutes les tâches actives

```bash
python check_email_status.py --list
```

**Exemple de résultat :**
```
📋 TÂCHES ACTIVES
============================================================

🔄 Tâches en cours d'exécution:
  Worker: celery@MacBook-Pro.local
    - send_email_task (ID: abc12345...)
    - send_email_task (ID: def67890...)

⏰ Tâches planifiées:
  Worker: celery@MacBook-Pro.local
    - send_email_task (ID: ghi11121...)
    - send_email_task (ID: jkl31415...)
```

## 🔍 Comprendre le Fonctionnement Technique

### Architecture du Mode Test

```
┌─────────────────────┐
│  send_emails.py     │  ← Vous choisissez "Test Asynchrone"
│  ou                 │     avec dry_run=True et limit=5
│  test_celery_async  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ send_bulk_emails_   │  ← Crée 5 tâches dans Redis
│ async(dry_run=True, │     avec le flag dry_run activé
│       limit=5)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│      REDIS          │  ← File d'attente des tâches
│  (Message Broker)   │     avec paramètres de test
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Celery Worker      │  ← Récupère les tâches et
│  (détecte dry_run)  │     détecte le mode test
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  send_email_task()  │  ← Pour chaque destinataire :
│  if dry_run:        │     • Affiche "[TEST]"
│    simulate()       │     • Attend 0.5 seconde
│  else:              │     • Retourne succès
│    send_real()      │     • N'envoie RIEN par SMTP
└─────────────────────┘
```

### Différences entre Mode Test et Mode Réel

| Aspect | Mode TEST | Mode RÉEL |
|--------|-----------|-----------|
| Emails envoyés | ❌ Non | ✅ Oui |
| Connexion SMTP | ❌ Non | ✅ Oui |
| Durée par email | ~0.5 sec | ~5+ sec |
| Logs | `[TEST]` messages | Logs normaux |
| Résultat retourné | `dry_run: True` | `dry_run: False` ou absent |
| Risque | ✅ Aucun | ⚠️ Envois réels |

### Code Technique (Simplifié)

**Dans tasks.py :**
```python
def send_email_task(self, recipient_email, recipient_name, dry_run=False):
    if dry_run:
        # MODE TEST
        print(f"🧪 [TEST] Simulation d'envoi à {recipient_name}...")
        time.sleep(0.5)  # Simuler un délai
        print(f"✅ [TEST] Envoi simulé avec succès")
        return {
            'status': 'success',
            'dry_run': True,
            'message': 'Envoi simulé (dry-run mode)'
        }
    else:
        # MODE RÉEL
        sender = EmailSender()
        success = sender.send_html_email(recipient_email)
        return {'status': 'success' if success else 'failed'}
```

## 🎓 Scénarios de Test Recommandés

### Scénario 1 : Test Rapide (Première fois)

```bash
# Test avec seulement 3 destinataires
python test_celery_async.py --limit 3 --delay 1
```

**Objectif :** Vérifier que toute la chaîne fonctionne
**Durée :** ~3 secondes
**Vérifications :** Redis accessible, Worker actif, Tâches traitées

### Scénario 2 : Test Moyen (Avant envoi réel)

```bash
# Test avec 20 destinataires
python test_celery_async.py --limit 20 --delay 1
```

**Objectif :** Simuler un envoi plus conséquent
**Durée :** ~20 secondes
**Vérifications :** Performance du système, Pas d'erreurs

### Scénario 3 : Test Complet (Validation finale)

```bash
# Test avec tous les destinataires (200+)
python test_celery_async.py --limit 200 --delay 0.5
```

**Objectif :** Tester avec le volume réel mais rapidement
**Durée :** ~100 secondes (vs 17 minutes en mode réel)
**Vérifications :** Capacité du système, Stabilité

### Scénario 4 : Test de Charge

```bash
# Test avec délai minimal pour vérifier la performance
python test_celery_async.py --limit 50 --delay 0
```

**Objectif :** Tester la capacité maximale du système
**Durée :** Quelques secondes
**Vérifications :** Le worker peut-il gérer une charge élevée ?

## ✅ Checklist de Validation

Avant de lancer un envoi réel, vérifiez que :

- [ ] **Test basique réussi** (3-5 destinataires)
  ```bash
  python test_celery_async.py --limit 5
  ```

- [ ] **Tous les envois simulés sont réussis**
  ```bash
  python check_email_status.py <task_id> --bulk
  # Vérifier: ✅ Réussis: 5, ❌ Échoués: 0
  ```

- [ ] **Le worker traite les tâches sans erreur**
  - Pas de messages d'erreur dans les logs
  - Tous les messages `[TEST]` sont suivis de `✅`

- [ ] **Redis fonctionne correctement**
  ```bash
  redis-cli ping
  # Doit répondre: PONG
  ```

- [ ] **Le template HTML existe**
  - Vérifier qu'un fichier existe dans `output/`
  - Le template contient le bon contenu

- [ ] **Les destinataires sont corrects**
  - Vérifier `scripts/email_sender/destinataires.csv`
  - Pas de doublons, emails valides

## 🐛 Résolution des Problèmes

### Problème : "Redis n'est pas accessible"

**Cause :** Redis n'est pas démarré

**Solution :**
```bash
# Sur macOS
brew services start redis

# Sur Linux
sudo systemctl start redis

# Manuellement
redis-server
```

### Problème : "Le worker ne traite pas les tâches"

**Cause :** Le worker Celery n'est pas démarré ou ne peut pas se connecter

**Solution :**
```bash
# Vérifier si le worker est actif
python check_email_status.py --list

# Redémarrer le worker
./start_celery_worker.sh
```

### Problème : "Tâche bloquée en PENDING"

**Cause :** Le worker n'a pas reçu la tâche ou ne peut pas la traiter

**Solution :**
1. Vérifier que Redis fonctionne : `redis-cli ping`
2. Redémarrer le worker Celery
3. Vérifier les logs du worker pour des erreurs

### Problème : "ImportError: No module named celery"

**Cause :** Dépendances Python non installées

**Solution :**
```bash
pip install -r requirements.txt
```

## 💡 Conseils et Bonnes Pratiques

1. **Testez toujours avant un envoi réel**
   - Lancez au minimum un test avec 5 destinataires
   - Vérifiez les logs du worker

2. **Utilisez des limites pendant les tests**
   - Inutile de tester avec les 200 destinataires à chaque fois
   - 5-10 destinataires suffisent pour valider

3. **Surveillez les logs du worker**
   - C'est là que vous verrez les messages `[TEST]`
   - Permet de détecter rapidement les problèmes

4. **Gardez le worker en mode foreground pendant les tests**
   - Plus facile de voir les logs en temps réel
   - Passez en mode daemon seulement pour la production

5. **Notez l'ID de la tâche**
   - Permet de vérifier le statut plus tard
   - Utile pour le débogage

## 📚 Résumé des Commandes

```bash
# Démarrer le worker (Terminal 1)
./start_celery_worker.sh

# Test rapide (Terminal 2)
python test_celery_async.py --limit 5

# Test via interface interactive
python send_emails.py
# Choisir option 2

# Vérifier le statut
python check_email_status.py <task_id> --bulk

# Lister les tâches actives
python check_email_status.py --list
```

## 🎯 Conclusion

Le mode test vous permet de valider **en toute sécurité** que votre système d'envoi asynchrone fonctionne correctement avant de lancer un envoi réel à vos 200 destinataires.

**Workflow recommandé :**
1. Test avec 5 destinataires → Vérification du système
2. Test avec 20 destinataires → Vérification de la performance
3. Envoi réel avec confiance ! 🚀

Pour plus d'informations sur l'installation et la configuration, consultez [CELERY_SETUP.md](./CELERY_SETUP.md).
