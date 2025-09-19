import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox,
    QListWidget, QInputDialog
)
from PyQt5.QtCore import Qt
from scripts.template_mail_generator import EmailTemplateGenerator
from datetime import datetime
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

class EmailGeneratorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Générateur d'Emails - Association Gamadji")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        
        self.image_links = []  # Liste pour les liens d'images Google Drive
        self.video_links = []  # Liste pour les liens vidéos Google Drive
        self.template_generator = EmailTemplateGenerator()
        
        # Widget central et layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
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
        main_layout.addLayout(content_layout)
        
        # Bouton de génération
        generate_btn = QPushButton("🚀 Générer le template")
        generate_btn.clicked.connect(self.generate_template)
        main_layout.addWidget(generate_btn)

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