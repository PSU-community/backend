from abc import ABC, abstractmethod

from src.models.email import EmailContent


class EmailSenderRepository(ABC):
    @staticmethod
    @abstractmethod
    def send_email(target_email: str, email: EmailContent):
        raise NotImplementedError
