class StrategyRegistry:
    _instance = None
    _strategies = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StrategyRegistry, cls).__new__(cls)
        return cls._instance

    def register_strategy(self, name, strategy):
        self._strategies[name] = strategy

    def get_strategy(self, name):
        return self._strategies.get(name)

    def list_strategies(self):
        return list(self._strategies.keys())
