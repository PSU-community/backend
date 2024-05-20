from ..models.email import EmailContent
from ..settings import settings

EMAIL_CONFIRMATION_URL = f"{settings.SITE_URL}/acc-finish?token="
PASSWORD_CHANGE_URL = f"{settings.SITE_URL}/pass-change?token="

def build_verification_email(jwt_token: str):
    url = EMAIL_CONFIRMATION_URL + jwt_token
    message = f"Для подтверждения электронной почты перейдите по <a href={url}>ссылке</a>"

    return EmailContent(
        title="Подтверждение почты Стобой",
        text=message,
    )


def build_recovery_password_mail(jwt_token: str):
    url = PASSWORD_CHANGE_URL + jwt_token
    message = f"Для сброса пароля перейдите по <a href={url}>ссылке</a>"

    return EmailContent(title="Сброс пароля Стобой", text=message)
