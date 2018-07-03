{% extends 'projects/to_user.md' %}

{% block body %}
{{ user }} s'est inscrit à {{ edition }}.

Vous pouvez télécharger la feuille des inscrits mise à jour sur [le site d'administration](https://{{ request.get_host }}{% url 'admin:projects_editionform_changelist' %}).
{% endblock %}
