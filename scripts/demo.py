#!/usr/bin/env python3
"""
Script de démonstration du générateur de templates email
Association Gamadji - Village en Afrique

Ce script montre un exemple d'utilisation sans interface interactive
"""

from .template_mail_generator import EmailTemplateGenerator
from datetime import datetime


def demo_rapide():
    """Démonstration rapide avec des données prédéfinies"""
    
    print("🚀 DÉMONSTRATION RAPIDE - Générateur de Template Email")
    print("=" * 60)
    
    # Données de démonstration
    demo_data = {
        'title': 'Démonstration - Nouvelles du village de Gamadji',
        'text': '''Chers amis et soutiens de l'association,

Nous espérons que vous vous portez bien. Nous souhaitons partager avec vous quelques nouvelles importantes de notre village.

Grâce à votre soutien continu, nous avons pu réaliser de nombreux projets qui améliorent la vie quotidienne de notre communauté.

Dans cette lettre, vous trouverez des photos et des vidéos qui témoignent de nos réalisations récentes.

Merci infiniment pour votre générosité et votre engagement à nos côtés.

L'équipe de l'Association Gamadji''',
        'photos': [
            'https://drive.google.com/file/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/view',
            'https://drive.google.com/open?id=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
        ],
        'videos': [
            'https://drive.google.com/file/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/view'
        ],
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Création du générateur
    generator = EmailTemplateGenerator()
    
    print(f"📧 Objet/Titre : {demo_data['title']}")
    print(f"📝 Texte : {len(demo_data['text'])} caractères")
    print(f"📷 Photos : {len(demo_data['photos'])} items")
    print(f"🎥 Vidéos : {len(demo_data['videos'])} items")
    print()
    
    # Génération du HTML
    print("🔄 Génération du template HTML...")
    html_content = generator.generate_html(demo_data)
    
    # Sauvegarde
    filename = f"demo_email_template_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = generator.save_html(html_content, filename)
    
    print()
    print("✅ DÉMONSTRATION TERMINÉE !")
    print(f"📁 Fichier généré : {filepath}")
    print()
    print("💡 Pour utiliser le script interactif complet :")
    print("   python template_mail_generator.py")
    print()
    print("🌐 Vous pouvez maintenant ouvrir le fichier HTML dans votre navigateur")
    print("   pour voir le résultat !")


if __name__ == "__main__":
    demo_rapide()