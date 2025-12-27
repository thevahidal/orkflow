from typing import Type, Dict

from .base import BaseStrategy


class StrategyRegistry:
    _strategies: Dict[str, Type[BaseStrategy]] = {}

    @classmethod
    def register(cls, name: str, strategy: Type[BaseStrategy]) -> None:
        cls._strategies[name] = strategy

    @classmethod
    def get(cls, name: str) -> Type[BaseStrategy] | None:
        return cls._strategies.get(name)

    @classmethod
    def list(cls) -> list[str]:
        return list(cls._strategies)
