from models.player import Player
from models.pot import Pot


class PotManager:
    """
    Manages the main pot and all side pots.
    """

    def __init__(self):

        self.main_pot = Pot()

        self.side_pots: list[Pot] = []

    # -------------------------------------------------

    def reset(self):
        """
        Reset all pots for a new hand.
        """

        self.main_pot.clear()

        self.side_pots.clear()

    # -------------------------------------------------

    def add_to_main_pot(
        self,
        player: Player,
        amount: int
    ):
        """
        Add chips to the main pot.
        """

        self.main_pot.add_chips(amount)

        self.main_pot.add_player(player)

    # -------------------------------------------------

    def create_side_pot(self):

        pot = Pot()

        self.side_pots.append(pot)

        return pot

    # -------------------------------------------------

    def total_pot(self):
        """
        Returns total chips in all pots.
        """

        total = self.main_pot.amount

        for pot in self.side_pots:
            total += pot.amount

        return total

    # -------------------------------------------------

    def get_all_pots(self):

        return [self.main_pot] + self.side_pots

    # -------------------------------------------------

    def __str__(self):

        text = []

        text.append(
            f"Main Pot : ${self.main_pot.amount}"
        )

        for i, pot in enumerate(
            self.side_pots,
            start=1
        ):

            text.append(
                f"Side Pot {i} : ${pot.amount}"
            )

        return "\n".join(text)