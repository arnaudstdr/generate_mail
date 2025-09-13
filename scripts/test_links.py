#!/usr/bin/env python3
"""
Testeur de liens Google Drive
Association Gamadji - Village en Afrique

Script pour tester et valider les liens Google Drive avant de générer un template
"""

from .utils import GoogleDriveUtils
import requests


class GoogleDriveTester:
    """Testeur pour les liens Google Drive"""
    
    def __init__(self):
        self.utils = GoogleDriveUtils()
    
    def test_photo_urls(self, file_id: str) -> dict:
        """Teste différentes URLs pour une photo et retourne les résultats"""
        urls_to_test = {
            'Thumbnail (nouveau)': f"https://drive.google.com/thumbnail?id={file_id}&sz=w1000-h1000",
            'UC Export': f"https://drive.google.com/uc?export=view&id={file_id}",
            'Thumbnail (ancien)': f"https://drive.google.com/thumbnail?id={file_id}&sz=s800",
            'Thumbnail 800x600': f"https://drive.google.com/thumbnail?id={file_id}&sz=w800-h600"
        }
        
        results = {}
        print(f"\n🧪 Test des URLs pour l'ID: {file_id}")
        print("-" * 60)
        
        for name, url in urls_to_test.items():
            try:
                response = requests.head(url, timeout=10, allow_redirects=True)
                status = "✅ OK" if response.status_code == 200 else f"❌ {response.status_code}"
                results[name] = {
                    'url': url,
                    'status_code': response.status_code,
                    'working': response.status_code == 200
                }
                print(f"{status:8} | {name:20} | {url}")
                
            except requests.RequestException as e:
                results[name] = {
                    'url': url,
                    'status_code': None,
                    'working': False,
                    'error': str(e)
                }
                print(f"❌ ERR   | {name:20} | Erreur: {str(e)[:50]}...")
        
        return results
    
    def test_video_urls(self, file_id: str) -> dict:
        """Teste les URLs pour une vidéo"""
        urls_to_test = {
            'Thumbnail vidéo': f"https://drive.google.com/thumbnail?id={file_id}&sz=w480-h360",
            'Lien direct': f"https://drive.google.com/file/d/{file_id}/view",
            'Preview embed': f"https://drive.google.com/file/d/{file_id}/preview"
        }
        
        results = {}
        print(f"\n🎥 Test des URLs vidéo pour l'ID: {file_id}")
        print("-" * 60)
        
        for name, url in urls_to_test.items():
            try:
                response = requests.head(url, timeout=10, allow_redirects=True)
                status = "✅ OK" if response.status_code == 200 else f"❌ {response.status_code}"
                results[name] = {
                    'url': url,
                    'status_code': response.status_code,
                    'working': response.status_code == 200
                }
                print(f"{status:8} | {name:20} | {url}")
                
            except requests.RequestException as e:
                results[name] = {
                    'url': url,
                    'status_code': None,
                    'working': False,
                    'error': str(e)
                }
                print(f"❌ ERR   | {name:20} | Erreur: {str(e)[:50]}...")
        
        return results
    
    def test_link(self, link: str):
        """Teste un lien Google Drive complet"""
        print(f"\n🔗 Test du lien: {link}")
        print("=" * 80)
        
        # Validation du lien
        if not self.utils.is_valid_google_drive_link(link):
            print("❌ ERREUR: Lien Google Drive invalide")
            return
        
        # Extraction de l'ID
        file_id = self.utils.extract_file_id(link)
        if not file_id:
            print("❌ ERREUR: Impossible d'extraire l'ID du fichier")
            return
        
        print(f"📋 ID extrait: {file_id}")
        
        # Test des URLs photos
        photo_results = self.test_photo_urls(file_id)
        
        # Test des URLs vidéos
        video_results = self.test_video_urls(file_id)
        
        # Résumé
        photo_working = sum(1 for result in photo_results.values() if result['working'])
        video_working = sum(1 for result in video_results.values() if result['working'])
        
        print(f"\n📊 RÉSUMÉ:")
        print(f"   Photos: {photo_working}/{len(photo_results)} URLs fonctionnelles")
        print(f"   Vidéos: {video_working}/{len(video_results)} URLs fonctionnelles")
        
        if photo_working > 0:
            best_photo = next(result for result in photo_results.values() if result['working'])
            print(f"   ✅ Meilleure URL photo: {best_photo['url']}")
        else:
            print(f"   ⚠️  Aucune URL photo ne fonctionne - vérifiez les permissions de partage")
        
        return {
            'file_id': file_id,
            'photo_results': photo_results,
            'video_results': video_results,
            'photo_working_count': photo_working,
            'video_working_count': video_working
        }
    
    def interactive_test(self):
        """Interface interactive pour tester les liens"""
        print("🧪 TESTEUR DE LIENS GOOGLE DRIVE")
        print("=" * 40)
        print()
        print("Collez vos liens Google Drive pour les tester avant de générer votre template.")
        print("Laissez vide pour terminer.")
        print()
        
        while True:
            link = input("🔗 Lien Google Drive à tester : ").strip()
            
            if not link:
                break
            
            self.test_link(link)
            print("\n" + "="*80)
        
        print("\n✅ Tests terminés !")


if __name__ == "__main__":
    tester = GoogleDriveTester()
    tester.interactive_test()