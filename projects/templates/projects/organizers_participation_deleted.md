{% extends 'projects/to_user.md' %}

{% block body %}
L'utilisateur {{ user }} a annulé sa participation à {{ edition }}.

Si besoin, vous pouvez contacter {{ user }} via son adresse email : {{ user.email }}.

Vous pouvez télécharger la feuille des inscrits mise à jour sur [le site d'administration]({{ editionform_admin_url }}).
{% endblock %}
