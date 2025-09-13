"""
Utilitaires pour Google Drive
Association Gamadji Saré

Fonctions pour traiter les liens Google Drive et extraire les informations nécessaires
"""

import re
import requests
from typing import Dict, Optional
from urllib.parse import urlparse, parse_qs


class GoogleDriveUtils:
    """Utilitaires pour manipuler les liens et fichiers Google Drive"""
    
    @staticmethod
    def is_valid_google_drive_link(link: str) -> bool:
        """Vérifie si le lien est un lien Google Drive valide"""
        if not link:
            return False
        
        # Patterns pour les liens Google Drive
        patterns = [
            r'https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)',
            r'https://drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)',
            r'https://docs\.google\.com/.*?/d/([a-zA-Z0-9_-]+)'
        ]
        
        for pattern in patterns:
            if re.search(pattern, link):
                return True
        
        return False
    
    @staticmethod
    def extract_file_id(link: str) -> Optional[str]:
        """Extrait l'ID du fichier depuis un lien Google Drive"""
        if not GoogleDriveUtils.is_valid_google_drive_link(link):
            return None
        
        # Patterns pour extraire l'ID
        patterns = [
            r'https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)',
            r'https://drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)',
            r'https://docs\.google\.com/.*?/d/([a-zA-Z0-9_-]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, link)
            if match:
                return match.group(1)
        
        return None
    
    @staticmethod
    def get_direct_image_url(file_id: str) -> str:
        """Génère l'URL directe pour afficher une image depuis Google Drive"""
        # Utilise l'URL thumbnail avec une grande taille pour avoir une image de qualité
        return f"https://drive.google.com/thumbnail?id={file_id}&sz=w1000-h1000"
    
    @staticmethod
    def get_thumbnail_url(file_id: str, size: int = 400) -> str:
        """Génère l'URL pour une miniature d'une taille donnée"""
        return f"https://drive.google.com/thumbnail?id={file_id}&sz=w{size}-h{size}"
    
    @staticmethod
    def get_video_embed_url(file_id: str) -> str:
        """Génère l'URL d'embed pour une vidéo Google Drive"""
        return f"https://drive.google.com/file/d/{file_id}/preview"
    
    @staticmethod
    def get_file_info(file_id: str) -> Dict[str, str]:
        """Récupère les informations basiques d'un fichier (nom, type)"""
        # Pour l'instant, on génère des infos basiques
        # Dans une version future, on pourrait utiliser l'API Google Drive pour plus de détails
        return {
            'id': file_id,
            'name': f'Fichier_{file_id[:8]}',
            'type': 'unknown'
        }
    
    def process_photo(self, photo_link: str) -> Optional[Dict]:
        """Traite un lien photo et retourne les informations nécessaires"""
        file_id = self.extract_file_id(photo_link)
        if not file_id:
            print(f"⚠️  Impossible d'extraire l'ID du fichier : {photo_link}")
            return None
        
        return {
            'id': file_id,
            'original_link': photo_link,
            'direct_url': self.get_direct_image_url(file_id),
            'thumbnail_url': self.get_thumbnail_url(file_id, 800),
            'type': 'photo',
            'info': self.get_file_info(file_id)
        }
    
    def process_video(self, video_link: str) -> Optional[Dict]:
        """Traite un lien vidéo et retourne les informations nécessaires"""
        file_id = self.extract_file_id(video_link)
        if not file_id:
            print(f"⚠️  Impossible d'extraire l'ID du fichier : {video_link}")
            return None
        
        return {
            'id': file_id,
            'original_link': video_link,
            'embed_url': self.get_video_embed_url(file_id),
            'thumbnail_url': self.get_thumbnail_url(file_id, 480),
            'direct_link': f"https://drive.google.com/file/d/{file_id}/view",
            'type': 'video',
            'info': self.get_file_info(file_id)
        }
    
    @staticmethod
    def test_link_accessibility(url: str) -> bool:
        """Teste si un lien est accessible publiquement"""
        try:
            response = requests.head(url, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False