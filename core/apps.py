from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "core"

    def ready(self):
        from core.strategies.python_function import PythonFunctionStrategy
        from core.strategies.registry import StrategyRegistry

        strategy_registry = StrategyRegistry()

        strategy_registry.register(
            "python_function",
            PythonFunctionStrategy(),
        )
