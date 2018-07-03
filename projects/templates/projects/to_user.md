{% extends 'mails/notification.md' %}

{% block greeting %}
Bonjour{% if participation.user.first_name %} {{ participation.user.first_name }}{% endif %},
{% endblock %}

{% block signature %}
À très bientôt,

Les organisateurs
{% endblock %}
