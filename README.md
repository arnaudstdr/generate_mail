# Générateur de Templates Email - Association Gamadji

[![Python version](https://img.shields.io/badge/python-%3E%3D3.8-blue)](https://www.python.org/downloads/)
[![Licence](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENCE)
[![Dernier commit](https://img.shields.io/github/last-commit/arnaudstdr/generate_mail/main)](https://github.com/arnaudstdr/generate_mail/commits/main)
[![Stars](https://img.shields.io/github/stars/arnaudstdr/generate_mail?style=social)](https://github.com/arnaudstdr/generate_mail/stargazers)

Un script Python pour générer des templates HTML d'emails personnalisés avec photos et vidéos depuis Google Drive.

## 🎯 Fonctionnalités

- **Interface graphique moderne** avec PyQt5 (✅ Nouveau)
- **Interface interactive en terminal** pour saisir le contenu
- **Système d'envoi d'emails complet** (✅ Nouveau)
- **Gestionnaire de destinataires intégré** (✅ Nouveau)
- **Design responsive** avec couleurs inspirées de l'Afrique
- **Support des médias Google Drive** (photos et vidéos)
- **Templates HTML optimisés** pour l'email
- **Aperçus vidéo** avec miniatures
- **Maximum 10 photos et 10 vidéos** par email
- **🧪 Testeur de liens** Google Drive intégré
- **🔄 URLs de fallback** pour améliorer l'affichage des photos
- **📧 Test d'envoi d'email** avant diffusion massive
- **📊 Gestion des destinataires** via fichier CSV

## 🚀 Installation

1. **Cloner ou télécharger le projet**
   ```bash
   git clone https://github.com/arnaudstdr/generate_mail.git
   cd generate_mail
   ```

2. **L'environnement Python est déjà configuré** avec les dépendances installées :
   - `requests` - pour les interactions avec Google Drive
   - `Pillow` - pour le traitement d'images
   - `PyQt5` - pour l'interface graphique ✅ Nouveau
   - `python-dotenv` - pour la gestion des variables d'environnement
   - `yagmail` - pour l'envoi d'emails simplifié ✅ Nouveau
   - `bs4` - pour le parsing HTML
   - `google-*` - pour les APIs Google Drive

3. **Configuration des variables d'environnement**
   - Créez un fichier `.env` à la racine du projet (voir [CONFIGURATION.md](./CONFIGURATION.md))
   - Ajoutez-y vos identifiants pour l'envoi d'emails et APIs Google ✅ Nouveau
   - Configurez vos paramètres SMTP selon votre fournisseur de messagerie

## 📋 Utilisation

### Menu de lancement rapide

```bash
./launch.sh
```

Au démarrage, choisissez le mode d'utilisation :
1. 🖥️ Interface graphique (GUI) — nécessite PyQt5
2. 💻 Mode Terminal (menu texte)

Options disponibles en mode Terminal :
1. **🚀 Lancer le générateur interactif complet**
2. **📬 Envoyer les emails** ✅ Nouveau
3. **📮 Gérer les destinataires** ✅ Nouveau
4. **🧪 Tester un email** ✅ Nouveau  
5. **🎮 Voir la démonstration rapide**
6. **🧪 Tester des liens Google Drive**
7. **📚 Afficher l'aide**
8. **🌐 Ouvrir le dernier template généré**

> Astuce: si PyQt5 n'est pas installé, le script bascule automatiquement en mode Terminal. Installez les dépendances avec:
> ```bash
> python -m pip install -r requirements.txt
> ```

### Lancement direct (nouvelle structure)

**Générateur principal :**
```bash
python generate_template.py
```

**Interface graphique :**
```bash
python gui.py
```

**Envoi d'emails :**
```bash
python send_emails.py
```

**Test d'un email :**
```bash
python test_email.py
```

**Démonstration :**
```bash
python run_demo.py
```

**Gestion des destinataires :**
```bash
python manage_recipients.py
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

# Interface graphique
.venv/bin/python gui.py

# Envoi d'emails
.venv/bin/python send_emails.py

# Gestion des destinataires
.venv/bin/python manage_recipients.py

# Test d'un email
.venv/bin/python test_email.py

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

## 🖥️ Interface graphique (PyQt5)

**Nouveau !** Une interface graphique moderne est maintenant disponible :

- 🎨 Interface utilisateur intuitive avec onglets
- 📋 Gestion des listes de photos et vidéos
- 👁️ Aperçu du template en temps réel
- 📧 Envoi d'emails intégré

**Lancement :**
```bash
python gui.py
```

L'interface inclut :
- **Générateur** : Création de templates avec interface visuelle
- **Envoi d'emails** : Choix du template, visualisation, et envoi
- **Gestion des destinataires** : Interface graphique pour gérer la liste des contacts ✅ Nouveau

## 📮 Gestion des destinataires

**Nouveau !** Un système complet de gestion des destinataires est maintenant disponible :

### Interface en ligne de commande

```bash
# Lancer le gestionnaire de destinataires
python manage_recipients.py
```

Le gestionnaire offre un menu interactif avec les fonctionnalités suivantes :

**Menu principal :**
- 🔍 **Affichage de la liste** : Visualisation de tous les destinataires avec numérotation
- ➕ **Ajouter un destinataire** : Saisie du nom et de l'email avec validation
- ✏️ **Modifier un destinataire** : Edition des informations existantes
- 🗑️ **Supprimer un destinataire** : Suppression sélective par numéro
- 📥 **Importer depuis un fichier CSV** : Import en masse depuis un autre fichier

**Fonctionnalités avancées :**
- ✅ Validation automatique des adresses email
- ✅ Détection et prévention des doublons
- ✅ Sauvegarde automatique au format CSV
- ✅ Interface intuitive avec navigation par numéros

### Interface graphique (PyQt5)

Dans l'interface graphique, un onglet dédié **"📮 Gestion des Destinataires"** propose :

**Fonctionnalités GUI :**
- 📋 **Tableau interactif** : Visualisation en colonnes (Nom | Email)
- ➕ **Bouton Ajouter** : Formulaires de saisie avec validation
- ✏️ **Bouton Modifier** : Edition directe des entrées sélectionnées
- 🗑️ **Bouton Supprimer** : Suppression avec confirmation
- 📥 **Bouton Importer** : Sélection de fichier CSV via explorateur

**Avantages de l'interface graphique :**
- 👁️ Visualisation claire en tableau
- 🖱️ Sélection intuitive par clic
- 📁 Sélecteur de fichiers intégré pour l'import
- ⚡ Mise à jour en temps réel de l'affichage

### Format du fichier CSV

Le fichier `scripts/email_sender/destinataires.csv` utilise le format suivant :

```csv
name,email
Jean Dupont,jean.dupont@exemple.com
Marie Martin,marie.martin@exemple.fr
Pierre Durand,pierre@association.org
```

**Structure :**
- **Header obligatoire** : `name,email`
- **Encodage** : UTF-8 pour les caractères spéciaux
- **Validation** : Les emails doivent contenir un `@`
- **Unicité** : Pas de doublons d'emails autorisés

### Import en masse

Pour importer des destinataires depuis un autre fichier :

**Depuis le terminal :**
1. Lancer `python manage_recipients.py`
2. Choisir option **"4. Importer depuis un fichier CSV"**
3. Saisir le chemin complet du fichier à importer

**Depuis l'interface graphique :**
1. Ouvrir l'onglet **"📮 Gestion des Destinataires"**
2. Cliquer sur **"📥 Importer"**
3. Sélectionner le fichier CSV via l'explorateur

**Fonctionnalités d'import :**
- ✅ Détection automatique des doublons
- ✅ Validation des emails lors de l'import
- ✅ Rapport détaillé (importés vs ignorés)
- ✅ Fusion avec la liste existante

## 📬 Envoi d'emails automatisé

**Nouveau !** Le système d'envoi d'emails est maintenant pleinement fonctionnel :

### Configuration
1. Créez un fichier `.env` avec vos paramètres SMTP (voir `CONFIGURATION.md`)
2. Ajoutez vos destinataires dans `scripts/email_sender/destinataires.csv` ou utilisez le gestionnaire de destinataires

### Utilisation
```bash
# Envoi en masse
python send_emails.py

# Test d'un seul email
python test_email.py votre.email@exemple.com
```

### Fonctionnalités d'envoi
- ✅ Support SMTP (Gmail, Outlook, serveurs personnalisés)
- ✅ Templates HTML avec images
- ✅ Liste de destinataires CSV avec gestionnaire intégré
- ✅ Logs d'envoi détaillés
- ✅ Test avant envoi en masse

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
│   └── 📁 email_sender/            # Module d'envoi d'emails ✅ IMPLÉMENTÉ
│       ├── __init__.py             # Classes d'envoi email
│       ├── mail.py                 # Module d'envoi principal
│       └── destinataires.csv       # Liste des destinataires
├── 📄 generate_template.py          # Point d'entrée principal
├── 📄 gui.py                        # Interface graphique (PyQt5) ✅ NOUVEAU
├── 📄 send_emails.py                # Point d'entrée envoi d'emails ✅ NOUVEAU
├── 📄 manage_recipients.py          # Gestionnaire de destinataires ✅ NOUVEAU
├── 📄 test_email.py                 # Test d'envoi d'un email ✅ NOUVEAU
├── 📄 run_demo.py                   # Lancement démo
├── 📄 test_drive_links.py           # Test des liens
├── 📄 launch.sh                     # Menu de lancement (GUI ou Terminal)
├── 📁 output/                       # Fichiers HTML générés
├── 📁 .venv/                        # Environnement Python
├── 📄 README.md                     # Documentation
├── 📄 requirements.txt              # Dépendances Python
├── 📄 CONFIGURATION.md              # Guide de configuration ✅ NOUVEAU
├── 📄 DEPANNAGE_PHOTOS.md          # Guide dépannage
├── 📄 CHANGELOG.md                  # Journal des modifications ✅ NOUVEAU
├── 📄 LICENCE                       # Licence du projet
├── 📄 logo.png                      # Logo de l'association ✅ NOUVEAU
├── 📄 logo_base64.txt               # Logo encodé en base64 ✅ NOUVEAU
└── 📄 .gitignore                    # Fichiers à ignorer (Git)
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

### 📧 Améliorations du module d'envoi (✅ Base implémentée)
Le module d'envoi est fonctionnel et peut être enrichi avec :

- **Envoi via Gmail API** - Configuration OAuth2
- **Envoi via SMTP** - Serveurs email personnalisés  


### 🔮 Fonctionnalités futures
- **Templates multiples** - Choix de designs et layouts
- **Intégration API Google Drive** - Synchronisation automatique
- **Gestion avancée des destinataires** - Segmentation et listes dynamiques
- **Analytics avancées** - Tableaux de bord et rapports
- **Multi-langues** - Support international

### 🏗️ Architecture et développement
La structure modulaire facilite :
- ✅ Interface graphique PyQt5 implémentée
- ✅ Module d'envoi d'emails opérationnel
- ✅ Tests unitaires de base
- ✅ Documentation complète
- 🔄 API REST pour intégrations externes
- 🔄 Docker pour déploiement simplifié
- 🔄 CI/CD avec GitHub Actions

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