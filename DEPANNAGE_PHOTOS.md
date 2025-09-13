# Guide de Dépannage - Photos Google Drive

## 🔍 Problème : Photos qui ne s'affichent pas

### ✅ Solution rapide (nouveau système)

Le générateur utilise maintenant **4 méthodes différentes** pour afficher vos photos :

1. **Thumbnail haute résolution** (1000x1000px)
2. **Export classique** (méthode UC)
3. **Thumbnail standard** (800x800px) 
4. **Message d'erreur + lien direct** (si tout échoue)

### 🧪 Diagnostic avec le testeur

```bash
python test_links.py
```

**Exemple de résultat :**
```
🔗 Test du lien: https://drive.google.com/file/d/1ABC.../view

📋 ID extrait: 1ABC...

🧪 Test des URLs pour l'ID: 1ABC...
✅ OK    | Thumbnail (nouveau)  | https://drive.google.com/thumbnail?id=1ABC...&sz=w1000-h1000
❌ 403   | UC Export           | https://drive.google.com/uc?export=view&id=1ABC...
✅ OK    | Thumbnail (ancien)  | https://drive.google.com/thumbnail?id=1ABC...&sz=s800
✅ OK    | Thumbnail 800x600   | https://drive.google.com/thumbnail?id=1ABC...&sz=w800-h600

📊 RÉSUMÉ:
   Photos: 3/4 URLs fonctionnelles
   ✅ Meilleure URL photo: https://drive.google.com/thumbnail?id=1ABC...&sz=w1000-h1000
```

### 🔧 Étapes de dépannage

#### 1. Vérifiez le partage du fichier

**❌ Incorrect :**
- "Restreint" 
- "Personnes spécifiques"

**✅ Correct :**
- "Accessible à tous ceux qui ont le lien"
- "Public sur le Web"

#### 2. Testez le lien manuellement

1. Ouvrez votre lien dans un **navigateur privé**
2. Vous devriez voir la photo **sans vous connecter**
3. Si demande de connexion → permissions incorrectes

#### 3. Utilisez le testeur intégré

```bash
# Dans le dossier du projet
python test_links.py
```

Collez votre lien et analysez les résultats :
- **3-4 URLs OK** → Excellent, photos s'afficheront
- **1-2 URLs OK** → Bon, avec fallback
- **0 URL OK** → Problème de permissions

#### 4. Formats de liens acceptés

✅ **Fonctionnent :**
```
https://drive.google.com/file/d/1ABC123.../view
https://drive.google.com/open?id=1ABC123...
https://docs.google.com/.../d/1ABC123.../edit
```

❌ **Ne fonctionnent pas :**
```
https://drive.google.com/drive/folders/... (dossier)
https://photos.google.com/... (Google Photos)
URLs tronquées ou modifiées
```

### 🎯 Solutions par type d'erreur

#### Erreur 403 (Forbidden)
- **Cause :** Fichier pas assez partagé
- **Solution :** Partager "Accessible à tous ceux qui ont le lien"

#### Erreur 404 (Not Found)
- **Cause :** Lien incorrect ou fichier supprimé
- **Solution :** Vérifier le lien et l'existence du fichier

#### Timeout/Erreur réseau
- **Cause :** Problème temporaire ou fichier très lourd
- **Solution :** Réessayer plus tard ou compresser l'image

### 💡 Bonnes pratiques

1. **Testez avant de générer** avec `python test_links.py`
2. **Utilisez des images de taille raisonnable** (< 5 MB)
3. **Préférez les formats JPG/PNG** pour les photos
4. **Créez un dossier dédié** dans Google Drive pour vos photos d'emails

### 🔄 En cas d'échec total

Si aucune URL ne fonctionne, le template affichera :

```
📷 Photo non disponible
Vérifiez que le fichier Google Drive est partagé publiquement
🔗 Voir sur Google Drive
```

**L'utilisateur peut cliquer** sur le lien pour voir la photo sur Google Drive.

### 📞 Support

Si le problème persiste :

1. ✅ Vérifiez que vous avez suivi tous les points ci-dessus
2. 📋 Notez les résultats du testeur de liens
3. 🔗 Testez avec une autre photo pour confirmer
4. 📧 Contactez l'équipe avec ces informations

---

**✨ Le nouveau système est beaucoup plus robuste et devrait résoudre 95% des problèmes d'affichage !**