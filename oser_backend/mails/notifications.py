"""Generic notification functionalities."""

import os
from typing import Callable, List

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from logs import get_logger
from markdown import markdown

logger = get_logger('notifications')


def send_notification(subject, message, recipient_list,
                      html=True, **kwargs) -> bool:
    """Send an email from the configured MAILS_NOTIFICATIONS_ADDRESS.

    If MAILS_ENABLED is not True, does nothing.

    Returns
    -------
    sent : bool

    """
    recipients = ', '.join(recipient_list)
    if not settings.MAILS_ENABLED:
        logger.warning(
            ('Email "%s" not sent to %s because'
             'MAILS_ENABLED is set to False'), subject, recipients)
        return False
    if html:
        kwargs['html_message'] = message
        message = strip_tags(message)
    send_mail(subject, message, settings.MAILS_NOTIFICATIONS_ADDRESS,
              recipient_list, **kwargs)
    logger.info('Sent email "%s" to %s', subject, recipients)
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
    send_function : callable, optional
        The function used to send the actual notification email.
        Required signature:
            (subject, message, recipient_list, **kwargs) -> None
    """

    template_name: str
    subject: str
    recipients: List[str] = []

    subject_format: str = '[OSER] {subject}'
    send_function: Callable = send_notification
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

    def send(self) -> dict:
        """Send the notification email.

        Returns
        -------
        results : dict
            Contains the kwargs, the recipients and the sent date.

        """
        subject = self.subject_format.format(subject=self.get_subject())
        message = self.render()
        if self.forced:
            recipients = self.recipients
        else:
            recipients = self.get_recipients()
        sent = type(self).send_function(
            subject, message, recipients, html=self.html)
        result = {
            **self.kwargs,
            'recipients': recipients,
            'sent': sent,
        }
        if sent:
            result['timestamp'] = timezone.now()
        return result

    @classmethod
    def example(cls):
        """Return an example notification instance."""
        raise NotImplementedError
