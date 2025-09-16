import csv
import time
import sys
import glob
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from bs4 import BeautifulSoup

# Fonction pour charger les variables d'environnement depuis le fichier .env
def load_env_file():
    env_vars = {}
    env_path = Path(__file__).parent.parent.parent / ".env"
    
    if env_path.exists():
        with open(env_path, "r") as env_file:
            for line in env_file:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()
    
    return env_vars

# Charger les variables d'environnement
env_vars = load_env_file()

# Ajouter le répertoire parent au path pour pouvoir importer les modules du projet
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Trouver le fichier de template HTML le plus récent
template_pattern = str(project_root / "output" / "email_template_*.html")
template_files = glob.glob(template_pattern)

if not template_files:
    raise FileNotFoundError("Aucun fichier de template trouvé dans le dossier output/")

# Prendre le fichier le plus récent
latest_template = max(template_files, key=os.path.getctime)

# Lire le template HTML
with open(latest_template, "r", encoding="utf-8") as file:
    html_template = file.read()

# Extraire le titre h1 du template HTML
soup = BeautifulSoup(html_template, 'html.parser')
header_div = soup.select_one('.header')
email_title = ""
if header_div:
    h1_tag = header_div.find('h1')
    if h1_tag:
        email_title = h1_tag.text.strip()

# Si pas trouvé dans le h1, essayer le titre du document
if not email_title:
    title_tag = soup.find('title')
    if title_tag:
        email_title = title_tag.text.strip()
    else:
        # Fallback sur le titre généré
        email_title = "Association Gamadji - Informations"

print(f"Titre extrait du template : {email_title}")

# Paramètres du serveur SMTP Gmail
SMTP_SERVER = env_vars.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(env_vars.get("SMTP_PORT", "587"))
EMAIL_SENDER = env_vars.get("EMAIL_SENDER", "")
EMAIL_PASSWORD = env_vars.get("EMAIL_PASSWORD", "")  # Mot de passe d'application

# Vérifier que les variables obligatoires sont définies
if not EMAIL_SENDER or not EMAIL_PASSWORD:
    raise ValueError("EMAIL_SENDER et EMAIL_PASSWORD doivent être définis dans le fichier .env")

# Fonction pour envoyer un email HTML
def send_html_email(recipient, subject, html_content):
    # Création du message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    # Ajouter uniquement le destinataire en Cci (Bcc)
    msg["Bcc"] = recipient
    
    # Créer la version texte et HTML du message
    text_part = MIMEText(
        "Ce message contient du contenu HTML. Si vous ne le voyez pas correctement, "
        "veuillez utiliser un client mail compatible HTML.", 
        "plain"
    )
    html_part = MIMEText(html_content, "html")
    
    # Attacher les deux versions
    msg.attach(text_part)
    msg.attach(html_part)
    
    # Connexion au serveur SMTP et envoi
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        # Pour sendmail, nous avons besoin d'un destinataire réel
        # même si dans les en-têtes du message il n'apparaît qu'en Bcc
        server.sendmail(EMAIL_SENDER, [recipient], msg.as_string())
        server.close()
        print(f"Email envoyé à {recipient}")
        return True
    except Exception as e:
        print(f"ERREUR: Impossible d'envoyer l'email à {recipient}. Erreur: {str(e)}")
        return False

# Chemin vers le fichier CSV des destinataires
destinataires_path = Path(__file__).parent / "destinataires.csv"

# lire le CSV et envoyer les emails
with open(destinataires_path, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        email = row["email"]
        nom = row["name"]
        
        # Envoyer l'email en utilisant le titre extrait du template
        send_html_email(email, email_title, html_template)
        
        # Pause pour éviter d'être considéré comme spammeur
        time.sleep(5)
        