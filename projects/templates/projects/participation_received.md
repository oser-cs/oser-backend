{% extends 'projects/to_user.md' %}

{% block body %}
Tu as demandé t'inscrire à {{ edition }} via l'espace projets.

Nous avons bien reçu ta demande et allons vérifier ton dossier dès que possible.

{% if edition.edition_form.form.files.count %}
📖 **Rappel** : l'inscription à ce projet nécessite de fournir des documents complémentaires.

🔗 Tu peux télécharger ces documents à tout moment en te rendant dans la section [Mes inscriptions]({{ edition.get_registration_url }}).

Fais-nous parvenir ces documents **impérativement avant le {{ edition.edition_form.deadline | date }}** à l'adresse suivante :

{{ edition.edition_form.recipient.user.get_full_name }}  
{{ edition.edition_form.recipient.address }}

⚠️ Nous ne pourrons valider ton dossier qu'une fois ces documents reçus.
{% endif %}
{% endblock %}
