{% extends 'mails/notification.md' %}

{% block body %}
{{ user }} s'est désinscrit(e) de la sortie **{{ visit }}** organisée le **{{ visit.date|date }}**. Voici la raison de son désistement :

> {{ reason }}

Vous pouvez contacter {{ user }} grâce à son adresse mail : {{ user.email }}.
{% endblock %}
