"""
Module pour l'envoi d'emails
Association Gamadji - Village en Afrique

Ce module contiendra les fonctionnalités d'envoi direct d'emails une fois développées.

Fonctionnalités prévues :
- Configuration des serveurs SMTP
- Envoi via Gmail API
- Envoi via services tiers (SendGrid, etc.)
- Gestion des listes de diffusion
- Tracking des envois
"""

__version__ = "0.1.0"

# Placeholder pour les futures classes d'envoi
class EmailSender:
    """Classe principale pour l'envoi d'emails - À développer"""
    
    def __init__(self):
        # Configuration à développer
        pass
    
    def send_email(self, html_content: str, subject: str, recipients: list):
        """Envoi d'email - À implémenter"""
        raise NotImplementedError("Fonctionnalité en cours de développement")

class GmailSender(EmailSender):
    """Envoi via Gmail API - À développer"""
    pass

class SMTPSender(EmailSender):
    """Envoi via SMTP - À développer"""
    pass