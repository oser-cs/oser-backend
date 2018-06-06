# Emails

This application allows you to easily send notification emails using Markdown templates.

## Quick start

### Write the template

- Create a templates folder for your emails, e.g. `templates/mails` (depending on your `TEMPLATE_DIRS` configuration).
- Create the text template file, e.g. in `mails/myapp/today.md`
- In the template, extend the base notification template and define the `body` block:

```
{% extends 'mails/notification.md' %}

{% block body %}
Today is {{ date|date }}.
{% endblock %}
```

- You can define the greeting and signature in the `greeting` and `signature` blocks respectively. For example:

```
{% block greeting %}
Hi {{ user.first_name }},
{% endblock %}

{% block signature %}
Cheers,

The Corporate, Inc. team
{% endblock %}
```

### Write the notification class

```py
# myapp/notifications.py
from mails import Notification

class Today(Notification):

  template_name = 'mails/myapp/today.md'
  args = ('user', 'date',)
  subject = "What's the date today?"

  def get_recipients(self):
    return [self.user.email]
```

### (Optional) Provide an example notification

You can define the `.example()` class method on the notification class.

If your template requires access to model instances, you should create them without saving them to the database.

```py
# myapp/notifications.py

class Today(Notification):

  ...

  @classmethod
  def example(cls):
      user = User(first_name='John', email='john.doe@example.com')
      return cls(user=user, date=now())
```

If your notification uses complex context (such as accessing foreign keys or M2M fields on a model instance), you should define a helper method and call it in `.get_context()`. It allows you to create the example notification by subclassing and overriding the helper method to return a mock result. For example:

```py
class NewUser(Notification):

    ...
    args = ('user',)

    def get_groups(self):
        return self.user.groups.all().values_list('name', flat=True)

    def get_context(self):
        context = super().get_context()
        context['groups'] = self.get_groups()
        return context

    @classmethod
    def example(cls):
        class Example(cls):
            def get_groups(self):
                return ['Admins', 'Reviewers']
        user = User(email='john.doe@example.com')
        return Example(user=user)
```

## Usage

### Send notifications in code

```py
# myapp/business.py
from myapp.notifications import Today
from django.utils.timezone import now

def perform_business(user):
    # ...
    Today(user=user, date=now()).send()
    # ...
```

### `rendernotification` : check the HTML rendering of the example notification

If you want to see how your notification will render without sending it, you can do it in code directly:

```py
>>> from myapp.notifications import Today
>>> from django.utils.timezone import now
>>> from users.models import User
>>> user = User.objects.first()
>>> notification = Today(user=user, date=now())
>>> print(notification.render())
```
```
Hi John,

Today is <strong>May 26, 2018</strong>.

Cheers,

The Corporate, Inc. team.

P.S. : this is an automatic email, please do not reply.
```

Alternatively, if the `.example()` class method is defined you can use
the `rendernotification` management command:

```sh
$ python manage.py rendernotification myapp.notifications.Today
```

### `sendnotification`: send the example notification

If the notification defines `.example()`, you can use the `sendnotification` management command to send the example notification to someone. In this case, the recipient list is forced to the `recipient` you provide, and the definitions for `recipients` or `.get_recipients()` on the notification will be ignored.

```
$ python manage.py sendnotification myapp.notifications.Today john.doe@example.com
✉️ Notification email sent to john.doe@example.com.
```
