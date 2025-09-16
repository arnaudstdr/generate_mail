## 📋 Configuration

### Fichier d'environnement (.env)

Pour sécuriser les informations sensibles comme les identifiants email, le projet utilise un fichier `.env` à la racine du projet. Créez ce fichier avec le contenu suivant :

```
# Configuration pour l'envoi d'emails
EMAIL_SENDER=votre_email@gmail.com
EMAIL_PASSWORD=votre_mot_de_passe_application
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

**Notes importantes :**
- Pour Gmail, il est recommandé d'utiliser un "mot de passe d'application" plutôt que votre mot de passe principal
- Ne partagez jamais votre fichier `.env` et ajoutez-le à votre `.gitignore`