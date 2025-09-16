#!/usr/bin/env python3
"""
Point d'entrée pour l'envoi des templates email
Association Gamadji - Village en Afrique
"""

import sys
import os

# Ajouter le dossier racine au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scripts.email_sender.mail import EmailSender

if __name__ == "__main__":
    sender = EmailSender()
    sender.send_bulk_emails()