from collections import defaultdict

from models.player import Player
from models.pot import Pot



class PotManager:
    """
    Manages poker pots.

    Responsibilities
    ----------------
    • Track contributions
    • Build main pot
    • Build side pots
    • Determine eligibility
    • Award chips
    """



    def __init__(self):

        self.main_pot = Pot()

        self.side_pots: list[Pot] = []


        # Player -> chips invested
        self.contributions: dict[Player, int] = defaultdict(int)



    # =====================================================
    # Reset
    # =====================================================

    def reset(self):
        """
        Reset complete pot state.
        """

        self.main_pot.clear()

        self.side_pots.clear()

        self.contributions.clear()



    # =====================================================
    # Validation
    # =====================================================

    def _validate_amount(
        self,
        amount: int
    ):

        if amount < 0:

            raise ValueError(
                "Chip amount cannot be negative."
            )



    # =====================================================
    # Contributions
    # =====================================================

    def add_to_main_pot(
        self,
        player: Player,
        amount: int
    ):
        """
        Add player contribution.

        Used by BettingEngine when
        chips enter the pot.
        """

        self._validate_amount(

            amount

        )


        if amount == 0:

            return



        self.main_pot.add_chips(

            amount

        )


        self.main_pot.add_player(

            player

        )


        self.contributions[player] += amount



    # -----------------------------------------------------

    def player_contribution(
        self,
        player: Player
    ) -> int:

        return self.contributions[player]



    # -----------------------------------------------------

    def all_players(self):

        return list(

            self.contributions.keys()

        )



    # -----------------------------------------------------

    def players_sorted_by_contribution(self):

        return sorted(

            self.contributions.items(),

            key=lambda x: x[1]

        )
        # =====================================================
    # Side Pot Construction
    # =====================================================

    def build_side_pots(self):
        """
        Build main pot and side pots.

        Example:

        Alice   -> 100
        Bob     -> 300
        Charlie -> 500


        Result:

        Main Pot  : 300
        Side Pot1 : 400
        Side Pot2 : 200
        """

        # Clear previous build

        self.main_pot.clear()

        self.side_pots.clear()



        contributors = [

            (player, chips)

            for player, chips

            in self.contributions.items()

            if chips > 0

        ]



        if not contributors:

            return



        # Lowest contribution first

        contributors.sort(

            key=lambda x: x[1]

        )



        previous_level = 0



        remaining_players = [

            player

            for player, _

            in contributors

        ]



        first_pot = True



        for player, contribution in contributors:


            layer = (

                contribution

                -

                previous_level

            )


            if layer <= 0:

                remaining_players.remove(

                    player

                )

                continue



            pot_amount = (

                layer

                *

                len(remaining_players)

            )



            if first_pot:


                pot = self.main_pot

                first_pot = False



            else:


                pot = Pot()

                self.side_pots.append(

                    pot

                )



            pot.amount = pot_amount


            pot.eligible_players = (

                remaining_players.copy()

            )



            previous_level = contribution



            remaining_players.remove(

                player

            )



    # =====================================================
    # Pot Access
    # =====================================================

    def get_main_pot(self) -> Pot:
        """
        Return main pot.
        """

        return self.main_pot



    # -----------------------------------------------------

    def get_side_pots(self) -> list[Pot]:
        """
        Return all side pots.
        """

        return self.side_pots



    # -----------------------------------------------------

    def get_all_pots(self) -> list[Pot]:
        """
        Main pot followed by side pots.
        """

        return [

            self.main_pot

        ] + self.side_pots



    # =====================================================
    # Pot Information
    # =====================================================

    def total_pot(self) -> int:
        """
        Return total chips in all pots.
        """

        total = self.main_pot.amount



        for pot in self.side_pots:

            total += pot.amount



        return total



    # -----------------------------------------------------

    def clear_side_pots(self):

        self.side_pots.clear()
        # =====================================================
    # Eligible Players
    # =====================================================

    @staticmethod
    def eligible_players(
        pot: Pot,
        active_players: list[Player]
    ) -> list[Player]:
        """
        Return players who can win a pot.

        A player must:
        - Be in pot eligibility list
        - Still be active
        """

        return [

            player

            for player in active_players

            if player in pot.eligible_players

        ]



    # -----------------------------------------------------

    def eligible_for_pot(
        self,
        pot: Pot,
        players: list[Player]
    ) -> list[Player]:
        """
        Instance wrapper for showdown usage.
        """

        return self.eligible_players(

            pot,

            players

        )



    # =====================================================
    # Pot Awarding
    # =====================================================

    def award_pot(
        self,
        winner: Player,
        pot: Pot
    ):
        """
        Award complete pot to one player.
        """

        if pot.amount <= 0:

            return



        winner.win_chips(

            pot.amount

        )


        self.clear_pot(

            pot

        )



    # -----------------------------------------------------

    def split_pot(
        self,
        winners: list[Player],
        pot: Pot
    ):
        """
        Split pot between multiple winners.

        Remaining chips after division
        go to players from first position.
        """

        if not winners:

            return



        if pot.amount <= 0:

            return



        share = (

            pot.amount

            //

            len(winners)

        )


        remainder = (

            pot.amount

            %

            len(winners)

        )



        for player in winners:


            player.win_chips(

                share

            )



        for i in range(remainder):


            winners[i].win_chips(

                1

            )



        self.clear_pot(

            pot

        )



    # =====================================================
    # Pot Clearing
    # =====================================================

    def clear_pot(
        self,
        pot: Pot
    ):
        """
        Empty a pot after payout.
        """

        pot.clear()



    # -----------------------------------------------------

    def clear_all_pots(self):
        """
        Remove all chips from all pots.
        """

        self.main_pot.clear()


        for pot in self.side_pots:

            pot.clear()
        # =====================================================
    # Validation
    # =====================================================

    def validate(self):
        """
        Validate pot state.
        """

        if self.main_pot.amount < 0:

            raise RuntimeError(
                "Main pot cannot be negative."
            )


        for pot in self.side_pots:

            if pot.amount < 0:

                raise RuntimeError(
                    "Side pot cannot be negative."
                )



        for player, amount in self.contributions.items():

            if amount < 0:

                raise RuntimeError(
                    f"Invalid contribution for {player.name}"
                )



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



    # -----------------------------------------------------

    def print_pots(self):

        print("\nPots")

        print("----------------------------")


        print(

            f"Main Pot : ${self.main_pot.amount}"

        )



        for index, pot in enumerate(

            self.side_pots,

            start=1

        ):

            names = ", ".join(

                player.name

                for player in pot.eligible_players

            )



            print()

            print(

                f"Side Pot {index}"

            )


            print(

                f"Amount : ${pot.amount}"

            )


            print(

                f"Eligible : {names}"

            )



    # =====================================================
    # Information
    # =====================================================

    def pot_count(self) -> int:
        """
        Return number of pots.
        """

        return 1 + len(self.side_pots)



    # -----------------------------------------------------

    def has_side_pots(self) -> bool:

        return len(self.side_pots) > 0



    # -----------------------------------------------------

    def is_empty(self) -> bool:

        return self.total_pot() == 0



    # =====================================================
    # String Representation
    # =====================================================

    def __str__(self):

        lines = []


        lines.append(

            f"Main Pot : ${self.main_pot.amount}"

        )


        for index, pot in enumerate(

            self.side_pots,

            start=1

        ):

            lines.append(

                f"Side Pot {index} : ${pot.amount}"

            )



        lines.append(

            f"Total Pot : ${self.total_pot()}"

        )


        return "\n".join(lines)