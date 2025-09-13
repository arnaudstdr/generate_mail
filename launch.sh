#!/bin/bash
# Script de lancement pour le générateur de templates email
# Association Gamadji

echo "🎯 GÉNÉRATEUR DE TEMPLATES EMAIL - ASSOCIATION GAMADJI"
echo "====================================================="
echo ""
echo "Choisissez une option :"
echo ""
echo "1) 🚀 Lancer le générateur interactif complet"
echo "2) 🎮 Voir la démonstration rapide"
echo "3) 🧪 Tester des liens Google Drive"
echo "4) 📚 Afficher l'aide"
echo "5) 🌐 Ouvrir le dernier template généré"
echo ""

read -p "Votre choix (1-5) : " choice

case $choice in
    1)
        echo ""
        echo "🚀 Lancement du générateur interactif..."
        echo ""
        /Users/arnaudstadler/Documents/PROJETS/template_mail_gamadji/.venv/bin/python generate_template.py
        ;;
    2)
        echo ""
        echo "🎮 Lancement de la démonstration..."
        echo ""
        /Users/arnaudstadler/Documents/PROJETS/template_mail_gamadji/.venv/bin/python run_demo.py
        ;;
    3)
        echo ""
        echo "🧪 Lancement du testeur de liens..."
        echo ""
        /Users/arnaudstadler/Documents/PROJETS/template_mail_gamadji/.venv/bin/python test_drive_links.py
        ;;
    4)
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
    5)
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
        echo "❌ Choix invalide. Veuillez choisir 1, 2, 3, 4 ou 5."
        ;;
esac

echo ""
echo "✨ Merci d'utiliser le générateur de templates email !"
echo "🌍 Association Gamadji Saré"