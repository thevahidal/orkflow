import logging
from smtplib import SMTP
from typing import TYPE_CHECKING, Dict, Any

from django.core.exceptions import ValidationError
import requests

from core.models import Action
from core.strategies.base import BaseMetadataSchema, BaseStrategy

if TYPE_CHECKING:
    from django.db.models import Model


logger = logging.getLogger(__name__)


class MailerooEmailStrategy(BaseStrategy):
    class MetadataSchema(BaseMetadataSchema):
        to: str
        subject: str
        body: str

    def __init__(self, *, api_key: str):
        self.sender = "info@orkflow.com"
        self.api_key = api_key

    def _send_email(self, *, to: str, subject: str, body: str):
        try:
            return requests.post(
                "https://smtp.maileroo.com/api/v2/emails",
                headers={"X-Api-Key": self.api_key},
                json={
                    "from": {
                        "address": self.sender,
                    },
                    "to": [
                        {
                            "address": to,
                        }
                    ],
                    "subject": subject,
                    "plain": body,
                },
            )
        except Exception as error:
            logger.exception(error)
            raise ValidationError(error)

    def execute(
        self, instance: "Model", action: Action, inputs: Dict[str, Any], *args, **kwargs
    ) -> None:
        metadata = super().execute(instance, action, inputs)

        response = self._send_email(
            to=metadata.to,
            subject=metadata.subject,
            body=metadata.body,
        )
        return response
