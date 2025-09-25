#!/bin/bash
# Script de lancement pour le générateur de templates email
# Association Gamadji

# Se placer dans le dossier du script pour garantir les chemins relatifs
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

echo "🎯 GÉNÉRATEUR DE TEMPLATES EMAIL - ASSOCIATION GAMADJI"
echo "====================================================="
echo ""

# Choix initial: Interface Graphique ou Terminal
echo "Souhaitez-vous utiliser l'interface graphique (GUI) ou rester dans le terminal ?"
echo ""
echo "1) 🖥️ Interface graphique (GUI)"
echo "2) 💻 Mode Terminal (menu texte)"
echo ""
read -p "Votre choix (1-2, défaut 2) : " mode_choice
mode_choice=${mode_choice:-2}

if [[ "$mode_choice" == "1" || "$mode_choice" == "G" || "$mode_choice" == "g" ]]; then
    echo ""
    echo "🖥️ Lancement de l'interface graphique..."
    echo ""
    # Vérifier la disponibilité de PyQt5 avant de lancer la GUI
    if $PYTHON -c "import PyQt5" >/dev/null 2>&1; then
        exec $PYTHON gui.py
    else
        echo "⚠️ PyQt5 n'est pas installé pour l'interpréteur: $PYTHON"
        echo "   Pour l'installer: $PYTHON -m pip install -r requirements.txt"
        echo "   Bascule en mode Terminal..."
        echo ""
    fi
fi

echo "Choisissez une option :"
echo ""
echo "1) 🚀 Lancer le générateur interactif complet"
echo "2) 📬 Envoyer les emails"
echo "3) 📮 Gérer les destinataires"
echo "4) 🎮 Voir la démonstration rapide"
echo "5) 🧪 Tester des liens Google Drive"
echo "6) 📚 Afficher l'aide"
echo "7) 🌐 Ouvrir le dernier template généré"
echo ""

read -p "Votre choix (1-7) : " choice

case $choice in
    1)
        echo ""
        echo "🚀 Lancement du générateur interactif..."
        echo ""
        $PYTHON generate_template.py
        ;;
    2)
        echo ""
        echo "📬 Lancement de l'envoi des emails..."
        echo ""
        $PYTHON send_emails.py
        ;;
    3)
        echo ""
        echo "📮 Gestion des destinataires..."
        echo ""
        $PYTHON manage_recipients.py
        ;;
    4)
        echo ""
        echo "🎮 Lancement de la démonstration..."
        echo ""
        $PYTHON run_demo.py
        ;;
    5)
        echo ""
        echo "🧪 Lancement du testeur de liens..."
        echo ""
        $PYTHON test_drive_links.py
        ;;
    6)
        echo ""
        echo "📚 AIDE - Générateur de Templates Email"
        echo "======================================"
        echo ""
        echo "Ce script génère des templates HTML pour des emails personnalisés."
        echo ""
        echo "Fonctionnalités :"
        echo "• Interface interactive pour saisir le contenu"
        echo "• Support des photos et vidéos Google Drive"
        echo "• Design responsive avec couleurs africaines"
        echo "• Maximum 10 photos et 10 vidéos par email"
        echo ""
        echo "Formats de liens Google Drive acceptés :"
        echo "• https://drive.google.com/file/d/XXXXXXX/view"
        echo "• https://drive.google.com/open?id=XXXXXXX"
        echo ""
        echo "⚠️  Important : Les fichiers doivent être partagés publiquement"
        echo ""
        echo "📁 Les templates HTML sont sauvegardés dans le dossier output/"
        echo ""
        ;;
    7)
        echo ""
        echo "🔍 Recherche du dernier template généré..."
        latest_file=$(ls -t output/*email_template*.html 2>/dev/null | head -n1)
        if [ -n "$latest_file" ]; then
            echo "🌐 Ouverture de : $latest_file"
            open "$latest_file"
        else
            echo "❌ Aucun template trouvé dans output/. Générez-en un d'abord !"
        fi
        ;;
    *)
        echo ""
        echo "❌ Choix invalide. Veuillez choisir 1, 2, 3, 4, 5 ou 6."
        ;;
esac

echo ""
echo "✨ Merci d'utiliser le générateur de templates email !"
echo "Arnaud STADLER - Dev Python | 🌍 Association Gamadji Saré"