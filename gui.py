import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox,
    QListWidget, QInputDialog, QTabWidget, QFileDialog, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from datetime import datetime
from scripts.template_mail_generator import EmailTemplateGenerator
from scripts.email_sender.mail import EmailSender


class EmailGeneratorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Générateur d'Emails - Association Gamadji")
        self.setMinimumWidth(1000)
        self.setMinimumHeight(700)
        
        self.image_links = []
        self.video_links = []
        self.template_generator = EmailTemplateGenerator()

        # Initialiser le gestionnaire de destinataires
        from manage_recipients import RecipientManager
        self.recipients_manager = RecipientManager()
        
        # Widget central avec onglets
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Création des onglets
        tabs = QTabWidget()
        tabs.addTab(self.create_generator_tab(), "🔨 Générateur de Template")
        tabs.addTab(self.create_sender_tab(), "📧 Envoi d'Emails")
        tabs.addTab(self.create_recipient_tab(), "📮 Gestion des Destinataires")
        main_layout.addWidget(tabs)
    
    def create_generator_tab(self):
        """Crée l'onglet de génération de template"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Layout horizontal pour le contenu et les listes de liens
        content_layout = QHBoxLayout()
        
        # Section gauche (titre et contenu)
        left_layout = QVBoxLayout()
        
        # Titre
        title_label = QLabel("📧 Objet du mail :")
        self.title_input = QLineEdit()
        left_layout.addWidget(title_label)
        left_layout.addWidget(self.title_input)
        
        # Zone de texte principal
        content_label = QLabel("📝 Contenu du mail :")
        self.content_text = QTextEdit()
        left_layout.addWidget(content_label)
        left_layout.addWidget(self.content_text)
        
        content_layout.addLayout(left_layout)
        
        # Section droite (liens médias)
        right_layout = QVBoxLayout()
        
        # Section Images
        images_label = QLabel("🖼️ Liens des images Google Drive :")
        self.images_list = QListWidget()
        add_image_btn = QPushButton("➕ Ajouter un lien d'image")
        add_image_btn.clicked.connect(lambda: self.add_drive_link("image"))
        remove_image_btn = QPushButton("❌ Supprimer le lien d'image sélectionné")
        remove_image_btn.clicked.connect(lambda: self.remove_link("image"))
        
        right_layout.addWidget(images_label)
        right_layout.addWidget(self.images_list)
        right_layout.addWidget(add_image_btn)
        right_layout.addWidget(remove_image_btn)
        
        # Section Vidéos
        videos_label = QLabel("🎥 Liens des vidéos Google Drive :")
        self.videos_list = QListWidget()
        add_video_btn = QPushButton("➕ Ajouter un lien vidéo")
        add_video_btn.clicked.connect(lambda: self.add_drive_link("video"))
        remove_video_btn = QPushButton("❌ Supprimer le lien vidéo sélectionné")
        remove_video_btn.clicked.connect(lambda: self.remove_link("video"))
        
        right_layout.addWidget(videos_label)
        right_layout.addWidget(self.videos_list)
        right_layout.addWidget(add_video_btn)
        right_layout.addWidget(remove_video_btn)
        
        content_layout.addLayout(right_layout)
        layout.addLayout(content_layout)
        
        # Bouton de génération
        generate_btn = QPushButton("🚀 Générer le template")
        generate_btn.clicked.connect(self.generate_template)
        layout.addWidget(generate_btn)
        
        return tab
    
    def create_sender_tab(self):
        """Crée l'onglet d'envoi d'emails"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Sélection du template
        template_layout = QHBoxLayout()
        template_label = QLabel("📄 Template HTML :")
        self.template_combo = QComboBox()
        self.refresh_templates_btn = QPushButton("🔄 Rafraîchir")
        self.refresh_templates_btn.clicked.connect(self.refresh_templates)
        
        template_layout.addWidget(template_label)
        template_layout.addWidget(self.template_combo)
        template_layout.addWidget(self.refresh_templates_btn)
        layout.addLayout(template_layout)
        
        # Aperçu du template
        preview_btn = QPushButton("👁️ Aperçu du template")
        preview_btn.clicked.connect(self.preview_template)
        layout.addWidget(preview_btn)
        
        # Bouton d'envoi
        send_btn = QPushButton("📨 Envoyer les emails")
        send_btn.clicked.connect(self.send_emails)
        layout.addWidget(send_btn)
        
        # Initialiser la liste des templates
        self.refresh_templates()
        
        return tab
    
    def create_recipient_tab(self):
        """Crée l'onglet de gestion des destinataires"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Titre
        title_label = QLabel("📮 Gestion des Destinataires")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px")
        layout.addWidget(title_label)

        # Tableau des destinataires
        self.recipients_table = QTableWidget()
        self.recipients_table.setColumnCount(2)
        self.recipients_table.setHorizontalHeaderLabels(["Nom", "Email"])
        self.recipients_table.horizontalHeader().setStretchLastSection(True)
        self.recipients_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        layout.addWidget(self.recipients_table)

        # Boutons d'action
        buttons_layout = QHBoxLayout()

        add_btn = QPushButton("➕ Ajouter")
        add_btn.clicked.connect(self.add_recipient)
        buttons_layout.addWidget(add_btn)

        edit_btn = QPushButton("🖊️ Modifier")
        edit_btn.clicked.connect(self.edit_recipient)
        buttons_layout.addWidget(edit_btn)

        remove_btn = QPushButton("❌ Supprimer")
        remove_btn.clicked.connect(self.remove_recipient)
        buttons_layout.addWidget(remove_btn)

        import_btn = QPushButton("📥 Importer CSV")
        import_btn.clicked.connect(self.import_recipients)
        buttons_layout.addWidget(import_btn)

        export_btn = QPushButton("📤 Exporter CSV")
        export_btn.clicked.connect(self.export_recipients)
        buttons_layout.addWidget(export_btn)

        layout.addLayout(buttons_layout)

        # charger les destinataires au démarrage
        self.refresh_recipients()

        return tab
    
    def refresh_recipients(self):
        """Rafraîchit le tableau des destinataires"""
        recipients = self.recipients_manager.load_recipients()
        self.recipients_table.setRowCount(len(recipients))

        for i, recipient in enumerate(recipients):
            self.recipients_table.setItem(i, 0, QTableWidgetItem(recipient['name']))
            self.recipients_table.setItem(i, 1, QTableWidgetItem(recipient['email']))

    def add_recipient(self):
        """Ajoute un nouveau destinataire via une boîte de dialogue"""
        name, ok1 = QInputDialog.getText(self, "Ajouter un destinataire", "Nom :")
        if not ok1 or not name.strip():
            return
        
        email, ok2 = QInputDialog.getText(self, "Ajouter un destinataire", "Adresse email :")
        if not ok2 or not email.strip():
            return
        
        recipients = self.recipients_manager.load_recipients()

        # Vérifier si l'email existe déjà
        for recipient in recipients:
            if recipient['email'].lower() == email.lower():
                QMessageBox.warning(self, "Erreur", "Cet email existe déjà !")
                return
            
        recipients.append({'name': name.strip(), 'email': email.strip()})
        self.recipients_manager.save_recipients(recipients)
        self.refresh_recipients()

        QMessageBox.information(self, "Succès", f"Destinataire ajouté : {name.strip()}")

    def edit_recipient(self):
        """Modifie le destinataire sélectionné"""
        current_row = self.recipients_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un destinataire à modifier.")
            return
        
        recipients = self.recipients_manager.load_recipients()
        if current_row >= len(recipients):
            return
        
        current_recipient = recipients[current_row]

        name, ok1 = QInputDialog.getText(self, "Modifier un destinataire", "Nom :", text=current_recipient['name'])
        if not ok1:
            return
        
        email, ok2 = QInputDialog.getText(self, "Modifier un destinataire", "Adresse email :", text=current_recipient['email'])
        if not ok2 or not email.strip() or '@' not in email:
            QMessageBox.warning(self, "Erreur", "Veuillez saisir une adresse email valide.")
            return
        
        # Vérifier si le nouvel email existe déjà (sauf pour le destinataire actuel)
        for i, recipient in enumerate(recipients):
            if i != current_row and recipient['email'].lower() == email.lower():
                QMessageBox.warning(self, "Erreur", "Cet email existe déjà !")
                return
            
        recipients[current_row] = {'name': name.strip(), 'email': email.strip()}
        self.recipients_manager.save_recipients(recipients)
        self.refresh_recipients()

        QMessageBox.information(self, "Succès", f"Destinataire modifié : {name.strip()}")

    def remove_recipient(self):
        """Supprime le destinataire sélectionné"""
        current_row = self.recipients_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un destinataire à supprimer.")
            return
        
        recipients = self.recipients_manager.load_recipients()
        if current_row >= len(recipients):
            return
        
        recipient = recipients[current_row]
        
        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Êtes-vous sûr de vouloir supprimer :\n{recipient['name']} <{recipient['email']}> ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            recipients.pop(current_row)
            self.recipients_manager.save_recipients(recipients)
            self.refresh_recipients()
            QMessageBox.information(self, "Succès", "Destinataire supprimé.")

    def import_recipients(self):
        """Importe des destinataires depuis un fichier CSV"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Importer des destinataires",
            "",
            "Fichiers CSV (*.csv);;Tous les fichiers (*)"
        )

        if not file_path:
            return
        
        try:
            import csv
            imported_count = 0
            skipped_count = 0
            recipients = self.recipients_manager.load_recipients()
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

            self.recipients_manager.save_recipients(recipients)
            self.refresh_recipients()

            message = f"{imported_count} destinataire(s) importé(s)"
            if skipped_count > 0:
                message += f"\n{skipped_count} destinataire(s) ignoré(s) (doublons ou emails invalides)"

            QMessageBox.information(self, "Importation terminée", message)

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'importation : \n{str(e)}")

    def export_recipients(self):
        """Exporte les destinataires vers un fichier CSV"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter les destinataires",
            "destinataires_export.csv",
            "Fichiers CSV (*.csv);;Tous les fichiers (*)"
        )

        if not file_path:
            return
        
        try:
            recipients = self.recipients_manager.load_recipients()

            import csv
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['name', 'email'])
                writer.writeheader()
                writer.writerows(recipients)

            QMessageBox.information(self, "Succès", f"Liste exportée vers :\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'exportation : \n{str(e)}")

    def add_drive_link(self, media_type):
        link, ok = QInputDialog.getText(
            self,
            f"Ajouter un lien {media_type}",
            "Entrez le lien Google Drive :"
        )
        
        if ok and link.strip():
            if media_type == "image":
                self.image_links.append(link.strip())
                self.images_list.addItem(link.strip())
            else:
                self.video_links.append(link.strip())
                self.videos_list.addItem(link.strip())

    def remove_link(self, media_type):
        if media_type == "image":
            current_row = self.images_list.currentRow()
            if current_row >= 0:
                self.image_links.pop(current_row)
                self.images_list.takeItem(current_row)
        else:
            current_row = self.videos_list.currentRow()
            if current_row >= 0:
                self.video_links.pop(current_row)
                self.videos_list.takeItem(current_row)

    def refresh_templates(self):
        """Rafraîchit la liste des templates disponibles"""
        self.template_combo.clear()
        output_dir = os.path.join(os.getcwd(), "output")
        
        if os.path.exists(output_dir):
            templates = [f for f in os.listdir(output_dir) if f.endswith('.html')]
            templates.sort(reverse=True)  # Plus récent en premier
            self.template_combo.addItems(templates)
    
    def preview_template(self):
        """Ouvre le template sélectionné dans le navigateur"""
        if self.template_combo.currentText():
            template_path = os.path.join(os.getcwd(), "output", self.template_combo.currentText())
            QDesktopServices.openUrl(QUrl.fromLocalFile(template_path))
    
    def send_emails(self):
        """Envoie les emails avec le template sélectionné"""
        if not self.template_combo.currentText():
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner un template!")
            return
            
        try:
            template_path = os.path.join(os.getcwd(), "output", self.template_combo.currentText())
            
            # Confirmation avant envoi
            reply = QMessageBox.question(
                self,
                "Confirmation",
                "Êtes-vous sûr de vouloir envoyer les emails à tous les destinataires ?\n\n" +
                "Assurez-vous que le fichier destinataires.csv est à jour.",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                email_sender = EmailSender()
                email_sender.send_bulk_emails()
                QMessageBox.information(self, "Succès", "Emails envoyés avec succès à tous les destinataires!")
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'envoi : {str(e)}")

    def generate_template(self):
        title = self.title_input.text().strip()
        content = self.content_text.toPlainText().strip()
        
        if not title:
            QMessageBox.warning(self, "Attention", "L'objet du mail ne peut pas être vide!")
            return
            
        if not content:
            QMessageBox.warning(self, "Attention", "Le contenu du mail ne peut pas être vide!")
            return
        
        try:
            # Construction du dictionnaire de données
            data = {
                'title': title,
                'text': content,
                'photos': self.image_links,
                'videos': self.video_links,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Génération du HTML
            html_content = self.template_generator.generate_html(data)
            
            # Sauvegarde
            filepath = self.template_generator.save_html(html_content)
            
            success_message = f"Template généré avec succès!\n\nFichier : {filepath}"
            QMessageBox.information(self, "Succès", success_message)
            
            # Rafraîchir la liste des templates
            self.refresh_templates()
            
            # Proposition d'ouverture du fichier
            reply = QMessageBox.question(
                self, 
                "Ouvrir le fichier",
                "Voulez-vous ouvrir le fichier HTML ?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Ouvrir le fichier avec le navigateur par défaut
                QDesktopServices.openUrl(QUrl.fromLocalFile(filepath))
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la génération : {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = EmailGeneratorGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()