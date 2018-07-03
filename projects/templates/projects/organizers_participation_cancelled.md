{% extends 'projects/to_user.md' %}

{% block body %}
L'utilisateur {{ user }} a supprimé sa participation à {{ edition }}.

Si besoin, vous pouvez contacter {{ user }} via son adresse email : {{ user.email }}.

Vous pouvez télécharger la feuille des inscrits mise à jour sur [le site d'administration]({% url 'admin:projects_editionform_changelist' %}).
{% endblock %}
