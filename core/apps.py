from django.apps import AppConfig

from core.strategies.python_function import PythonFunctionStrategy
from core.strategies.registry import StrategyRegistry


class CoreConfig(AppConfig):
    name = "core"

    def ready(self):
        strategy_registry = StrategyRegistry()

        strategy_registry.register_strategy(
            "python_function",
            PythonFunctionStrategy(),
        )
