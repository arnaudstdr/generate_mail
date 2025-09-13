#!/usr/bin/env python3
"""
Point d'entrée pour la démonstration rapide
Association Gamadji - Village en Afrique
"""

import sys
import os

# Ajouter le dossier racine au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.demo import demo_rapide

if __name__ == "__main__":
    demo_rapide()