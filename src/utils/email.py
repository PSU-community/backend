from ..models.email import EmailContent
from ..settings import settings


def build_url(token: str):
    return f"{settings.SITE_URL}/verification?token={token}"


def build_verification_email(jwt_token: str):
    url = build_url(jwt_token)
    message = f"Перейдите по ссылке для подтверждения электронной почты: {url}"

    return EmailContent(
        title="Подтверждение почты PsychoSupport",
        text=message,
    )


def build_recovery_password_mail(jwt_token: str):
    url = build_url(jwt_token)
    message = f"Перейдите по ссылке для сброса пароля: {url}"

    return EmailContent(
        title="Сброс пароля PsychoSupport",
        text=message
    )
