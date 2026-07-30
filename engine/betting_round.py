from models.player import Player
from models.table import Table
from models.action import Action
from models.street import Street
from simulation.logger import GameLogger

class BettingRound:
    """
    Controls a single betting street in Texas Hold'em.

    Responsibilities
    ----------------
    • Manage betting round state
    • Manage turn order
    • Track betting progress
    • Determine when betting is complete
    • Maintain action history
    • Send actions to logger

    This class does NOT:

        • Move chips
        • Evaluate hands
        • Award pots
        • Deal cards
    """

    def __init__(
        self,
        players: list[Player],
        table: Table,
        logger: GameLogger = None
    ):

        # ==========================================
        # References
        # ==========================================

        self.players = players

        self.table = table

        # ==========================================
        # Logger
        # ==========================================

        self.logger = logger

        # ==========================================
        # Round State
        # ==========================================

        self.started = False

        self.first_action_taken = False

        self.betting_closed = False
        # ==========================================
        # Current Street
        # ==========================================

        self.street = Street.PRE_FLOP

        # ==========================================
        # Turn State
        # ==========================================

        self.current_index = -1

        self.starting_player: Player | None = None

        self.last_aggressor: Player | None = None

        # ==========================================
        # Betting State
        # ==========================================

        self.players_to_act: set[Player] = set()

        # ==========================================
        # History
        # ==========================================

        self.action_history: list[dict] = []
        # ==================================================
    # Round Management
    # ==================================================

    def reset(self):
        """
        Prepare betting round for a new street.
        """

        self.started = False

        self.first_action_taken = False

        self.betting_closed = False

        self.current_index = -1

        self.starting_player = None

        self.last_aggressor = None

        self.players_to_act.clear()

        self.action_history.clear()

        for player in self.players:

            player.reset_betting_round()

            if player.can_act():

                self.players_to_act.add(

                    player

                )

    # --------------------------------------------------

    def reset_for_new_street(
        self
    ):

        self.reset()

    # --------------------------------------------------
    def start(
    self
):
        """
        Start betting round and select
        the first player to act.
        """

        self.started = True

        self.betting_closed = False

        # Already selected
        if self.current_index != -1:
            return

        first = self.first_player()

        if first is not None:

            self.set_starting_player(
                first
            )

    # --------------------------------------------------

    def finish(
        self
    ):

        self.started = False

        self.betting_closed = True

    # ==================================================
    # Current Player
    # ==================================================

    def current_player(
        self
    ) -> Player:
        """
        Return current acting player.
        """

        if self.current_index == -1:

            raise RuntimeError(

                "Current player has not been selected."

            )

        return self.players[

            self.current_index

        ]

    # --------------------------------------------------

    def current_player_or_none(
        self
    ) -> Player | None:
        """
        Return current player if available.
        """

        if self.current_index == -1:

            return None

        return self.players[

            self.current_index

        ]

    # --------------------------------------------------

    def set_current_player(
        self,
        player: Player
    ):
        """
        Set current acting player.
        """

        if player not in self.players:

            raise ValueError(

                "Player is not part of this betting round."

            )

        self.current_index = self.players.index(

            player

        )

    # --------------------------------------------------

    def set_starting_player(
        self,
        player: Player
    ):
        """
        Set first player to act.
        """

        if player not in self.players:

            raise ValueError(

                "Player is not part of this betting round."

            )

        if not player.can_act():

            raise ValueError(

                "Player cannot act."

            )

        self.starting_player = player

        self.set_current_player(

            player

        )

    # ==================================================
    # Navigation
    # ==================================================

    def next_player(
        self
    ) -> Player | None:
        """
        Move clockwise to next player
        who can act.
        """

        if not self.players:

            return None

        total = len(

            self.players

        )

        for _ in range(total):

            self.current_index = (

                self.current_index + 1

            ) % total

            player = self.players[

                self.current_index

            ]

            if player.can_act():

                return player

        return None

    # --------------------------------------------------

    def previous_player(
        self
    ) -> Player | None:
        """
        Move backwards to previous
        player who can act.
        """

        if not self.players:

            return None

        total = len(

            self.players

        )

        for _ in range(total):

            self.current_index = (

                self.current_index - 1

            ) % total

            player = self.players[

                self.current_index

            ]

            if player.can_act():

                return player

        return None
    
    # ==================================================
    # Navigation Helpers
    # ==================================================

    def next_player_from(
        self,
        player: Player
    ) -> Player | None:
        """
        Find next acting player after
        given player.
        """

        if player not in self.players:

            raise ValueError(

                "Player is not part of this betting round."

            )

        old_index = self.current_index

        self.current_index = self.players.index(

            player

        )

        result = self.next_player()

        self.current_index = old_index

        return result

    # --------------------------------------------------

    def previous_player_from(
        self,
        player: Player
    ) -> Player | None:
        """
        Find previous acting player.
        """

        if player not in self.players:

            raise ValueError(

                "Player is not part of this betting round."

            )

        old_index = self.current_index

        self.current_index = self.players.index(

            player

        )

        result = self.previous_player()

        self.current_index = old_index

        return result

    # --------------------------------------------------

    def first_player(
        self
    ) -> Player | None:
        """
        Return first player who can act.

        Game controller should override
        using poker rules.
        """

        for player in self.players:

            if player.can_act():

                return player

        return None

    # --------------------------------------------------

    def last_player(
        self
    ) -> Player | None:

        for player in reversed(self.players):

            if player.can_act():

                return player

        return None

    # ==================================================
    # Player Queries
    # ==================================================

    def players_in_hand(
        self
    ) -> list[Player]:
        """
        Players still participating.

        Includes:
        - Active players
        - All-in players

        Excludes:
        - Folded
        - Eliminated
        """

        return [

            player

            for player in self.players

            if self.is_player_in_hand(player)

        ]

    # --------------------------------------------------

    def active_players(
        self
    ) -> list[Player]:
        """
        Players who can still act.
        """

        return [

            player

            for player in self.players

            if player.can_act()

        ]

    # --------------------------------------------------

    def folded_players(
        self
    ) -> list[Player]:

        return [

            player

            for player in self.players

            if player.folded

        ]

    # --------------------------------------------------

    def all_in_players(
        self
    ) -> list[Player]:

        return [

            player

            for player in self.players

            if player.all_in

        ]

    # --------------------------------------------------

    def eliminated_players(
        self
    ) -> list[Player]:

        return [

            player

            for player in self.players

            if player.eliminated

        ]

    # ==================================================
    # Counts
    # ==================================================

    def players_in_hand_count(
        self
    ) -> int:

        return len(

            self.players_in_hand()

        )

    # --------------------------------------------------

    def active_player_count(
        self
    ) -> int:

        return len(

            self.active_players()

        )

    # --------------------------------------------------

    def folded_player_count(
        self
    ) -> int:

        return len(

            self.folded_players()

        )

    # --------------------------------------------------

    def all_in_player_count(
        self
    ) -> int:

        return len(

            self.all_in_players()

        )

    # --------------------------------------------------

    def eliminated_player_count(
        self
    ) -> int:

        return len(

            self.eliminated_players()

        )
    
    # ==================================================
    # Boolean Queries
    # ==================================================

    def has_players_in_hand(
        self
    ) -> bool:

        return (

            self.players_in_hand_count()

            > 0

        )

    # --------------------------------------------------

    def has_active_players(
        self
    ) -> bool:

        return (

            self.active_player_count()

            > 0

        )

    # --------------------------------------------------

    def is_player_in_hand(
        self,
        player: Player
    ) -> bool:
        """
        Check whether player is eligible
        for the pot.
        """

        return (

            not player.folded

            and

            not player.eliminated

        )

    # --------------------------------------------------

    def has_pending_action(
        self,
        player: Player
    ) -> bool:

        return (

            player in self.players_to_act

        )

    # ==================================================
    # Betting Logic
    # ==================================================

    def mark_player_acted(
        self,
        player: Player
    ):
        """
        Mark player as completed action.
        """

        self.first_action_taken = True

        self.players_to_act.discard(

            player

        )

    # --------------------------------------------------

    def record_action(
        self,
        player: Player,
        action: Action,
        amount=0
    ):
        """
        Store action history.

        Used for:
        - Replay
        - AI training
        - Debugging
        - External logging
        """

        action_name = (

            action.name

            if hasattr(

                action,

                "name"

            )

            else action

        )

        action_data = {

            "player":

                player.name,

            "action":

                action_name,

            "amount":

                amount,

            "street":

                self.street

        }

        # Internal history

        self.action_history.append(

            action_data

        )

        # External Game Logger

        if self.logger:

            self.logger.log_action(

                player,

                action,

                amount,

                self.street

            )

    # --------------------------------------------------

    def reopen_action(
        self,
        aggressor: Player
    ):
        """
        Reopen betting after bet/raise.

        Every active player except
        aggressor must respond again.
        """

        if aggressor not in self.players:

            raise ValueError(

                "Player is not part of this betting round."

            )

        self.last_aggressor = aggressor

        self.first_action_taken = True

        self.players_to_act.clear()

        for player in self.players:

            if (

                player.can_act()

                and

                player != aggressor

            ):

                self.players_to_act.add(

                    player

                )

    # --------------------------------------------------

    def amount_to_call(
        self,
        player: Player
    ) -> int:
        """
        Return chips required to call.
        """

        return max(

            0,

            self.table.current_bet

            -

            player.current_bet

        )

    # --------------------------------------------------

    def everyone_acted(
        self
    ) -> bool:

        return (

            len(self.players_to_act)

            == 0

        )

    # --------------------------------------------------

    def everyone_matched_bet(
        self
    ) -> bool:
        """
        Check if all players matched
        current bet.
        """

        current_bet = self.table.current_bet

        for player in self.players_in_hand():

            if player.all_in:

                continue

            if player.current_bet != current_bet:

                return False

        return True

    # --------------------------------------------------

    def everyone_all_in(
        self
    ) -> bool:
        """
        Check if all remaining players
        are all-in.
        """

        players = self.players_in_hand()

        if not players:

            return False

        return all(

            player.all_in

            for player in players

        )

    # --------------------------------------------------

    def only_one_player_left(
        self
    ) -> bool:

        return (

            self.players_in_hand_count()

            == 1

        )

    # --------------------------------------------------

    def betting_complete(
        self
    ) -> bool:
        """
        Determine if street ended.
        """

        if self.only_one_player_left():

            return True

        if self.everyone_all_in():

            return True

        if (

            self.everyone_acted()

            and

            self.everyone_matched_bet()

        ):

            return True

        return False

    # --------------------------------------------------

    def can_continue(
        self
    ) -> bool:

        return not self.betting_complete()
        # ==================================================
    # Validation
    # ==================================================

    def validate(
        self
    ):
        """
        Validate betting round state.
        """

        if not self.players:

            raise ValueError(

                "No players in betting round."

            )

        for player in self.players:

            if player is None:

                raise ValueError(

                    "Invalid player detected."

                )

        return True

    # ==================================================
    # Status Helpers
    # ==================================================

    def pending_player_count(
        self
    ) -> int:
        """
        Number of players waiting
        for action.
        """

        return len(

            self.players_to_act

        )

    # --------------------------------------------------

    def has_started(
        self
    ) -> bool:
        """
        Check if betting round started.
        """

        return self.started

    # --------------------------------------------------

    def is_closed(
        self
    ) -> bool:
        """
        Check if betting round ended.
        """

        return self.betting_closed

    # --------------------------------------------------

    def has_current_player(
        self
    ) -> bool:
        """
        Check current player availability.
        """

        return self.current_index != -1

    # --------------------------------------------------

    def is_waiting_for_player(
        self
    ) -> bool:
        """
        Check whether round is waiting
        for an action.
        """

        return (

            self.has_started()

            and

            self.pending_player_count() > 0

        )

    # ==================================================
    # Street Management
    # ==================================================

    def set_street(
        self,
        street: Street
    ):
        """
        Update current betting street.
        """

        if not isinstance(street, Street):

            raise ValueError(
                "Invalid street type."
            )

        self.street = street

    # ==================================================
    # Debug
    # ==================================================

    def __str__(
        self
    ):

        return (

            f"BettingRound("

            f"players={len(self.players)}, "

            f"pending={len(self.players_to_act)})"

        )

    def __repr__(
        self
    ):

        return (

            f"BettingRound("

            f"started={self.started}, "

            f"closed={self.betting_closed})"

        )