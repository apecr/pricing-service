import os
from typing import List

from requests import Response, post


class MailgunException(Exception):
    def __init__(self, message: str):
        self.message = message


class Mailgun:
    FROM_TITLE = "Princing Service"

    @classmethod
    def send_email(cls, emails: List[str], subject: str, text: str, html: str) -> Response:
        mailgun_api_key = os.environ.get('MAILGUN_API_KEY', None)
        mailgun_domain = os.environ.get('MAILGUN_DOMAIN', None)
        from_email = f"do-not-reply@{mailgun_domain}"
        if mailgun_api_key is None or mailgun_domain is None:
            raise MailgunException('Not getting Mailgun configuration')
        response = post(
            f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
            auth=("api", mailgun_api_key),
            data={"from": f"{cls.FROM_TITLE} <{from_email}>",
                  "to": emails,
                  "subject": subject,
                  "text": text,
                  "html": html})
        if response.status_code != 200:
            raise MailgunException('An error ocurred while sending e-mail')
        return response
