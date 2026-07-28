from dataclasses import dataclass


@dataclass(slots=True)
class GameConfig:
    """
    Global game configuration.
    """

    # -----------------------------
    # Players
    # -----------------------------

    min_players: int = 2
    max_players: int = 10

    # -----------------------------
    # Chips
    # -----------------------------

    starting_chips: int = 1000

    # -----------------------------
    # Blinds
    # -----------------------------

    small_blind: int = 10
    big_blind: int = 20

    # -----------------------------
    # Betting
    # -----------------------------

    minimum_raise: int = 20

    # -----------------------------
    # Tournament
    # -----------------------------

    blind_increase_rounds: int = 10

    # -----------------------------
    # AI
    # -----------------------------

    monte_carlo_simulations: int = 5000

    think_time: float = 0.5