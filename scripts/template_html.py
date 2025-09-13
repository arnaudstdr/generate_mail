"""
Template HTML pour emails
Association Gamadji - Village en Afrique

Génère des templates HTML responsives avec une palette de couleurs inspirée de l'Afrique
"""

from typing import List, Dict


class EmailTemplate:
    """Générateur de templates HTML pour emails"""
    
    def __init__(self):
        self.css_styles = self._get_css_styles()
    
    def _get_css_styles(self) -> str:
        """Retourne les styles CSS pour le template"""
        return """
        <style>
            /* Reset et base */
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #2c3e50;
                background-color: #f8f9fa;
            }
            
            .email-container {
                max-width: 800px;
                margin: 0 auto;
                background-color: #ffffff;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
                border-radius: 10px;
                overflow: hidden;
            }
            
            /* Header avec couleurs africaines */
            .header {
                background: linear-gradient(135deg, #d2691e 0%, #cd853f 50%, #daa520 100%);
                padding: 40px 30px;
                text-align: center;
                color: white;
                position: relative;
            }
            
            .header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="80" cy="40" r="1.5" fill="rgba(255,255,255,0.1)"/><circle cx="60" cy="80" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="30" cy="70" r="1.5" fill="rgba(255,255,255,0.1)"/></svg>') repeat;
                opacity: 0.3;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                position: relative;
                z-index: 1;
            }
            
            .header .subtitle {
                font-size: 1.2em;
                opacity: 0.9;
                position: relative;
                z-index: 1;
            }
            
            /* Contenu principal */
            .content {
                padding: 40px 30px;
            }
            
            .text-content {
                font-size: 1.1em;
                margin-bottom: 40px;
                text-align: justify;
                background-color: #faf9f6;
                padding: 25px;
                border-radius: 8px;
                border-left: 4px solid #d2691e;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            }
            
            .text-content p {
                margin-bottom: 15px;
            }
            
            /* Grilles de médias */
            .media-section {
                margin-bottom: 40px;
            }
            
            .media-section h2 {
                color: #8b4513;
                margin-bottom: 20px;
                font-size: 1.8em;
                border-bottom: 2px solid #daa520;
                padding-bottom: 10px;
                display: flex;
                align-items: center;
            }
            
            .media-section h2::before {
                content: '';
                width: 30px;
                height: 30px;
                margin-right: 15px;
                background: linear-gradient(45deg, #d2691e, #daa520);
                border-radius: 50%;
            }
            
            .media-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            
            /* Photos */
            .photo-item {
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                background: white;
            }
            
            .photo-item:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            }
            
            .photo-item img {
                width: 100%;
                height: auto;
                display: block;
                max-height: 400px;
                object-fit: cover;
            }
            
            /* Vidéos */
            .video-item {
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
                background: white;
                position: relative;
            }
            
            .video-item:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            }
            
            .video-thumbnail {
                position: relative;
                width: 100%;
                height: 250px;
                background-size: cover;
                background-position: center;
                cursor: pointer;
            }
            
            .video-overlay {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.3);
                display: flex;
                align-items: center;
                justify-content: center;
                transition: background 0.3s ease;
            }
            
            .video-thumbnail:hover .video-overlay {
                background: rgba(0,0,0,0.5);
            }
            
            .play-button {
                width: 80px;
                height: 80px;
                background: rgba(255,255,255,0.9);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 30px;
                color: #d2691e;
                transition: transform 0.3s ease;
            }
            
            .video-thumbnail:hover .play-button {
                transform: scale(1.1);
                background: white;
            }
            
            .video-info {
                padding: 15px;
                text-align: center;
            }
            
            .video-link {
                display: inline-block;
                padding: 10px 20px;
                background: linear-gradient(45deg, #d2691e, #daa520);
                color: white;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                transition: transform 0.3s ease;
                margin-top: 10px;
            }
            
            .video-link:hover {
                transform: translateY(-2px);
                text-decoration: none;
                color: white;
            }
            
            /* Footer */
            .footer {
                background: #2c3e50;
                color: white;
                padding: 30px;
                text-align: center;
            }
            
            .footer .association-name {
                font-size: 1.3em;
                font-weight: bold;
                margin-bottom: 10px;
                color: #daa520;
            }
            
            .footer .timestamp {
                opacity: 0.7;
                font-size: 0.9em;
            }
            
            /* Responsive */
            @media (max-width: 768px) {
                .email-container {
                    margin: 0;
                    border-radius: 0;
                }
                
                .header {
                    padding: 30px 20px;
                }
                
                .header h1 {
                    font-size: 2em;
                }
                
                .content {
                    padding: 30px 20px;
                }
                
                .media-grid {
                    grid-template-columns: 1fr;
                }
                
                .text-content {
                    padding: 20px;
                }
            }
            
            @media (max-width: 480px) {
                .header h1 {
                    font-size: 1.8em;
                }
                
                .content {
                    padding: 20px 15px;
                }
                
                .text-content {
                    padding: 15px;
                }
            }
        </style>
        """
    
    def _format_text_content(self, text: str) -> str:
        """Formate le texte en HTML en préservant les sauts de ligne"""
        if not text:
            return ""
        
        # Remplace les sauts de ligne par des balises <p>
        paragraphs = text.split('\n\n')
        formatted_paragraphs = []
        
        for paragraph in paragraphs:
            if paragraph.strip():
                # Remplace les sauts de ligne simples par <br>
                formatted = paragraph.replace('\n', '<br>')
                formatted_paragraphs.append(f"<p>{formatted}</p>")
        
        return '\n'.join(formatted_paragraphs)
    
    def _generate_photos_html(self, photos: List[Dict]) -> str:
        """Génère le HTML pour la section photos"""
        if not photos:
            return ""
        
        photos_html = []
        for photo in photos:
            # Générer plusieurs URLs de fallback
            file_id = photo['id']
            fallback_urls = [
                photo['direct_url'],
                f"https://drive.google.com/uc?export=view&id={file_id}",
                f"https://drive.google.com/thumbnail?id={file_id}&sz=w800-h600",
                photo['thumbnail_url']
            ]
            
            # Script JavaScript pour essayer les URLs une par une
            fallback_script = ""
            for i, url in enumerate(fallback_urls[1:], 1):
                fallback_script += f"if(this.dataset.fallback=='{i-1}') {{this.src='{url}'; this.dataset.fallback='{i}'; return;}} "
            
            photo_html = f"""
            <div class="photo-item">
                <img src="{fallback_urls[0]}" 
                     alt="Photo {photo['info']['name']}" 
                     data-fallback="0"
                     onerror="{fallback_script}this.style.display='none'; this.nextElementSibling.style.display='block';" 
                     style="max-width: 100%; height: auto;" />
                <div style="display: none; padding: 20px; text-align: center; background: #f8f9fa; border: 2px dashed #ddd; border-radius: 8px; color: #666;">
                    <p>📷 Photo non disponible</p>
                    <p style="font-size: 0.9em;">Vérifiez que le fichier Google Drive est partagé publiquement</p>
                    <a href="https://drive.google.com/file/d/{file_id}/view" target="_blank" style="color: #d2691e; text-decoration: none;">
                        🔗 Voir sur Google Drive
                    </a>
                </div>
            </div>
            """
            photos_html.append(photo_html)
        
        return f"""
        <div class="media-section">
            <h2>📷 Photos</h2>
            <div class="media-grid">
                {''.join(photos_html)}
            </div>
        </div>
        """
    
    def _generate_videos_html(self, videos: List[Dict]) -> str:
        """Génère le HTML pour la section vidéos"""
        if not videos:
            return ""
        
        videos_html = []
        for video in videos:
            video_html = f"""
            <div class="video-item">
                <div class="video-thumbnail" style="background-image: url('{video['thumbnail_url']}');"
                     onclick="window.open('{video['direct_link']}', '_blank')">
                    <div class="video-overlay">
                        <div class="play-button">▶</div>
                    </div>
                </div>
                <div class="video-info">
                    <p><strong>Vidéo {video['info']['name']}</strong></p>
                    <a href="{video['direct_link']}" target="_blank" class="video-link">
                        🎥 Regarder la vidéo
                    </a>
                </div>
            </div>
            """
            videos_html.append(video_html)
        
        return f"""
        <div class="media-section">
            <h2>🎥 Vidéos</h2>
            <div class="media-grid">
                {''.join(videos_html)}
            </div>
        </div>
        """
    
    def generate(self, title: str, text: str, photos: List[Dict], videos: List[Dict], timestamp: str) -> str:
        """Génère le template HTML complet"""
        
        # Formatage du texte
        formatted_text = self._format_text_content(text)
        
        # Génération des sections médias
        photos_section = self._generate_photos_html(photos)
        videos_section = self._generate_videos_html(videos)
        
        # Template HTML complet
        html_template = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>{title}</title>
    {self.css_styles}
</head>
<body>
    <div class="email-container">
        <!-- Header -->
        <div class="header">
            <h1>{title}</h1>
            <div class="subtitle">Association Gamadji Saré</div>
        </div>
        
        <!-- Contenu principal -->
        <div class="content">
            <!-- Texte -->
            <div class="text-content">
                {formatted_text if formatted_text else '<p><em>Aucun texte fourni</em></p>'}
            </div>
            
            <!-- Photos -->
            {photos_section}
            
            <!-- Vidéos -->
            {videos_section}
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <div class="association-name">Association Gamadji Saré</div>
            <div class="timestamp">Généré le {timestamp}</div>
        </div>
    </div>
</body>
</html>
        """
        
        return html_template.strip()