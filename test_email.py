#!/usr/bin/env python3
"""
Script de test pour l'envoi d'un email avant l'envoi en masse
Arnaud STADLER - Dev Python | 🌍 Association Gamadji Saré
"""

import sys
import os
import argparse

# Ajouter le dossier racine au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scripts.email_sender.mail import EmailSender

def test_email_send(test_email=None):
    """
    Envoie un email de test à l'adresse spécifiée ou à l'adresse de l'expéditeur
    """
    print("📧 TEST D'ENVOI EMAIL - Association Gamadji")
    print("=" * 60)
    
    # Initialiser l'objet EmailSender
    sender = EmailSender()
    
    # Si aucune adresse de test n'est fournie, utiliser l'adresse de l'expéditeur
    if not test_email:
        test_email = sender.EMAIL_SENDER
        print(f"ℹ️ Aucune adresse de test spécifiée, utilisation de l'adresse d'envoi: {test_email}")
    
    print(f"📤 Envoi d'un email de test à: {test_email}")
    print(f"📑 Sujet: {sender.email_title}")
    
    # Trouver le dernier template généré
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
    template_files = [f for f in os.listdir(output_dir) if f.endswith('.html')]
    if template_files:
        latest_template = max(template_files, key=lambda f: os.path.getctime(os.path.join(output_dir, f)))
        print(f"🔍 Template utilisé: {latest_template}")
    
    # Modifier le sujet pour indiquer qu'il s'agit d'un test
    test_subject = f"[TEST] {sender.email_title}"
    
    # Tentative d'envoi
    print("\n⏳ Envoi en cours...")
    success = sender.send_html_email(test_email, subject=test_subject)
    
    if success:
        print("\n✅ TEST RÉUSSI!")
        print(f"📬 Email envoyé avec succès à {test_email}")
        print("\nContrôlez votre boîte de réception pour vérifier le rendu et le contenu de l'email.")
        print("Si tout vous convient, vous pouvez maintenant procéder à l'envoi en masse avec:")
        print("   python send_emails.py")
    else:
        print("\n❌ ÉCHEC DU TEST!")
        print("Vérifiez les paramètres de connexion SMTP dans le fichier .env")
        print("Assurez-vous que l'authentification à deux facteurs est activée sur votre compte Gmail")
        print("et que vous utilisez un mot de passe d'application valide.")

if __name__ == "__main__":
    # Mise en place des arguments en ligne de commande
    parser = argparse.ArgumentParser(description='Tester l\'envoi d\'email avant envoi en masse')
    parser.add_argument('--email', '-e', type=str, help='Adresse email de test (optionnel)')
    args = parser.parse_args()
    
    # Exécution du test
    test_email_send(args.email)