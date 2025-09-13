"""
Package scripts pour le générateur de templates email
Association Gamadji - Village en Afrique

Ce package contient tous les scripts et modules pour générer des templates HTML d'emails
avec support des médias Google Drive.

Modules disponibles :
- template_mail_generator : Script principal interactif
- utils : Utilitaires Google Drive  
- template_html : Générateur de templates HTML
- demo : Script de démonstration
- test_links : Testeur de liens Google Drive
"""

__version__ = "1.1.0"
__author__ = "Association Gamadji"

# Imports principaux pour faciliter l'utilisation
from .template_mail_generator import EmailTemplateGenerator
from .utils import GoogleDriveUtils
from .template_html import EmailTemplate
from .test_links import GoogleDriveTester

__all__ = [
    'EmailTemplateGenerator',
    'GoogleDriveUtils', 
    'EmailTemplate',
    'GoogleDriveTester'
]