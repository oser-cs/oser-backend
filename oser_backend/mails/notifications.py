"""Generic notification functionalities."""

import os
from typing import List

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils import translation

from markdown import markdown

from .signals import app_disabled, delivered, notification_sent, failed


def send_notification(subject, message, recipient_list,
                      html=True, **kwargs) -> bool:
    """Send an email from the configured MAILS_NOTIFICATIONS_ADDRESS.

    If MAILS_ENABLED is not True, does nothing.

    Returns
    -------
    sent : bool

    Signals
    -------
    mails_disabled :
        If the mails app is not enabled (MAILS_ENABLED is not True).
    mail_delievered :
        After the mail has been successfully sent.

    """
    if not settings.MAILS_ENABLED:
        app_disabled.send(None, subject=subject,
                          recipient_list=recipient_list)
        return False

    if html:
        kwargs['html_message'] = message
        message = strip_tags(message)

    mail_from = settings.MAILS_NOTIFICATIONS_ADDRESS

    try:
        send_mail(subject, message, mail_from, recipient_list, **kwargs)
    except Exception as e:
        failed.send(None, exception=e)
        return False

    delivered.send(None, mail_from=mail_from,
                   recipient_list=recipient_list, subject=subject)

    return True


def checkattr(attr):
    """Check for an AttributeError or raise a meaningful error message."""
    def decorate(f):
        def decorated(self, *args, **kwargs):
            try:
                return f(self, *args, **kwargs)
            except AttributeError as e:
                message = f'{attr} not set on {self.__class__.__name__}'
                raise AttributeError(message) from e
        return decorated
    return decorate


class Notification:
    """Generic notification handler.

    Class attributes
    ----------------
    args : sequence of str, optional
        Determines what keyword arguments the constructor will expect, and
        what the template context will be
        (unless `.get_context()` has been overriden).
    template_name : str
        Name of the template used to render the notification.
        Must be resolvable by Django's template loader.
    subject : str
        The notification email subject.
        You can also override `.get_subject()`.
    recipients : list of str
        A list of recipients to send the notification to.
        You can also override `.get_recipients()`.
    subject_format : str, optional
        The notification email subject format string.
        Should contain a `subject` key.
    """

    template_name: str
    subject: str
    recipients: List[str] = []

    subject_format: str = '[OSER] {subject}'
    args: List[str] = ()

    def __init__(self, **kwargs):
        """Create a notification object.

        Parameters
        ----------
        **kwargs : dict

        """
        self.kwargs = {}
        for arg in self.args:
            try:
                value = kwargs[arg]
            except KeyError as e:
                message = (
                    f"{self.__class__.__name__} expected the argument '{arg}'"
                )
                raise TypeError(message) from e
            self.kwargs[arg] = value
            setattr(self, arg, value)
        self.html = False
        self.forced = False
        self.sent = None
        self.timestamp = None

    @checkattr('template_name')
    def get_template(self) -> str:
        """Return the name of the template."""
        return self.template_name

    @checkattr('subject')
    def get_subject(self) -> str:
        """Return the notification subject."""
        return self.subject

    def get_context(self) -> dict:
        """Return the template context.

        Return the notifier kwargs by default.
        """
        return self.kwargs

    def adapt(self, content, template_name):
        """Adapt the content depending on the template's extension."""
        filename, file_extension = os.path.splitext(template_name)
        html = False
        if file_extension == '.md':
            content = markdown(content)
            html = True
        elif file_extension == '.html':
            html = True
        return content, html

    def render(self) -> str:
        """Render the template and return the notification message body."""
        translation.activate('fr_FR')  # force usage of French
        template = self.get_template()
        context = self.get_context()
        content = render_to_string(template, context)
        content, html = self.adapt(content, template)
        self.html = html
        return content

    @checkattr('recipients')
    def get_recipients(self) -> List[str]:
        """Return the list of recipients."""
        return self.recipients

    def force_recipients(self, recipients: List[str]):
        """Set the recipient list."""
        self.recipients = recipients
        self.forced = True

    def send(self) -> None:
        """Send the notification email."""
        subject = self.subject_format.format(subject=self.get_subject())
        # Subject must not be longer than 78 characters
        # See https://github.com/sendgrid/sendgrid-python/issues/187
        subject = Truncator(subject).chars(75)
        message = self.render()

        if self.forced:
            recipients = self.recipients
        else:
            recipients = self.get_recipients()

        self.sent = send_notification(
            subject, message, recipients, html=self.html)
        self.timestamp = timezone.now()

        if self.sent:
            notification_sent.send(sender=self.__class__, instance=self)

    @classmethod
    def example(cls):
        """Return an example notification instance."""
        raise NotImplementedError
