from mails import Notification

class SendDocs(Notification):
    """Sends a link to the google docs containing the registration documents"""
    subject = "Dossier d'inscription OSER"

    template_name = "profiles/registration_docs.md"
    args = ('user',)
    def get_recipients(self):
        return [self.user.email]

