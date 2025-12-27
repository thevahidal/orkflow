from .base import StateGuard


class GuardRegistry:
    _registry = {}

    @classmethod
    def register(cls, name: str, guard: type[StateGuard]):
        cls._registry[name] = guard

    @classmethod
    def get(cls, name: str) -> StateGuard | None:
        guard_cls = cls._registry.get(name)
        return guard_cls() if guard_cls else None
