from src.api.auth import create_email_verification_token, create_reset_password_token
from src.models.schemas.users import UserSchema
from src.utils.email import build_verification_email, build_recovery_password_mail
from src.utils.abstract.email_sender_repository import EmailSenderRepository


class EmailSenderService:
    def __init__(self, repository: EmailSenderRepository):
        self.repository = repository

    def send_verification_email(self, user: UserSchema):
        token = create_email_verification_token(user.id)
        email = build_verification_email(token)
        data = self.repository.send_email(user.email, email)

    def send_reset_password_email(self, user: UserSchema):
        token = create_reset_password_token(user.id)
        email = build_recovery_password_mail(token)
        data = self.repository.send_email(user.email, email)
