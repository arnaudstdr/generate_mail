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


class EmailSender:
    def __init__(self):
        # Charger les variables d'environnement
        self.env_vars = self.load_env_file()

        # Ajouter le répertoire parent au path pour pouvoir importer les modules du projet
        self.project_root = Path(__file__).parent.parent.parent
        sys.path.append(str(self.project_root))

        # Trouver le fichier de template HTML le plus récent
        template_pattern = str(self.project_root / "output" / "email_template_*.html")
        template_files = glob.glob(template_pattern)

        if not template_files:
            raise FileNotFoundError("Aucun fichier de template trouvé dans le dossier output/")

        # Prendre le fichier le plus récent
        latest_template = max(template_files, key=os.path.getctime)

        # Lire le template HTML
        with open(latest_template, "r", encoding="utf-8") as file:
            self.html_template = file.read()

        # Extraire le titre h1 du template HTML
        soup = BeautifulSoup(self.html_template, 'html.parser')
        header_div = soup.select_one('.header')
        self.email_title = ""
        if header_div:
            h1_tag = header_div.find('h1')
            if h1_tag:
                self.email_title = h1_tag.text.strip()

        # Si pas trouvé dans le h1, essayer le titre du document
        if not self.email_title:
            title_tag = soup.find('title')
            if title_tag:
                self.email_title = title_tag.text.strip()
            else:
                # Fallback sur le titre généré
                self.email_title = "Association Gamadji - Informations"

        print(f"Titre extrait du template : {self.email_title}")

        # Paramètres du serveur SMTP Gmail
        self.SMTP_SERVER = self.env_vars.get("SMTP_SERVER", "smtp.gmail.com")
        self.SMTP_PORT = int(self.env_vars.get("SMTP_PORT", "587"))
        self.EMAIL_SENDER = self.env_vars.get("EMAIL_SENDER", "")
        self.EMAIL_PASSWORD = self.env_vars.get("EMAIL_PASSWORD", "")  # Mot de passe d'application

        # Vérifier que les variables obligatoires sont définies
        if not self.EMAIL_SENDER or not self.EMAIL_PASSWORD:
            raise ValueError("EMAIL_SENDER et EMAIL_PASSWORD doivent être définis dans le fichier .env")
            
        # Chemin vers le fichier CSV des destinataires
        self.destinataires_path = Path(__file__).parent / "destinataires.csv"
    
    # Fonction pour charger les variables d'environnement depuis le fichier .env
    def load_env_file(self):
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

    # Fonction pour envoyer un email HTML
    def send_html_email(self, recipient, subject=None, html_content=None):
        if subject is None:
            subject = self.email_title
        
        if html_content is None:
            html_content = self.html_template
            
        # Création du message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.EMAIL_SENDER
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
            server = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
            server.ehlo()
            server.starttls()
            server.login(self.EMAIL_SENDER, self.EMAIL_PASSWORD)
            # Pour sendmail, nous avons besoin d'un destinataire réel
            # même si dans les en-têtes du message il n'apparaît qu'en Bcc
            server.sendmail(self.EMAIL_SENDER, [recipient], msg.as_string())
            server.close()
            print(f"Email envoyé à {recipient}")
            return True
        except Exception as e:
            print(f"ERREUR: Impossible d'envoyer l'email à {recipient}. Erreur: {str(e)}")
            return False
    
    # Méthode pour envoyer des emails à tous les destinataires du fichier CSV
    def send_bulk_emails(self):
        # lire le CSV et envoyer les emails
        with open(self.destinataires_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                email = row["email"]
                nom = row["name"]
                
                # Envoyer l'email en utilisant le titre extrait du template
                self.send_html_email(email)
                
                # Pause pour éviter d'être considéré comme spammeur
                time.sleep(5)

if __name__ == "__main__":
    sender = EmailSender()
    sender.send_bulk_emails()
        