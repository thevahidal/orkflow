from django.apps import AppConfig
from decouple import config


class OmsDemoConfig(AppConfig):
    name = "oms_demo"

    def ready(self):
        from core.strategies import StrategyRegistry
        from oms_demo.strategies import MailerooEmailStrategy

        registry = StrategyRegistry()
        registry.register(
            "maileroo_email",
            MailerooEmailStrategy(
                api_key=config(
                    "MAILEROO_API_KEY",
                ),
            ),
        )
