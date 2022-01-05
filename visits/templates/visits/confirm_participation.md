{% extends 'mails/notification.md' %}

{% block greeting %}
Bonjour{% if participation.user.first_name %} {{ participation.user.first_name }}{% endif %},
{% endblock %}

{% block body %}
{% if participation.submitted %}Le {{ participation.submitted|date }}, tu{% else %}Tu{% endif%} as demandé à t'inscrire à la sortie **{{ participation.visit }}** organisée le **{{ participation.visit.date|date }}**.



{% if participation.accepted %}


Bonne nouvelle : nous avons validé ta participation à la sortie. ✅

Avant la sortie, tu pourras, en te rendant sur [l'espace sorties]({{ participation.visit.get_site_url }}) :

- Consulter les informations pratiques ;
- Télécharger la fiche sortie ;
- Télécharger l'autorisation de sortie, à faire remplir par tes parents.


{% else %}
Malheureusement, en raison du nombre de places limité, tu ne pourras pas participer à cette sortie. 😔

Nous te recontacterons si des places se libèrent suite à des désistements.
{% endif %}
{% endblock %}

{% block signature %}
À très bientôt,  
Les organisateurs  

Nous contacter : oser.sortie@gmail.fr
{% endblock %}
