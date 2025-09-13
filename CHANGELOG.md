# Changelog - Générateur de Templates Email

## Version 1.1.1 - 13 septembre 2025

### 🗂️ Organisation des fichiers de sortie
- **📁 Dossier output/** : Tous les fichiers HTML générés sont maintenant sauvegardés dans `output/`
- **🔧 Scripts mis à jour** : `template_mail_generator.py`, `demo.py`, et `launch.sh` utilisent le nouveau dossier
- **📝 Documentation** : Ajout d'un README dans `output/` pour expliquer l'usage
- **🧹 .gitignore** : Le dossier `output/` est ignoré par Git (sauf le README)
- **📋 requirements.txt** : Ajout des dépendances du projet sans versions

### 🔧 Améliorations techniques
- **Création automatique** du dossier `output/` s'il n'existe pas
- **Recherche intelligente** du dernier fichier généré dans `launch.sh`
- **Structure plus propre** : séparation claire entre code source et fichiers générés

---

## Version 1.1.0 - 13 septembre 2025

### 🏗️ Restructuration majeure
- **📁 Reorganisation du code** : Tous les scripts Python déplacés dans `scripts/`
- **📦 Package Python** : `scripts/` devient un package avec `__init__.py`
- **🚀 Points d'entrée simplifiés** :
  - `generate_template.py` - Générateur principal
  - `run_demo.py` - Démonstration
  - `test_drive_links.py` - Test des liens
- **📧 Module d'envoi préparé** : `scripts/email_sender/` pour futures fonctionnalités

### 🔧 Améliorations techniques
- **Imports relatifs** : Correction de tous les imports dans les modules
- **Structure modulaire** : Facilite l'extension et la maintenance
- **Points d'entrée unifiés** : Scripts principaux à la racine
- **Préparation pour l'envoi** : Architecture prête pour les fonctionnalités d'email

### 📂 Nouvelle structure
```
├── scripts/                    # Package principal
│   ├── template_mail_generator.py
│   ├── utils.py
│   ├── template_html.py
│   ├── demo.py
│   ├── test_links.py
│   └── email_sender/          # Module d'envoi (futur)
├── generate_template.py       # Point d'entrée principal
├── run_demo.py               # Démonstration
├── test_drive_links.py       # Test des liens
└── launch.sh                 # Menu interactif
```

---

## Version 1.0.0 - 13 septembre 2025

### 🎯 Fonctionnalités initiales
- **Interface interactive** pour création de templates
- **Support Google Drive** pour photos et vidéos
- **Design responsive** avec palette africaine
- **Système de fallback** pour affichage des photos
- **Testeur de liens** Google Drive intégré
- **Génération HTML** optimisée pour email

### 🎨 Design
- **Couleurs africaines** : Ocre, brun sable, doré
- **Grille responsive** pour médias
- **Aperçus vidéo** avec miniatures
- **Effets visuels** et transitions

### 🔧 Outils
- **Validation de liens** Google Drive
- **URLs de fallback** multiples
- **Messages d'erreur informatifs**
- **Guide de dépannage** intégré

---

## Prochaines versions prévues

### Version 1.2.0 - Envoi d'emails
- Envoi via Gmail API
- Envoi via SMTP
- Services tiers (SendGrid, etc.)
- Gestion des listes de diffusion

### Version 1.3.0 - Fonctionnalités avancées
- Templates multiples
- Éditeur visuel
- Statistiques d'envoi
- Planification automatique