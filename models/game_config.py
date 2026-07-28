from dataclasses import dataclass


@dataclass(slots=True)
class GameConfig:
    """
    Global configuration for a Texas Hold'em game.

    Every configurable value in the game should
    come from this class instead of being hardcoded.
    """

    # ==================================================
    # Players
    # ==================================================

    starting_chips: int = 1000

    minimum_players: int = 2

    maximum_players: int = 9

    # ==================================================
    # Blinds
    # ==================================================

    small_blind: int = 10

    big_blind: int = 20

    blind_increase_interval: int = 10

    blind_multiplier: float = 2.0

    # ==================================================
    # Tournament
    # ==================================================

    eliminate_players: bool = True

    rotate_dealer: bool = True

    # ==================================================
    # AI
    # ==================================================

    monte_carlo_simulations: int = 10000

    thinking_delay: float = 0.5

    # ==================================================
    # UI
    # ==================================================

    show_ai_cards: bool = False

    show_win_probability: bool = True

    show_hand_strength: bool = True

    # ==================================================
    # Debug
    # ==================================================

    debug_mode: bool = False

    # ==================================================
    # Validation
    # ==================================================

    def __post_init__(self):

        if self.minimum_players < 2:
            raise ValueError(
                "Minimum players must be at least 2."
            )

        if self.maximum_players > 9:
            raise ValueError(
                "Texas Hold'em supports a maximum of 9 players."
            )

        if self.small_blind <= 0:
            raise ValueError(
                "Small blind must be positive."
            )

        if self.big_blind <= self.small_blind:
            raise ValueError(
                "Big blind must be greater than the small blind."
            )

        if self.starting_chips <= 0:
            raise ValueError(
                "Starting chips must be positive."
            )

    # ==================================================
    # Utility
    # ==================================================

    def next_blind_level(self):
        """
        Increase blinds for tournament mode.
        """

        self.small_blind = int(
            self.small_blind * self.blind_multiplier
        )

        self.big_blind = int(
            self.big_blind * self.blind_multiplier
        )

    # ==================================================
    # Debug
    # ==================================================

    def __str__(self):

        return (

            "========== GAME CONFIG ==========\n"

            f"Players        : {self.minimum_players}-{self.maximum_players}\n"

            f"Starting Chips : {self.starting_chips}\n"

            f"Blinds         : {self.small_blind}/{self.big_blind}\n"

            f"Tournament     : {self.eliminate_players}\n"

            f"Monte Carlo    : {self.monte_carlo_simulations}\n"

            f"Debug          : {self.debug_mode}"

        )