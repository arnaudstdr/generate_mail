#!/usr/bin/env python3
"""
Point d'entrée pour le testeur de liens Google Drive
Association Gamadji - Village en Afrique
"""

import sys
import os

# Ajouter le dossier racine au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.test_links import GoogleDriveTester

if __name__ == "__main__":
    tester = GoogleDriveTester()
    tester.interactive_test()