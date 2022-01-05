{% extends 'mails/notification.md' %}

{% block greeting %}
Bonjour{% if participation.user.first_name %} {{ participation.user.first_name }}{% endif %},
{% endblock %}

{% block body %}
{% if participation.submitted %}Le {{ participation.submitted|date }}, tu{% else %}Tu{% endif%} as demandé à t'inscrire à la sortie **{{ participation.visit }}** organisée le **{{ participation.visit.date|date }}**.


Malheureusement, en raison du nombre de places limité, tu es sur liste d'attente pour participer à cette sortie. 😔

Nous te recontacterons si des places se libèrent suite à des désistements.

{% endblock %}

{% block signature %}
À très bientôt,  
Les organisateurs  

Nous contacter : oser.sortie@gmail.fr
{% endblock %}
