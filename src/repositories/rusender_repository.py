import requests

from ..models.email import EmailContent
from src.utils.abstract.email_sender_repository import EmailSenderRepository
from ..settings import settings

ENDPOINT = "https://api.beta.rusender.ru/api/v1/external-mails/send"


class RuSenderRepository(EmailSenderRepository):
    @staticmethod
    def send_email(target_email: str, email: EmailContent):
        payload = {
            "mail": {
                "to": {"email": target_email, "name": "user"},
                "from": {"email": "no-reply@damego.ru", "name": "Стобой"},
                "subject": email.title,
                "html": email.text,
            }
        }
        response = requests.post(
            ENDPOINT, json=payload, headers={"X-Api-Key": settings.RUSENDER_API_KEY}
        )

        if response.status_code == 200:
            return response.json()

        print(response.json())
        # TODO: provide 4xx handler https://rusender.ru/developer/api/email/
