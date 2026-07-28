from dataclasses import dataclass, field

from models.player import Player


@dataclass(slots=True)
class Pot:
    """
    Represents a poker pot.

    A game always has one main pot and may have
    multiple side pots.

    Each pot tracks:
    - Amount of chips
    - Players eligible to win it
    """

    amount: int = 0

    eligible_players: list[Player] = field(
        default_factory=list
    )

    # =====================================================
    # Chip Management
    # =====================================================

    def add_chips(
        self,
        amount: int
    ):

        if amount < 0:
            raise ValueError(
                "Cannot add negative chips."
            )

        self.amount += amount

    # -----------------------------------------------------

    def remove_chips(
        self,
        amount: int
    ):

        if amount < 0:
            raise ValueError(
                "Cannot remove negative chips."
            )

        if amount > self.amount:
            raise ValueError(
                "Not enough chips in pot."
            )

        self.amount -= amount

    # =====================================================
    # Eligible Players
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

    # =====================================================
    # Reset
    # =====================================================

    def clear(self):

        self.amount = 0

        self.eligible_players.clear()

    # =====================================================
    # Information
    # =====================================================

    def player_count(self):

        return len(
            self.eligible_players
        )

    # -----------------------------------------------------

    def is_empty(self):

        return self.amount == 0

    # =====================================================
    # Debug
    # =====================================================

    def __repr__(self):

        players = ", ".join(

            player.name

            for player in self.eligible_players

        )

        return (

            f"Pot("

            f"amount={self.amount}, "

            f"eligible=[{players}]"

            f")"

        )