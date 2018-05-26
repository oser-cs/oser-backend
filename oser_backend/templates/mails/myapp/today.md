{% extends 'mails/notification.md' %}

{% block greeting %}
Hi {{ user.first_name }},
{% endblock %}

{% block body %}
Today is **{{ date|date }}**.
{% endblock %}

{% block signature %}
Cheers,

The Corporate, Inc. team
{% endblock %}
