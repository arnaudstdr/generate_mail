#!/usr/bin/env python3
"""
Générateur de template HTML pour emails
Association Gamadji - Village en Afrique

Ce script génère des templates HTML pour des emails avec :
- Titre personnalisé (identique à l'objet du mail)
- Texte personnalisé
- Photos depuis Google Drive (max 10)
- Vidéos depuis Google Drive avec aperçus (max 10)
- Design responsive avec couleurs inspirées de l'Afrique
"""

import os
import re
from datetime import datetime
from typing import List, Dict, Optional
import requests
from .utils import GoogleDriveUtils
from .template_html import EmailTemplate


class EmailTemplateGenerator:
    """Générateur principal de templates d'emails"""
    
    def __init__(self):
        self.google_utils = GoogleDriveUtils()
        self.template = EmailTemplate()
        
    def collect_user_input(self) -> Dict:
        """Collecte les informations saisies par l'utilisateur de manière interactive"""
        print("=== GÉNÉRATEUR DE TEMPLATE EMAIL - ASSOCIATION GAMADJI ===\n")
        
        # Titre/Objet du mail
        title = input("📧 Objet du mail (sera aussi le titre de l'email) : ").strip()
        while not title:
            title = input("⚠️  L'objet ne peut pas être vide. Veuillez saisir l'objet : ").strip()
        
        # Texte principal
        print("\n📝 Texte de l'email :")
        print("   (Tapez votre texte. Appuyez sur Entrée deux fois pour terminer)")
        text_lines = []
        empty_line_count = 0
        
        while empty_line_count < 2:
            line = input()
            if line.strip() == "":
                empty_line_count += 1
            else:
                empty_line_count = 0
            text_lines.append(line)
        
        # Retirer les lignes vides de fin
        while text_lines and text_lines[-1].strip() == "":
            text_lines.pop()
            
        text_content = "\n".join(text_lines)
        
        # Photos
        photos = self._collect_media_links("📷 Photos", "photo", 10)
        
        # Vidéos
        videos = self._collect_media_links("🎥 Vidéos", "vidéo", 10)
        
        return {
            'title': title,
            'text': text_content,
            'photos': photos,
            'videos': videos,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _collect_media_links(self, media_type: str, media_name: str, max_count: int) -> List[str]:
        """Collecte les liens Google Drive pour un type de média"""
        print(f"\n{media_type} (maximum {max_count}) :")
        print(f"   Collez les liens de partage Google Drive (un par ligne)")
        print(f"   Laissez une ligne vide pour terminer la saisie des {media_name}s")
        
        links = []
        while len(links) < max_count:
            link = input(f"   {media_name.capitalize()} {len(links) + 1} : ").strip()
            
            if not link:
                break
                
            if self.google_utils.is_valid_google_drive_link(link):
                links.append(link)
                print(f"   ✅ {media_name.capitalize()} {len(links)} ajoutée")
            else:
                print(f"   ❌ Lien invalide. Veuillez utiliser un lien de partage Google Drive")
        
        print(f"   📊 Total : {len(links)} {media_name}(s) ajoutée(s)")
        return links
    
    def generate_html(self, data: Dict) -> str:
        """Génère le HTML final avec les données collectées"""
        print("\n🔄 Génération du template HTML...")
        
        # Traitement des médias
        processed_photos = []
        for photo_link in data['photos']:
            photo_data = self.google_utils.process_photo(photo_link)
            if photo_data:
                processed_photos.append(photo_data)
        
        processed_videos = []
        for video_link in data['videos']:
            video_data = self.google_utils.process_video(video_link)
            if video_data:
                processed_videos.append(video_data)
        
        # Génération du HTML
        html_content = self.template.generate(
            title=data['title'],
            text=data['text'],
            photos=processed_photos,
            videos=processed_videos,
            timestamp=data['timestamp']
        )
        
        return html_content
    
    def save_html(self, html_content: str, filename: Optional[str] = None) -> str:
        """Sauvegarde le HTML généré dans un fichier"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"email_template_{timestamp}.html"
        
        # Créer le dossier output s'il n'existe pas
        output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def run(self):
        """Exécute le processus complet de génération de template"""
        try:
            # Collecte des données
            data = self.collect_user_input()
            
            # Génération du HTML
            html_content = self.generate_html(data)
            
            # Sauvegarde
            filepath = self.save_html(html_content)
            
            print(f"\n✅ Template généré avec succès !")
            print(f"📁 Fichier sauvegardé : {filepath}")
            print(f"📧 Objet du mail : {data['title']}")
            print(f"📊 Contenu : {len(data['photos'])} photo(s), {len(data['videos'])} vidéo(s)")
            
            # Proposition d'ouverture
            response = input("\n🌐 Voulez-vous ouvrir le fichier HTML ? (o/n) : ").strip().lower()
            if response in ['o', 'oui', 'y', 'yes']:
                os.system(f"open '{filepath}'")
            
        except KeyboardInterrupt:
            print("\n\n❌ Génération annulée par l'utilisateur")
        except Exception as e:
            print(f"\n❌ Erreur lors de la génération : {str(e)}")


if __name__ == "__main__":
    generator = EmailTemplateGenerator()
    generator.run()