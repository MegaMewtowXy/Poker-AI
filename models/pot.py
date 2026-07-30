from dataclasses import dataclass, field

from models.player import Player

@dataclass(slots=True)
class Pot:
    """
    Represents a poker pot.

    Supports:
    - Main pot
    - Side pots
    - Multiple winners
    - Split payouts
    - Tournament tracking

    Does NOT:
    - Decide winners
    - Build side pots
    - Handle betting
    """

    # =====================================================
    # Identity
    # =====================================================

    pot_id: int = 0

    is_main_pot: bool = False

    # =====================================================
    # Chips
    # =====================================================

    amount: int = 0

    # =====================================================
    # Eligibility
    # =====================================================

    eligible_players: list[Player] = field(
        default_factory=list
    )

    # =====================================================
    # Showdown Result
    # =====================================================

    winners: list[Player] = field(
        default_factory=list
    )

    payouts: dict[Player, int] = field(
        default_factory=dict
    )

    # =====================================================
    # State
    # =====================================================

    closed: bool = False

    # =====================================================
    # Chip Management
    # =====================================================

    def add_chips(
        self,
        amount: int
    ):

        self._validate_amount(amount)

        if self.closed:

            raise RuntimeError(
                "Cannot add chips to closed pot."
            )

        self.amount += amount

    # -----------------------------------------------------

    def remove_chips(
        self,
        amount: int
    ):

        self._validate_amount(amount)

        if amount > self.amount:

            raise ValueError(
                "Not enough chips in pot."
            )

        self.amount -= amount

    # =====================================================
    # Eligibility
    # =====================================================

    def add_player(
        self,
        player: Player
    ):

        if player not in self.eligible_players:

            self.eligible_players.append(
                player
            )

    # -----------------------------------------------------

    def remove_player(
        self,
        player: Player
    ):

        if player in self.eligible_players:

            self.eligible_players.remove(
                player
            )

    # -----------------------------------------------------

    def is_eligible(
        self,
        player: Player
    ) -> bool:

        return player in self.eligible_players

    # =====================================================
    # Winner Handling
    # =====================================================

    def set_winners(
        self,
        winners: list[Player]
    ):

        self.winners = winners

    # -----------------------------------------------------

    def award(
        self,
        player: Player,
        amount: int
    ):

        self._validate_amount(amount)

        if amount > self.amount:

            raise ValueError(
                "Payout exceeds pot size."
            )

        self.payouts[player] = (

            self.payouts.get(
                player,
                0
            )

            +

            amount

        )

    # -----------------------------------------------------

    def split_amount(
        self,
        winners: list[Player]
    ) -> dict[Player, int]:

        if not winners:

            return {}

        share = self.amount // len(winners)

        remainder = self.amount % len(winners)

        result = {}

        for index, player in enumerate(winners):

            result[player] = share

            if index < remainder:

                result[player] += 1

        return result

    # =====================================================
    # Lifecycle
    # =====================================================

    def close(self):

        self.closed = True

    # -----------------------------------------------------

    def clear(self):

        self.amount = 0

        self.eligible_players.clear()

        self.winners.clear()

        self.payouts.clear()

        self.closed = False

    # =====================================================
    # Information
    # =====================================================

    def player_count(self):

        return len(
            self.eligible_players
        )

    # -----------------------------------------------------

    def winner_count(self):

        return len(
            self.winners
        )

    # -----------------------------------------------------

    def is_empty(self):

        return self.amount == 0

    # -----------------------------------------------------

    def total_paid(self):

        return sum(
            self.payouts.values()
        )

    # -----------------------------------------------------

    def remaining_amount(self):

        return (

            self.amount

            -

            self.total_paid()

        )

    # =====================================================
    # Serialization
    # =====================================================

    def to_dict(self):

        return {

            "pot_id": self.pot_id,

            "amount": self.amount,

            "main_pot": self.is_main_pot,

            "eligible_players": [

                p.name

                for p in self.eligible_players

            ],

            "winners": [

                p.name

                for p in self.winners

            ],

            "payouts": {

                p.name: amount

                for p, amount in self.payouts.items()

            },

            "closed": self.closed

        }

    # =====================================================
    # Validation
    # =====================================================

    def _validate_amount(
        self,
        amount
    ):

        if amount < 0:

            raise ValueError(
                "Amount cannot be negative."
            )

    # =====================================================
    # Debug
    # =====================================================

    def __repr__(self):

        return (

            "Pot("

            f"id={self.pot_id}, "

            f"amount={self.amount}, "

            f"main={self.is_main_pot}"

            ")"

        )

    # -----------------------------------------------------

    def __str__(self):

        return (

            f"Pot #{self.pot_id}\n"

            f"Amount: ${self.amount}\n"

            f"Players: {self.player_count()}\n"

            f"Closed: {self.closed}"

        )