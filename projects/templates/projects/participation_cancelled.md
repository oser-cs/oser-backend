{% extends 'projects/to_user.md' %}

{% block body %}
Ta participation à {{ edition }} a bien été annulée.

Si tu souhaites réactiver ta demande de participation, tu peux le faire
avant le {{ edition.edition_form.deadline | date }} dans la section
[Mes inscriptions]({{ edition.get_registration_url }}).
{% endblock %}
