# Générateur de Templates Email - Association Gamadji

[![Python version](https://img.shields.io/badge/python-%3E%3D3.8-blue)](https://www.python.org/downloads/)
[![Licence](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENCE)
[![Dernier commit](https://img.shields.io/github/last-commit/arnaudstdr/generate_mail/main)](https://github.com/arnaudstdr/generate_mail/commits/main)
[![Stars](https://img.shields.io/github/stars/arnaudstdr/generate_mail?style=social)](https://github.com/arnaudstdr/generate_mail/stargazers)

Un script Python pour générer des templates HTML d'emails personnalisés avec photos et vidéos depuis Google Drive.

## 🎯 Fonctionnalités

- **Interface interactive** pour saisir le contenu
- **Design responsive** avec couleurs inspirées de l'Afrique
- **Support des médias Google Drive** (photos et vidéos)
- **Templates HTML optimisés** pour l'email
- **Aperçus vidéo** avec miniatures
- **Maximum 10 photos et 10 vidéos** par email
- **🧪 Testeur de liens** Google Drive intégré
- **🔄 URLs de fallback** pour améliorer l'affichage des photos

## 🚀 Installation

1. **Cloner ou télécharger le projet**
   ```bash
   git clone https://github.com/arnaudstdr/generate_mail.git
   cd generate_mail
   ```

2. **L'environnement Python est déjà configuré** avec les dépendances installées :
   - `requests` - pour les interactions avec Google Drive
   - `Pillow` - pour le traitement d'images (si nécessaire)

3. **Configuration des variables d'environnement**
   - Créez un fichier `.env` à la racine du projet (voir [CONFIGURATION.md](./CONFIGURATION.md))
   - Ajoutez-y vos identifiants pour l'envoi d'emails

## 📋 Utilisation

### Menu de lancement rapide

```bash
./launch.sh
```

Options disponibles :
1. **🚀 Générateur interactif complet**
2. **🎮 Démonstration rapide**
3. **🧪 Testeur de liens Google Drive** *(Nouveau !)*
4. **📚 Aide**
5. **🌐 Ouvrir le dernier template**

### Lancement direct (nouvelle structure)

**Générateur principal :**
```bash
python generate_template.py
```

**Démonstration :**
```bash
python run_demo.py
```

**Testeur de liens :**
```bash
python test_drive_links.py
```

### Utilisation avec l'environnement virtuel

Si vous préférez utiliser explicitement l'environnement virtuel :

```bash
# Générateur principal
.venv/bin/python generate_template.py

# Démonstration  
.venv/bin/python run_demo.py

# Testeur de liens
.venv/bin/python test_drive_links.py
```

## 🧪 Testeur de liens Google Drive

**Nouveau !** Avant de créer votre template, testez vos liens Google Drive :

- ✅ Valide les liens Google Drive
- 🔍 Teste différentes URLs d'affichage
- 📊 Affiche les résultats de compatibilité
- 💡 Recommande les meilleures URLs

**Utilisation :**
```bash
python test_drive_links.py
```

Collez vos liens un par un pour voir lesquels fonctionnent le mieux.

### Interface interactive

Le script vous guide à travers les étapes suivantes :

1. **📧 Objet du mail** : Saisissez l'objet (qui sera aussi le titre de l'email)

2. **📝 Texte de l'email** : 
   - Saisissez votre texte ligne par ligne
   - Appuyez sur Entrée deux fois pour terminer
   - Les sauts de ligne sont préservés

3. **📷 Photos** (maximum 10) :
   - Collez les liens de partage Google Drive
   - Un lien par ligne
   - Ligne vide pour terminer

4. **🎥 Vidéos** (maximum 10) :
   - Collez les liens de partage Google Drive
   - Un lien par ligne
   - Ligne vide pour terminer

### Formats de liens Google Drive acceptés

- `https://drive.google.com/file/d/XXXXXXX/view`
- `https://drive.google.com/open?id=XXXXXXX`
- `https://docs.google.com/.../d/XXXXXXX/...`

⚠️ **Important** : Les fichiers doivent être partagés publiquement pour être accessibles dans l'email.

## 📁 Fichiers générés

- **Nom automatique** : `email_template_YYYYMMDD_HHMMSS.html`
- **Emplacement** : Dossier `output/` (créé automatiquement)
- **Option d'ouverture** automatique dans le navigateur

## 🎨 Design

Le template utilise :
- **Design responsive** s'adaptant aux mobiles
- **Grille flexible** pour les médias
- **Effets visuels** (ombres, transitions)
- **Aperçus vidéo** avec bouton de lecture

## 📂 Structure du projet

```
template_mail_gamadji/
├── 📁 scripts/                      # Scripts Python organisés
│   ├── __init__.py                  # Package principal
│   ├── template_mail_generator.py   # Générateur principal
│   ├── utils.py                     # Utilitaires Google Drive
│   ├── template_html.py             # Templates HTML
│   ├── demo.py                      # Démonstration
│   ├── test_links.py               # Testeur de liens
│   └── 📁 email_sender/            # Module d'envoi (futur)
│       └── __init__.py             # Classes d'envoi email
├── 📄 generate_template.py          # Point d'entrée principal
├── 📄 run_demo.py                   # Lancement démo
├── 📄 test_drive_links.py           # Test des liens
├── 📄 launch.sh                     # Menu de lancement
├── 📁 output/                       # Fichiers HTML générés
├── 📁 .venv/                        # Environnement Python
├── 📄 README.md                     # Documentation
├── 📄 requirements.txt              # Dépendances Python
├── 📄 .gitignore                    # Fichiers à ignorer (Git)
└── 📄 DEPANNAGE_PHOTOS.md          # Guide dépannage
```

## 🔧 Fonctions principales

### 📁 Package `scripts/`

**GoogleDriveUtils** (`scripts/utils.py`)
- Validation des liens Google Drive
- Extraction des IDs de fichiers
- Génération d'URLs directes et miniatures
- Test d'accessibilité des liens

**EmailTemplate** (`scripts/template_html.py`)
- Génération du CSS responsive
- Création des grilles de médias
- Formatage du texte avec préservation des sauts de ligne
- Assembly du template final

**EmailTemplateGenerator** (`scripts/template_mail_generator.py`)
- Interface utilisateur interactive
- Orchestration du processus complet
- Sauvegarde des fichiers HTML

## 🎯 Exemple d'utilisation

```
=== GÉNÉRATEUR DE TEMPLATE EMAIL - ASSOCIATION GAMADJI ===

📧 Objet du mail : Nouvelles du village - Septembre 2025

📝 Texte de l'email :
Chers amis et soutiens,

Nous sommes heureux de partager avec vous les dernières nouvelles
de notre village et les progrès de nos projets.

📷 Photos (maximum 10) :
Photo 1 : https://drive.google.com/file/d/1ABC.../view
Photo 2 : https://drive.google.com/file/d/2DEF.../view
[ligne vide pour terminer]

🎥 Vidéos (maximum 10) :
Vidéo 1 : https://drive.google.com/file/d/3GHI.../view
[ligne vide pour terminer]

✅ Template généré avec succès !
📁 Fichier sauvegardé : email_template_20250913_143022.html
```

## 🔧 Résolution des problèmes photos

### ✅ Photos qui ne s'affichent pas

Le script utilise maintenant **plusieurs URLs de fallback** pour maximiser les chances d'affichage :

1. **URL thumbnail haute résolution** (principale)
2. **URL export classique** (fallback 1)
3. **URL thumbnail alternative** (fallback 2)
4. **Message d'erreur informatif** (dernier recours)

### 🧪 Diagnostic avec le testeur

Si vos photos ne s'affichent toujours pas :

1. **Lancez le testeur** : `python test_links.py`
2. **Collez vos liens** Google Drive
3. **Analysez les résultats** : le script teste 4 URLs différentes
4. **Vérifiez les permissions** si aucune URL ne fonctionne

### 📋 Checklist pour les photos

- ✅ Le fichier est partagé **"Accessible à tous ceux qui ont le lien"**
- ✅ Le lien est au format Google Drive valide
- ✅ Le fichier n'est pas dans un dossier privé
- ✅ Vous avez testé le lien avec le testeur intégré

## ⚠️ Notes importantes

1. **Partage public** : Les fichiers Google Drive doivent être partagés en lecture pour tous
2. **Taille des médias** : Les photos sont affichées en taille réelle (avec optimisation)
3. **Compatibilité email** : Le HTML généré est optimisé pour les clients email
4. **Responsive** : Le design s'adapte automatiquement aux écrans mobiles

## 🚧 Prochaines étapes

### 📧 Module d'envoi d'emails (en préparation)
Le dossier `scripts/email_sender/` est déjà préparé pour accueillir les fonctionnalités d'envoi :

- **Envoi via Gmail API** - Configuration OAuth2
- **Envoi via SMTP** - Serveurs email personnalisés  
- **Services tiers** - SendGrid, Mailgun, etc.
- **Listes de diffusion** - Gestion des destinataires
- **Tracking des envois** - Suivi des emails envoyés
- **Templates de relance** - Emails de suivi automatiques

### 🔮 Fonctionnalités futures
- Templates multiples au choix
- Intégration API Google Drive avancée
- Éditeur de templates visuel
- Planification d'envois
- Statistiques et analytics

### 🏗️ Architecture extensible
La nouvelle structure modulaire facilite :
- ✅ Ajout de nouveaux scripts
- ✅ Développement en équipe
- ✅ Tests unitaires
- ✅ Maintenance du code
- ✅ Réutilisation des composants

## 🆘 Dépannage

### Liens Google Drive non reconnus
- Vérifiez que le lien est un lien de partage Google Drive
- Assurez-vous que le fichier est partagé publiquement

### Images qui ne s'affichent pas
- Vérifiez les permissions de partage du fichier
- Testez le lien dans un navigateur en mode navigation privée

### Erreurs de génération
- Vérifiez que l'environnement Python est activé
- Assurez-vous que toutes les dépendances sont installées