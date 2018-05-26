# Email templates

This directory contains text templates for automatic emails and notifications. This readme takes you through the process of writing and using a template to send notification emails.

## Write a notification template

- As a best practice, create a folder named after the application you are sending an email from
- Create the text template file, e.g. `mails/myapp/today.txt`
- In the template, extend the base notification template and define the `body` block:

```
{% extends 'mails/notification.txt' %}

{% block body %}
Today is {{ date|date }}.
{% endblock %}
```

- You may customize the greeting, signature and postscriptum by overriding the `greeting`, `signature` and `postscriptum` blocks respectively. For example:

```
{% block signature %}À bientôt,

Le secteur Geek
{% endblock %}
```

> Please note that any line break will be as-is in the final rendered email.

## Check the rendering

This can be done in the Django shell:

```
$ python manage.py shell
>>> from django.template.loader import render_to_string
>>> from django.utils.timezone import now
>>> print(render_to_string('mails/myapp/today.txt', {'date': now()}))
Bonjour,

Today is May 26, 2018.

À bientôt,

Le site OSER

P.S. : ceci est un email automatique du service de notifications.

>>>
```

## Use your template to send an email

```python
from django.core.mail import send_mail
from django.utils.timezone import now

context = {'date': now()}

plain_message = render_to_string('mails/myapp/today.txt', context)

send_mail_notification(
    subject='Ever wondered what the date was?',
    message=plain_message,
    recipient_list=['some.user@example.com'])
```
