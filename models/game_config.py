from dataclasses import dataclass

from models.betting_structure import BettingStructure

@dataclass(slots=True)
class GameConfig:
    """
    Global configuration for Texas Hold'em.

    Single source of truth for:

    - Player limits
    - Chips
    - Blinds
    - Betting rules
    - Tournament settings
    - AI settings
    - UI settings
    - Debug options
    """

    # ==================================================
    # Players
    # ==================================================

    starting_chips: int = 1000

    minimum_players: int = 2

    maximum_players: int = 9

    # ==================================================
    # Betting Structure
    # ==================================================

    betting_structure: BettingStructure = (
        BettingStructure.NO_LIMIT
    )

    # Fixed Limit support

    small_bet: int = 20

    big_bet: int = 40

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

    tournament_mode: bool = False

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

        if self.starting_chips <= 0:

            raise ValueError(
                "Starting chips must be positive."
            )

        if self.minimum_players < 2:

            raise ValueError(
                "Minimum players must be at least 2."
            )

        if self.maximum_players > 9:

            raise ValueError(
                "Texas Hold'em supports maximum 9 players."
            )

        if self.minimum_players > self.maximum_players:

            raise ValueError(
                "Minimum players cannot exceed maximum players."
            )

        if self.small_blind <= 0:

            raise ValueError(
                "Small blind must be positive."
            )

        if self.big_blind <= self.small_blind:

            raise ValueError(
                "Big blind must be greater than small blind."
            )

        if self.blind_increase_interval <= 0:

            raise ValueError(
                "Blind increase interval must be positive."
            )

        if self.blind_multiplier <= 1:

            raise ValueError(
                "Blind multiplier must be greater than 1."
            )

        if self.small_bet <= 0:

            raise ValueError(
                "Small bet must be positive."
            )

        if self.big_bet <= self.small_bet:

            raise ValueError(
                "Big bet must be greater than small bet."
            )

        if self.monte_carlo_simulations <= 0:

            raise ValueError(
                "Monte Carlo simulations must be positive."
            )

        if not isinstance(
            self.betting_structure,
            BettingStructure
        ):

            raise ValueError(
                "Invalid betting structure."
            )

    # ==================================================
    # Betting Helpers
    # ==================================================

    @property
    def is_no_limit(self) -> bool:

        return (
            self.betting_structure
            ==
            BettingStructure.NO_LIMIT
        )

    # --------------------------------------------------

    @property
    def is_pot_limit(self) -> bool:

        return (
            self.betting_structure
            ==
            BettingStructure.POT_LIMIT
        )

    # --------------------------------------------------

    @property
    def is_fixed_limit(self) -> bool:

        return (
            self.betting_structure
            ==
            BettingStructure.FIXED_LIMIT
        )

    # ==================================================
    # Game Modes
    # ==================================================

    @property
    def is_heads_up(self) -> bool:

        return self.maximum_players == 2

    # ==================================================
    # Betting Calculation
    # ==================================================

    def calculate_max_raise(
        self,
        pot_size: int,
        call_amount: int
    ):
        """
        Calculate maximum legal raise.

        Returns:

        No Limit:
            None

        Pot Limit:
            Pot + Call

        Fixed Limit:
            Fixed bet size
        """

        if self.is_no_limit:

            return None

        if self.is_pot_limit:

            return (

                pot_size

                +

                call_amount

            )

        if self.is_fixed_limit:

            return self.big_bet

    # ==================================================
    # Tournament
    # ==================================================

    def next_blind_level(self):
        """
        Increase tournament blinds.
        """

        self.small_blind = int(

            self.small_blind

            *

            self.blind_multiplier

        )

        self.big_blind = int(

            self.big_blind

            *

            self.blind_multiplier

        )

    # ==================================================
    # Debug
    # ==================================================

    def __str__(self):

        return (

            "========== GAME CONFIG ==========\n"

            f"Players        : "
            f"{self.minimum_players}-{self.maximum_players}\n"

            f"Starting Chips : "
            f"{self.starting_chips}\n"

            f"Structure      : "
            f"{self.betting_structure}\n"

            f"Blinds         : "
            f"{self.small_blind}/{self.big_blind}\n"

            f"Tournament     : "
            f"{self.tournament_mode}\n"

            f"Monte Carlo    : "
            f"{self.monte_carlo_simulations}\n"

            f"Debug          : "
            f"{self.debug_mode}"

        )