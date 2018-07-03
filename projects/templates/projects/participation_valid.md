{% extends 'projects/to_user.md' %}

{% block body %}
Nous venons de valider ton dossier pour {{ edition }} : celui-ci est bien complet ! ✅

Une fois la période des inscriptions terminée, nous étudierons chaque demande
avec soin pour établir la liste des inscrits. Cela se fera à partir du {{ edition.edition_form.deadline | date }}.

Nous te recontacterons alors pour te confirmer ta participation.
{% endblock %}
