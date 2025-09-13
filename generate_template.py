#!/usr/bin/env python3
"""
Point d'entrée principal pour le générateur de templates email
Association Gamadji - Village en Afrique
"""

import sys
import os

# Ajouter le dossier racine au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.template_mail_generator import EmailTemplateGenerator

if __name__ == "__main__":
    generator = EmailTemplateGenerator()
    generator.run()