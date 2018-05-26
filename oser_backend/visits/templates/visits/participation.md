{% extends 'mails/notification.md' %}

{% block greeting %}
Bonjour{% if user.first_name %} {{ user.first_name }}{% endif %},
{% endblock %}

{% block body %}
Tu as demandé à t'inscrire à la sortie **{{ visit.title }}** organisée le **{{ visit.date|date }}**.

{% if accepted %}
Bonne nouvelle : nous avons validé ta participation à la sortie. ✅

En te rendant sur [l'espace sorties]({{ visit.get_site_url }}), tu peux dès à présent:

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
