from enum import Enum

class Strategy(Enum):
    """
    Poker AI playing personalities.
    Controls:
    - aggression
    - bluff frequency
    - risk tolerance
    - range width
    - pressure style
    """
    TIGHT_AGGRESSIVE = "tight_aggressive"
    LOOSE_AGGRESSIVE = "loose_aggressive"
    TIGHT_PASSIVE = "tight_passive"
    BALANCED = "balanced"
    ADAPTIVE = "adaptive"
    CALLING_STATION = "calling_station"

class StrategyConfig:
    """
    Configuration for AI personalities.
    """
    CONFIG = {
        Strategy.TIGHT_AGGRESSIVE: {
            "range_width": 0.20,
            "aggression": 0.85,
            "bluff_frequency": 0.15,
            "risk_tolerance": 0.60,
            "pressure_factor": 0.80,
            "adaptability": 0.50,
            "description": "Selective starting range with strong aggression"
        },
        Strategy.LOOSE_AGGRESSIVE: {
            "range_width": 0.45,
            "aggression": 0.95,
            "bluff_frequency": 0.30,
            "risk_tolerance": 0.85,
            "pressure_factor": 1.00,
            "adaptability": 0.70,
            "description": "Wide range, high pressure and frequent aggression"
        },
        Strategy.TIGHT_PASSIVE: {
            "range_width": 0.18,
            "aggression": 0.30,
            "bluff_frequency": 0.05,
            "risk_tolerance": 0.25,
            "pressure_factor": 0.30,
            "adaptability": 0.30,
            "description": "Selective defensive playing style"
        },
        Strategy.BALANCED: {
            "range_width": 0.30,
            "aggression": 0.55,
            "bluff_frequency": 0.20,
            "risk_tolerance": 0.50,
            "pressure_factor": 0.55,
            "adaptability": 0.80,
            "description": "Balanced strategy adapting to situations"
        },
        Strategy.ADAPTIVE: {
            "range_width": 0.35,
            "aggression": 0.60,
            "bluff_frequency": 0.25,
            "risk_tolerance": 0.55,
            "pressure_factor": 0.60,
            "adaptability": 1.00,
            "description": "Changes behaviour based on opponents"
        },
        Strategy.CALLING_STATION: {
            "range_width": 0.60,
            "aggression": 0.15,
            "bluff_frequency": 0.02,
            "risk_tolerance": 0.90,
            "pressure_factor": 0.20,
            "adaptability": 0.10,
            "description": "Plays wide range, calls bets, rarely raises or folds"
        }
    }

    @classmethod
    def get_config(cls, strategy: Strategy) -> dict:
        """Return strategy configuration."""
        return cls.CONFIG.get(strategy, cls.CONFIG[Strategy.BALANCED])

    @classmethod
    def available_strategies(cls):
        return list(cls.CONFIG.keys())

class StrategyManager:
    """
    Handles AI playing personality.
    """
    def __init__(self, strategy: Strategy = Strategy.BALANCED):
        self.strategy = strategy
        self.overrides = {}

    def config(self):
        base = StrategyConfig.get_config(self.strategy).copy()
        base.update(self.overrides)
        return base

    def range_width(self) -> float:
        return self.get_parameter("range_width", 0.30)

    def aggression(self) -> float:
        return self.get_parameter("aggression", 0.55)

    def bluff_frequency(self) -> float:
        return self.get_parameter("bluff_frequency", 0.20)

    def risk_tolerance(self) -> float:
        return self.get_parameter("risk_tolerance", 0.50)

    def pressure_factor(self) -> float:
        return self.get_parameter("pressure_factor", 0.55)

    def adaptability(self) -> float:
        return self.get_parameter("adaptability", 0.80)

    def profile(self) -> dict:

        cfg = self.config()
        return {
            "strategy": self.strategy.value if hasattr(self.strategy, "value") else str(self.strategy),
            "description": cfg.get("description", ""),
            "parameters": cfg
        }

    def get_parameter(self, param_name: str, default=0.5):
        cfg = self.config()
        return cfg.get(param_name, default)

    def set_override(self, param_name: str, value: float):
        self.overrides[param_name] = value

    def clear_overrides(self):
        self.overrides.clear()
