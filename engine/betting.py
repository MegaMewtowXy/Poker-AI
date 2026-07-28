from engine.pot_manager import PotManager
from engine.betting_round import BettingRound

from models import player
from models.player import Player
from models.table import Table
from models.action import Action





class BettingEngine:
    """
    Executes all legal Texas Hold'em betting actions.

    Responsibilities
    ----------------
    • Fold
    • Check
    • Call
    • Bet
    • Raise
    • All-In

    Integrates with:
    • BettingRound -> turn/state tracking
    • PotManager -> chip collection


    Does NOT:

    • Decide AI actions
    • Control player order
    • Evaluate hands
    • Award winners
    """





    def __init__(
        self,
        table: Table,
        pot_manager: PotManager,
        betting_round: BettingRound | None = None
    ):

        self.table = table

        self.pot_manager = pot_manager

        self.betting_round = betting_round





    # =====================================================
    # Internal Helpers
    # =====================================================

    def _validate_player(
        self,
        player: Player
    ):
        """
        Ensure player can act.
        """

        if not player.can_act():

            raise ValueError(

                f"{player.name} cannot act."

            )





    # -----------------------------------------------------

    def _collect_bet(
        self,
        player: Player,
        amount: int
    ) -> int:
        """
        Move chips from player
        into pot.
        """

        if amount <= 0:

            return 0





        collected = player.place_bet(

            amount

        )





        self.pot_manager.add_to_main_pot(

            player,

            collected

        )





        return collected





    # -----------------------------------------------------

    def _record_action(
        self,
        player: Player,
        action: Action,
        amount: int = 0
    ):
        """
        Send action information
        to BettingRound.

        Amount is stored for:
        - Replay
        - Statistics
        - AI training
        """

        if self.betting_round is not None:

            self.betting_round.record_action(

                player,

                action,

                amount

            )





    # -----------------------------------------------------

    def _mark_acted(
        self,
        player: Player
    ):
        """
        Notify BettingRound that
        player completed action.
        """

        if self.betting_round is not None:

            self.betting_round.mark_player_acted(

                player

            )
        # =====================================================
    # Blind Management
    # =====================================================

    def post_blind(
    self,
    player: Player,
    amount: int
) -> int:
        """
        Post small blind or big blind.

        Returns actual amount posted.
        """

        self._validate_player(
            player
        )
        
        paid = self._collect_bet(
            player,
            amount
        )

        # ------------------------------------------
        # Update current table bet
        # ------------------------------------------

        if paid > self.table.current_bet:

            self.table.current_bet = paid

        # ------------------------------------------
        # Big blind becomes minimum raise
        # ------------------------------------------

        if paid >= self.table.big_blind:

            self.table.minimum_raise = self.table.big_blind

        # ------------------------------------------
        # Record action
        # ------------------------------------------

        self._record_action(
            player,
            Action.POST_BLIND,
            paid
        )

        return paid



    # =====================================================
    # Fold
    # =====================================================

    def fold(
        self,
        player: Player
    ):
        """
        Player folds hand.
        """

        self._validate_player(

            player

        )


        player.fold()


        self._record_action(

            player,

            Action.FOLD,

            0

        )


        self._mark_acted(

            player

        )





    # =====================================================
    # Check
    # =====================================================

    def check(
        self,
        player: Player
    ):
        """
        Player checks.

        Allowed only when no chips
        are required to call.
        """

        self._validate_player(

            player

        )


        if self.amount_to_call(player) != 0:

            raise ValueError(

                "Cannot check. Player must call."

            )


        player.check()


        self._record_action(

            player,

            Action.CHECK,

            0

        )


        self._mark_acted(

            player

        )





    # =====================================================
    # Call
    # =====================================================

    def call(
        self,
        player: Player
    ) -> int:
        """
        Match current table bet.
        """

        self._validate_player(

            player

        )


        amount = self.amount_to_call(

            player

        )


        paid = self._collect_bet(

            player,

            amount

        )


        player.call()


        self._record_action(

            player,

            Action.CALL,

            paid

        )


        self._mark_acted(

            player

        )


        return paid





    # =====================================================
    # Helpers
    # =====================================================

    def amount_to_call(
        self,
        player: Player
    ) -> int:
        """
        Calculate chips required
        to match current bet.
        """

        return max(

            0,

            self.table.current_bet

            -

            player.current_bet

        )
        # =====================================================
    # Bet
    # =====================================================

    def bet(
        self,
        player: Player,
        amount: int
    ) -> int:
        """
        Place first bet in betting round.
        """

        self._validate_player(

            player

        )


        if self.table.current_bet > 0:

            raise ValueError(

                "Cannot bet. A bet already exists."

            )


        if amount <= 0:

            raise ValueError(

                "Bet amount must be positive."

            )



        paid = self._collect_bet(

            player,

            amount

        )



        self.table.current_bet = (

            player.current_bet

        )


        self.table.minimum_raise = (

            self.table.big_blind

        )


        player.bet()



        self._record_action(

            player,

            Action.BET,

            paid

        )


        self._mark_acted(

            player

        )



        if self.betting_round is not None:

            self.betting_round.reopen_action(

                player

            )


        return paid





    # =====================================================
    # Raise
    # =====================================================

    def raise_bet(
        self,
        player: Player,
        raise_to: int
    ) -> int:
        """
        Raise current table bet.

        raise_to means final total bet
        after raising.
        """

        self._validate_player(

            player

        )

        
        if raise_to <= self.table.current_bet:

            raise ValueError(

                "Raise must exceed current bet."

            )



        previous_bet = self.table.current_bet



        additional = (

            raise_to

            -

            player.current_bet

        )



        if additional <= 0:

            raise ValueError(

                "Invalid raise amount."

            )



        paid = self._collect_bet(

            player,

            additional

        )

        

        actual_raise = raise_to - previous_bet
        

        if actual_raise < self.table.minimum_raise:
            
            if player.chips == 0:
            # Player is all-in.
            # This does NOT reopen betting.
                self.table.current_bet = player.current_bet

                player.last_action = Action.ALL_IN

                return paid
            raise ValueError(

                "Raise is below minimum raise."

            )



        self.table.current_bet = player.current_bet



        self.table.minimum_raise = actual_raise



        player.raise_bet()



        self._record_action(

            player,

            Action.RAISE,

            paid

        )



        self._mark_acted(

            player

        )



        if self.betting_round is not None:

            self.betting_round.reopen_action(

                player

            )


        return paid
    
    # =====================================================
    # All-In
    # =====================================================

    def all_in(
        self,
        player: Player
    ) -> int:
        """
        Move entire remaining stack.

        Handles:
        - normal all-in
        - short all-in
        """

        self._validate_player(

            player

        )


        amount = player.chips


        if amount <= 0:

            return 0



        paid = self._collect_bet(

            player,

            amount

        )


        player.last_action = Action.ALL_IN



        self._record_action(

            player,

            Action.ALL_IN,

            paid

        )


        self._mark_acted(

            player

        )



        # ---------------------------------------------
        # Full raise handling
        # ---------------------------------------------

        if player.current_bet > self.table.current_bet:


            raise_amount = (

                player.current_bet

                -

                self.table.current_bet

            )


            self.table.current_bet = (

                player.current_bet

            )



            if raise_amount >= self.table.minimum_raise:

                self.table.minimum_raise = raise_amount



                if self.betting_round is not None:

                    self.betting_round.reopen_action(

                        player

                    )


        return paid





    # =====================================================
    # Validation Helpers
    # =====================================================

    def validate_amount(
        self,
        amount: int
    ):
        """
        Validate chip amount.
        """

        if amount < 0:

            raise ValueError(

                "Amount cannot be negative."

            )





    # -----------------------------------------------------

    def validate_raise(
        self,
        player: Player,
        raise_to: int
    ):
        """
        Validate raise legality.
        """

        self._validate_player(

            player

        )


        if raise_to <= self.table.current_bet:

            raise ValueError(

                "Raise must exceed current bet."

            )


        if (

            raise_to - self.table.current_bet

            <

            self.table.minimum_raise

        ):

            raise ValueError(

                "Raise is below minimum raise."

            )





    # =====================================================
    # All-In Helpers
    # =====================================================

    def is_short_all_in(
        self,
        player: Player
    ) -> bool:
        """
        Check if player's all-in is
        smaller than minimum raise.
        """

        if not player.all_in:

            return False



        raise_amount = (

            player.current_bet

            -

            self.table.current_bet

        )


        return (

            raise_amount > 0

            and

            raise_amount < self.table.minimum_raise

        )





    # -----------------------------------------------------

    def can_reopen_after_all_in(
        self,
        player: Player
    ) -> bool:
        """
        Determine whether an all-in
        reopens betting.

        Short all-ins do not reopen.
        """

        return not self.is_short_all_in(

            player

        )
    
    # =====================================================
    # Pot Helpers
    # =====================================================

    def current_pot_size(
        self
    ) -> int:
        """
        Return total chips currently
        in pots.
        """

        return self.pot_manager.total_pot()





    # -----------------------------------------------------

    def player_contribution(
        self,
        player: Player
    ) -> int:
        """
        Return player's total
        contribution this hand.
        """

        return player.total_bet





    # =====================================================
    # Player State Helpers
    # =====================================================

    def can_player_act(
        self,
        player: Player
    ) -> bool:
        """
        Public wrapper for player action check.
        """

        return player.can_act()





    # -----------------------------------------------------

    def player_has_folded(
        self,
        player: Player
    ) -> bool:

        return player.folded





    # -----------------------------------------------------

    def player_is_all_in(
        self,
        player: Player
    ) -> bool:

        return player.all_in





    # =====================================================
    # Street Helpers
    # =====================================================

    def current_street(
        self
    ):
        """
        Return current poker street.
        """

        return self.table.street





    # -----------------------------------------------------

    def is_pre_flop(
        self
    ) -> bool:

        return self.table.is_pre_flop()





    # -----------------------------------------------------

    def is_flop(
        self
    ) -> bool:

        return self.table.is_flop()





    # -----------------------------------------------------

    def is_turn(
        self
    ) -> bool:

        return self.table.is_turn()





    # -----------------------------------------------------

    def is_river(
        self
    ) -> bool:

        return self.table.is_river()





    # =====================================================
    # Betting Completion
    # =====================================================

    def is_betting_closed(
        self,
        players: list[Player]
    ) -> bool:
        """
        Check whether betting round is complete.

        Conditions:

        - Folded players ignored
        - All-in players ignored
        - Remaining players must match
          current bet
        """

        for player in players:


            if player.folded:

                continue



            if player.eliminated:

                continue



            if player.all_in:

                continue



            if player.current_bet != self.table.current_bet:

                return False





        return True





    # -----------------------------------------------------

    def active_players(
        self,
        players: list[Player]
    ) -> list[Player]:
        """
        Return players still in hand.
        """

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

    def players_with_chips(
        self,
        players: list[Player]
    ) -> list[Player]:
        """
        Return players who can continue betting.
        """

        return [

            player

            for player in players

            if (

                not player.folded

                and

                not player.eliminated

                and

                player.chips > 0

            )

        ]





    # =====================================================
    # Pot Finalization
    # =====================================================

    def finalize_betting(
        self
    ):
        """
        Called after betting street ends.

        Builds side pots.
        """

        self.pot_manager.build_side_pots()





    # =====================================================
    # Street Reset
    # =====================================================

    def reset_street(
        self
    ):
        """
        Reset table betting values
        for next street.
        """

        self.table.current_bet = 0

        self.table.minimum_raise = (

            self.table.big_blind

        )





    # =====================================================
    # Full Reset
    # =====================================================

    def reset(
        self
    ):
        """
        Reset engine state.

        Does not affect chips.
        """

        self.reset_street()





    # =====================================================
    # Debug
    # =====================================================

    def print_betting_status(
        self,
        players: list[Player]
    ):

        print(
            "\n========== BETTING STATUS ==========\n"
        )


        print(
            f"Current Bet   : ${self.table.current_bet}"
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

                f"Total: {player.total_bet:<6}"

                f"Folded: {player.folded}"

                f"All-In: {player.all_in}"

            )





    # =====================================================
    # String Representation
    # =====================================================

    def __str__(
        self
    ):

        return (

            "========== BETTING ENGINE ==========\n"

            f"Current Bet   : ${self.table.current_bet}\n"

            f"Minimum Raise : ${self.table.minimum_raise}\n"

            f"Street        : {self.table.street}"

        )