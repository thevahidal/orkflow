from django.apps import AppConfig
from decouple import config


class OmsDemoConfig(AppConfig):
    name = "oms_demo"

    def ready(self):
        from core.strategies import StrategyRegistry
        from oms_demo.strategies import MailerooEmailStrategy

        registry = StrategyRegistry()
        registry.register_strategy(
            "maileroo_email",
            MailerooEmailStrategy(
                smtp_server=config("MAILEROO_SMTP_SERVER", default="smtp.maileroo.com"),
                smtp_port=config("MAILEROO_SMTP_PORT", default=587, cast=int),
                username=config("MAILEROO_USERNAME", default=""),
                password=config("MAILEROO_PASSWORD", default=""),
            ),
        )
