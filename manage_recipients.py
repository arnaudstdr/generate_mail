#!/usr/bin/env python3
"""
Gestionnaire de destinataires pour l'envoi des templates email
Arnaud STADLER - Dev Python | 🌍 Association Gamadji Saré
"""

import sys
import os
import csv
from pathlib import Path

# Ajouter le dossier racine au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class RecipientManager:
    def __init__(self):
        self.csv_path = Path("scripts/email_sender/destinataires.csv")
        self.ensure_csv_exists()

    def ensure_csv_exists(self):
        """S'assure que le fichier CSV existe avec les en-têtes appropriés"""
        if not self.csv_path.exists():
            self.csv_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['name', 'email'])

    def load_recipients(self):
        """Charge la liste des destinataires depuis le fichier CSV"""
        recipients = []
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    recipients.append(row)
        except FileNotFoundError:
            print("Fichier destinataires.csv non trouvé")
        return recipients
    
    def save_recipients(self, recipients):
        """Sauvegarde la liste des destinataires dans le fichier CSV"""
        with open(self.csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['name', 'email'])
            writer.writeheader()
            writer.writerows(recipients)

    def display_recipients(self):
        """Affiche la liste actuelle des destinataires"""
        recipients = self.load_recipients()

        if not recipients:
            print("Aucun destinataire dans la liste")
            return
        
        print(f"\nListe des destinataires ({len(recipients)})")
        print("=" * 50)
        for i, recipient in enumerate(recipients, 1):
            print(f"{i:2d}. {recipient['name']} <{recipient['email']}>")
        print()

    def add_recipient(self):
        """Ajoute un nouveau destinataire"""
        print("\nAjouter un nouveau destinataire")
        print("=" * 35)

        name = input("Nom complet : ").strip()
        while not name:
            name = input("Le nom ne peut pas être vide. Nom complet : ").strip()

        email = input("Adresse email : ").strip()
        while not email or "@" not in email:
            email = input("Veuillez saisir une adresse email valide : ").strip()

        recipients = self.load_recipients()

        # Vérifier si l'email existe déjà
        for recipient in recipients:
            if recipient['email'].lower() == email.lower():
                print("L'email {email} existe déjà dans la liste")
                return
            
        recipients.append({'name': name, 'email': email})
        self.save_recipients(recipients)

        print(f"Destinataire ajouté : {name} <{email}>")

    def remove_recipient(self):
        """Supprime un destinataire"""
        recipients = self.load_recipients()

        if not recipients:
            print("Aucun destinataire à supprimer")
            return
        
        self.display_recipients()

        try:
            index = int(input("Numéro du destinataire à supprimer : ")) - 1
            if 0 <= index < len(recipients):
                removed = recipients.pop(index)
                self.save_recipients(recipients)
                print(f"Destinataire supprimé : {removed['name']} <{removed['email']}>")
            else:
                print("Numéro invalide")
        except ValueError:
            print("Veuillez saisir un numéro valide")

    def edit_recipient(self):
        """Modifie un destinataire existant"""
        recipients = self.load_recipients()

        if not recipients:
            print("Aucun destinataire à modifier")
            return
        
        self.display_recipients()

        try:
            index = int(input("Numéro du destinataire à modifier : ")) - 1
            if 0 <= index < len(recipients):
                recipient = recipients[index]
                print(f"\nModification de : {recipient['name']} <{recipient['email']}>")

                new_name = input(f"Nouveau nom (actuel: {recipient['name']}) : ").strip()
                if new_name:
                    recipient['name'] = new_name

                new_email = input(f"Nouvelle adresse email (actuelle : {recipient['email']}) : ").strip()
                if new_email and '@' in new_email:
                    # Vérifier si le nouvel email existe déjà
                    for i, other in enumerate(recipients):
                        if i != index and other['email'].lower() == new_email.lower():
                            print(f"L'email {new_email} existe déjà dans la liste")
                            return
                    recipient['email'] = new_email
                elif new_email:
                    print("Adresse email invalide, modification annulée")
                    return
                
                self.save_recipients(recipients)
                print(f"Destinataire modifié : {recipient['name']} <{recipient['email']}>")
            else:
                print("Numéro invalide")
        except ValueError:
            print("Veuillez saisir un numéro valide")
    
    def import_from_file(self):
        """Importe des destinataires depuis un autre fichier CSV"""
        file_path = input("Chemin du fichier CSV à importer : ").strip()

        if not os.path.exists(file_path):
            print("Fichier non trouvé")
            return
        
        try:
            imported_count = 0
            skipped_count = 0
            recipients = self.load_recipients()
            existing_emails = {r['email'].lower() for r in recipients}

            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if 'email' in row and 'name' in row:
                        email = row['email'].strip().lower()
                        if email and '@' in email and email not in existing_emails:
                            recipients.append({
                                'name': row['name'].strip(),
                                'email': email
                            })
                            existing_emails.add(email)
                            imported_count += 1
                        else:
                            skipped_count += 1
            
            self.save_recipients(recipients)
            print(f"{imported_count} destinataire(s) importé(s)")
            if skipped_count > 0:
                print(f"{skipped_count} destinataire(s) ignoré(s) (doublons ou emails invalides)")
        
        except Exception as e:
            print(f"Erreur lors de l'importation : {e}")

    def run_menu(self):
        """Lance le menu interactif de gestion des destinataires"""
        while True:
            print("\n" + "=" * 60)
            print("GESTIONNAIRE DE DESTINATAIRES")
            print("=" * 60)

            self.display_recipients()

            print("Actions disponibles :")
            print("1. Ajouter un destinataire")
            print("2. Modifier un destinataire")
            print("3. Supprimer un destinataire")
            print("4. Importer depuis un fichier CSV")
            print("5. Quitter")
            print()

            choice = input("Choix (1 - 5) : ").strip()

            if choice == '1':
                self.add_recipient()
            elif choice == '2':
                self.edit_recipient()
            elif choice == '3':
                self.remove_recipient()
            elif choice == '4':
                self.import_from_file()
            elif choice == '5':
                print("Au revoir!")
                break
            else:
                print("Choix invalide, veuillez recommencer")

if __name__ == "__main__":
    manager = RecipientManager()
    manager.run_menu()

