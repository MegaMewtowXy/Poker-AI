from collections import defaultdict

from models.player import Player
from models.pot import Pot


class PotManager:
    """
    Manages the main pot and every side pot.

    Responsibilities
    ----------------
    • Track each player's total contribution.
    • Build side pots.
    • Determine eligible players.
    • Award chips.
    """

    def __init__(self):

        self.main_pot = Pot()

        self.side_pots: list[Pot] = []

        # Total contribution for the current hand
        self.contributions: dict[Player, int] = defaultdict(int)

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.main_pot.clear()

        self.side_pots.clear()

        self.contributions.clear()

    # =====================================================
    # Contributions
    # =====================================================

    def add_to_main_pot(
        self,
        player: Player,
        amount: int
    ):

        if amount <= 0:
            return

        self.main_pot.add_chips(amount)

        self.main_pot.add_player(player)

        self.contributions[player] += amount

    # =====================================================

    def player_contribution(
        self,
        player: Player
    ) -> int:

        return self.contributions[player]

    # =====================================================

    def total_pot(self) -> int:

        total = self.main_pot.amount

        for pot in self.side_pots:

            total += pot.amount

        return total

    # =====================================================

    def all_players(self):

        return list(
            self.contributions.keys()
        )

    # =====================================================

    def players_sorted_by_contribution(self):

        return sorted(

            self.contributions.items(),

            key=lambda x: x[1]

        )

    # =====================================================

    def clear_side_pots(self):

        self.side_pots.clear()
    # =====================================================
    # Side Pot Construction
    # =====================================================

    def build_side_pots(self):
        """
        Build the main pot and all side pots from
        every player's total contribution.

        Example

        A -> 100
        B -> 300
        C -> 700

        Main Pot : 300
        Side Pot1: 400
        Side Pot2: 400
        """

        self.main_pot.clear()

        self.side_pots.clear()

        # Active contributors only
        contributors = [

            (player, chips)

            for player, chips in self.contributions.items()

            if chips > 0

        ]

        if not contributors:
            return

        contributors.sort(
            key=lambda x: x[1]
        )

        previous_level = 0

        remaining_players = [

            player

            for player, _ in contributors

        ]

        first_pot = True

        for player, contribution in contributors:

            layer = contribution - previous_level

            if layer <= 0:

                remaining_players.remove(player)

                continue

            pot_amount = (

                layer

                * len(remaining_players)

            )

            if first_pot:

                pot = self.main_pot

                first_pot = False

            else:

                pot = Pot()

                self.side_pots.append(pot)

            pot.amount = pot_amount

            pot.eligible_players = remaining_players.copy()

            previous_level = contribution

            remaining_players.remove(player)
        # =====================================================
    # Pot Access
    # =====================================================

    def get_all_pots(self) -> list[Pot]:
        """
        Returns the main pot followed by all side pots.
        """

        return [self.main_pot] + self.side_pots

    # =====================================================
    # Eligible Players
    # =====================================================

    @staticmethod
    def eligible_players(
        pot: Pot,
        active_players: list[Player]
    ) -> list[Player]:
        """
        Returns players eligible to win the given pot.
        """

        return [

            player

            for player in active_players

            if player in pot.eligible_players

        ]

    # =====================================================
    # Awarding Pots
    # =====================================================

    @staticmethod
    def award_pot(
        winner: Player,
        pot: Pot
    ):
        """
        Award the entire pot to one winner.
        """

        winner.win_chips(pot.amount)

    # =====================================================

    @staticmethod
    def split_pot(
        winners: list[Player],
        pot: Pot
    ):
        """
        Split a pot equally among winners.
        Any leftover chip is awarded starting
        from the first player.
        """

        if not winners:
            return

        share = pot.amount // len(winners)

        remainder = pot.amount % len(winners)

        for player in winners:
            player.win_chips(share)

        for i in range(remainder):
            winners[i].win_chips(1)

    # =====================================================
    # Debug Helpers
    # =====================================================

    def print_contributions(self):

        print("\nPlayer Contributions")

        print("----------------------------")

        for player, chips in self.contributions.items():

            print(
                f"{player.name:<15}${chips}"
            )

    def print_pots(self):

        print("\nPots")

        print("----------------------------")

        print(
            f"Main Pot : ${self.main_pot.amount}"
        )

        for i, pot in enumerate(
            self.side_pots,
            start=1
        ):

            names = ", ".join(

                player.name

                for player in pot.eligible_players

            )

            print()

            print(
                f"Side Pot {i}"
            )

            print(
                f"Amount : ${pot.amount}"
            )

            print(
                f"Eligible : {names}"
            )

    # =====================================================

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

        text.append(
            f"Total Pot : ${self.total_pot()}"
        )

        return "\n".join(text)