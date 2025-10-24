#!/bin/bash
# Script de démarrage du worker Celery pour l'envoi asynchrone d'emails
# Association Gamadji Saré

echo "🚀 DÉMARRAGE DU WORKER CELERY - ENVOI D'EMAILS ASYNCHRONE"
echo "=========================================================="
echo ""

# Se placer dans le dossier racine du projet
cd "$(cd "$(dirname "$0")" && pwd)" || exit 1

# Détecter l'interpréteur Python
if [ -x ".venv/bin/python" ]; then
    PYTHON=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON="python"
else
    echo "❌ Aucun interpréteur Python trouvé. Veuillez installer Python 3."
    exit 1
fi

echo "🐍 Interpréteur Python: $PYTHON"

# Vérifier que Redis est accessible
echo "🔍 Vérification de Redis..."
if command -v redis-cli >/dev/null 2>&1; then
    if redis-cli ping > /dev/null 2>&1; then
        echo "✅ Redis est accessible"
    else
        echo "⚠️  Redis ne répond pas. Assurez-vous qu'il est démarré:"
        echo "   - Sur macOS: brew services start redis"
        echo "   - Sur Linux: sudo systemctl start redis"
        echo "   - Manuellement: redis-server"
        echo ""
        read -p "Continuer quand même? (o/n) " choice
        if [[ "$choice" != "o" && "$choice" != "O" ]]; then
            exit 1
        fi
    fi
else
    echo "⚠️  redis-cli non trouvé. Redis est-il installé?"
    echo "   - Sur macOS: brew install redis"
    echo "   - Sur Linux: sudo apt-get install redis-server"
    echo ""
fi

# Vérifier que Celery est installé
echo "🔍 Vérification de Celery..."
if ! $PYTHON -c "import celery" 2>/dev/null; then
    echo "❌ Celery n'est pas installé."
    echo "💡 Installation: $PYTHON -m pip install -r requirements.txt"
    exit 1
fi
echo "✅ Celery est installé"

echo ""
echo "🎯 Configuration du worker:"
echo "   - Concurrence: 2 workers"
echo "   - Log level: INFO"
echo "   - Queues: email_queue, bulk_email_queue"
echo ""

# Options du worker
echo "📋 Choisissez le mode de lancement:"
echo "1) Mode normal (foreground, avec logs)"
echo "2) Mode daemon (background, logs dans fichier)"
echo ""
read -p "Votre choix (1-2, défaut 1): " mode_choice
mode_choice=${mode_choice:-1}

if [[ "$mode_choice" == "2" ]]; then
    # Mode daemon avec logs dans fichier
    echo "🔄 Démarrage du worker en mode daemon..."
    
    # Créer le dossier de logs s'il n'existe pas
    mkdir -p logs
    
    LOGFILE="logs/celery_worker.log"
    PIDFILE="logs/celery_worker.pid"
    
    $PYTHON -m celery -A scripts.email_sender.celery_config worker \
        --loglevel=INFO \
        --concurrency=2 \
        --logfile="$LOGFILE" \
        --pidfile="$PIDFILE" \
        --detach
    
    echo "✅ Worker démarré en arrière-plan"
    echo "📄 Logs: $LOGFILE"
    echo "🆔 PID: $PIDFILE"
    echo ""
    echo "💡 Pour arrêter le worker:"
    echo "   kill \$(cat $PIDFILE)"
    echo ""
    echo "💡 Pour voir les logs en temps réel:"
    echo "   tail -f $LOGFILE"
else
    # Mode normal (foreground)
    echo "🔄 Démarrage du worker en mode normal..."
    echo "💡 Appuyez sur Ctrl+C pour arrêter"
    echo ""
    
    $PYTHON -m celery -A scripts.email_sender.celery_config worker \
        --loglevel=INFO \
        --concurrency=2 \
        --queues=email_queue,bulk_email_queue
fi
