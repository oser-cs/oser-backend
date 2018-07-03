{% extends 'projects/to_user.md' %}

{% block body %}
Ta participation à {{ edition }} a bien été supprimée.

Si tu souhaites finalement participer à ce projet, tu devras te réinscrire en te rendant sur [l'espace projets]({{ edition.get_projects_site_url }}).
{% endblock %}
