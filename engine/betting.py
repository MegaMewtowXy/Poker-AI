from engine.pot_manager import PotManager

from models.player import Player
from models.table import Table


class BettingEngine:
    """
    Executes all legal betting actions.

    Responsibilities
    ----------------
    • Fold
    • Check
    • Call
    • Bet
    • Raise
    • All-In

    Does NOT

    • Control turn order
    • Decide AI actions
    • Determine winners
    """

    def __init__(
        self,
        table: Table,
        pot_manager: PotManager
    ):

        self.table = table

        self.pot_manager = pot_manager

    # =====================================================
    # Internal
    # =====================================================

    def _collect_bet(
        self,
        player: Player,
        amount: int
    ) -> int:
        """
        Removes chips from player
        and places them into the pot.
        """

        if amount <= 0:
            return 0

        amount = player.place_bet(
            amount
        )

        self.pot_manager.add_to_main_pot(
            player,
            amount
        )

        return amount

    # =====================================================
    # Validation
    # =====================================================

    def can_check(
        self,
        player: Player
    ) -> bool:

        return (
            player.current_bet
            ==
            self.table.current_bet
        )

    # -----------------------------------------------------

    def amount_to_call(
        self,
        player: Player
    ) -> int:

        return max(

            0,

            self.table.current_bet
            -
            player.current_bet

        )

    # -----------------------------------------------------

    def can_call(
        self,
        player: Player
    ) -> bool:

        return (
            self.amount_to_call(player)
            > 0
        )

    # -----------------------------------------------------

    def minimum_raise(self) -> int:

        return (

            self.table.current_bet

            +

            self.table.minimum_raise

        )

    # =====================================================
    # Blinds
    # =====================================================

    def post_small_blind(
        self,
        player: Player
    ):

        self._collect_bet(

            player,

            self.table.small_blind

        )

        self.table.current_bet = max(

            self.table.current_bet,

            player.current_bet

        )

    # -----------------------------------------------------

    def post_big_blind(
        self,
        player: Player
    ):

        self._collect_bet(

            player,

            self.table.big_blind

        )

        self.table.current_bet = max(

            self.table.current_bet,

            player.current_bet

        )

        self.table.minimum_raise = (
            self.table.big_blind
        )
        # =====================================================
    # Actions
    # =====================================================

    def fold(
        self,
        player: Player
    ):
        """
        Player folds.
        """

        player.fold()

    # -----------------------------------------------------

    def check(
        self,
        player: Player
    ) -> bool:
        """
        Execute a check.

        Returns
        -------
        True if successful.
        """

        if not self.can_check(player):

            raise ValueError(
                "Cannot check. A bet must be called."
            )

        return True

    # -----------------------------------------------------

    def call(
        self,
        player: Player
    ) -> int:
        """
        Match the current bet.
        """

        amount = self.amount_to_call(player)

        return self._collect_bet(
            player,
            amount
        )

    # -----------------------------------------------------

    def bet(
        self,
        player: Player,
        amount: int
    ) -> int:
        """
        First bet on a betting street.
        """

        if self.table.current_bet != 0:

            raise ValueError(
                "Cannot bet after betting has started."
            )

        if amount <= 0:

            raise ValueError(
                "Bet must be greater than zero."
            )

        self._collect_bet(
            player,
            amount
        )

        self.table.current_bet = (
            player.current_bet
        )

        self.table.minimum_raise = amount

        return amount

    # -----------------------------------------------------

    def raise_bet(
        self,
        player: Player,
        raise_to: int
    ) -> int:
        """
        Raise to a total amount.

        Example

        Current Bet = 40

        Raise To = 100
        """

        if raise_to <= self.table.current_bet:

            raise ValueError(
                "Raise must exceed the current bet."
            )

        minimum = self.minimum_raise()

        if raise_to < minimum:

            raise ValueError(
                f"Minimum raise is {minimum}."
            )

        additional = (

            raise_to

            -

            player.current_bet

        )

        self._collect_bet(

            player,

            additional

        )

        self.table.minimum_raise = (

            raise_to

            -

            self.table.current_bet

        )

        self.table.current_bet = raise_to

        return raise_to

    # -----------------------------------------------------

    def all_in(
        self,
        player: Player
    ) -> int:
        """
        Push every remaining chip.
        """

        previous = player.current_bet

        amount = self._collect_bet(

            player,

            player.chips

        )

        # Player increased betting

        if player.current_bet > self.table.current_bet:

            self.table.minimum_raise = (

                player.current_bet

                -

                self.table.current_bet

            )

            self.table.current_bet = (

                player.current_bet

            )

        return amount
        # =====================================================
    # Validation Helpers
    # =====================================================

    def is_valid_raise(
        self,
        player: Player,
        raise_to: int
    ) -> bool:
        """
        Checks whether a raise is legal.
        """

        if raise_to <= self.table.current_bet:
            return False

        # Player can always go all-in even if it is
        # smaller than a minimum raise.
        if raise_to >= (
            player.current_bet + player.chips
        ):
            return True

        return raise_to >= self.minimum_raise()

    # -----------------------------------------------------

    def can_go_all_in(
        self,
        player: Player
    ) -> bool:

        return (
            not player.all_in
            and
            player.chips > 0
        )

    # -----------------------------------------------------

    def has_called(
        self,
        player: Player
    ) -> bool:

        return (
            player.current_bet
            ==
            self.table.current_bet
        )

    # -----------------------------------------------------

    def is_betting_closed(
        self,
        players: list[Player]
    ) -> bool:
        """
        Returns True when every active player has
        either:

        • Folded
        • Is All-In
        • Matched the current bet
        """

        for player in players:

            if player.folded:
                continue

            if player.all_in:
                continue

            if player.current_bet != self.table.current_bet:
                return False

        return True

    # =====================================================
    # Raise Logic
    # =====================================================

    def raise_reopens_action(
        self,
        previous_bet: int,
        new_bet: int
    ) -> bool:
        """
        Determines whether betting should reopen.

        According to Texas Hold'em rules,
        a raise must be at least the size of the
        previous full raise.
        """

        return (

            new_bet

            -

            previous_bet

            >=

            self.table.minimum_raise

        )

    # =====================================================
    # Short All-In
    # =====================================================

    def is_short_all_in(
        self,
        previous_bet: int,
        player: Player
    ) -> bool:
        """
        Detect whether an all-in is smaller than
        the minimum raise.
        """

        return (

            player.all_in

            and

            (
                player.current_bet
                -
                previous_bet
            )

            <

            self.table.minimum_raise

        )

    # =====================================================
    # Betting Round Helpers
    # =====================================================

    @staticmethod
    def active_players(
        players: list[Player]
    ):

        return [

            player

            for player in players

            if (
                not player.folded
                and
                not player.eliminated
            )

        ]

    # -----------------------------------------------------

    @staticmethod
    def players_still_with_chips(
        players: list[Player]
    ):

        return [

            player

            for player in players

            if (
                not player.folded
                and
                player.chips > 0
            )

        ]
        # =====================================================
    # Pot Helpers
    # =====================================================

    def finalize_betting(
        self,
        players: list[Player]
    ):
        """
        Called once a betting street has ended.

        Builds side pots if necessary.
        """

        self.pot_manager.build_side_pots()

    # =====================================================
    # Utility
    # =====================================================

    def reset_street(self):
        """
        Reset betting information for the next street.
        """

        self.table.current_bet = 0

        self.table.minimum_raise = self.table.big_blind

    # -----------------------------------------------------

    def player_is_all_in(
        self,
        player: Player
    ) -> bool:

        return player.all_in

    # -----------------------------------------------------

    def player_has_folded(
        self,
        player: Player
    ) -> bool:

        return player.folded

    # -----------------------------------------------------

    def player_can_act(
        self,
        player: Player
    ) -> bool:

        return (

            not player.folded

            and

            not player.all_in

            and

            not player.eliminated

        )

    # =====================================================
    # Debug
    # =====================================================

    def print_betting_status(
        self,
        players: list[Player]
    ):

        print("\n========== BETTING STATUS ==========\n")

        print(
            f"Current Bet : ${self.table.current_bet}"
        )

        print(
            f"Minimum Raise : ${self.table.minimum_raise}"
        )

        print()

        for player in players:

            print(
                f"{player.name:<15}"
                f"Chips: {player.chips:<6}"
                f"Bet: {player.current_bet:<6}"
                f"Folded: {player.folded}"
            )

    # =====================================================
    # String Representation
    # =====================================================

    def __str__(self):

        return (

            f"Current Bet : ${self.table.current_bet}\n"

            f"Minimum Raise : ${self.table.minimum_raise}"

        )