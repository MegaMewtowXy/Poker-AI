from models.player import Player
from models.table import Table


class BettingRound:
    """
    Controls a single betting street in Texas Hold'em.

    Responsibilities
    ----------------
    • Manage betting round state
    • Manage turn order
    • Track betting progress
    • Determine when betting is complete

    This class does NOT:
        • Move chips
        • Evaluate hands
        • Award pots
        • Deal cards
    """

    def __init__(
        self,
        players: list[Player],
        table: Table
    ):

        # ==========================================
        # References
        # ==========================================

        self.players = players

        self.table = table

        # ==========================================
        # Round State
        # ==========================================

        # Betting has officially started.
        self.started = False

        # At least one betting action
        # has occurred.
        self.first_action_taken = False

        # Betting street is complete.
        self.betting_closed = False

        # ==========================================
        # Turn State
        # ==========================================

        # Current acting player.
        # -1 means no player selected yet.
        self.current_index = -1

        # First player that acts this street.
        self.starting_player: Player | None = None

        # Last player that bet or raised.
        self.last_aggressor: Player | None = None

        # ==========================================
        # Betting State
        # ==========================================

        # Players still required to respond
        # to the latest bet or raise.
        self.players_to_act: set[Player] = set()

    # ==================================================
    # Round Management
    # ==================================================

    def reset(self):
        """
        Prepare for a new betting street.
        """

        self.started = False

        self.first_action_taken = False

        self.betting_closed = False

        self.current_index = -1

        self.starting_player = None

        self.last_aggressor = None

        self.players_to_act.clear()

        for player in self.players:

            player.reset_betting_round()

            if player.can_act():

                self.players_to_act.add(
                    player
                )

    # --------------------------------------------------

    def reset_for_new_street(self):
        """
        Convenience alias.
        """

        self.reset()

    # --------------------------------------------------

    def start(self):
        """
        Open betting.
        """

        self.started = True

        self.betting_closed = False

    # --------------------------------------------------

    def finish(self):
        """
        Close betting.
        """

        self.started = False

        self.betting_closed = True

    # ==================================================
    # Current Player
    # ==================================================

    def current_player(self) -> Player:
        """
        Return the current acting player.
        """

        if self.current_index == -1:

            raise RuntimeError(
                "Current player has not been set."
            )

        return self.players[
            self.current_index
        ]

    # --------------------------------------------------

    def current_player_or_none(
        self
    ) -> Player | None:
        """
        Return the current player if one
        has been selected.
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
        Set the acting player.
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
        Set the first player to act.
        """

        if player not in self.players:

            raise ValueError(
                "Player is not part of this betting round."
            )

        if not player.can_act():

            raise ValueError(
                "Starting player cannot act."
            )

        self.starting_player = player

        self.set_current_player(
            player
        )
        # ==================================================
    # Navigation
    # ==================================================

    def next_player(self) -> Player | None:
        """
        Advance to the next player able to act.
        """

        if not self.players:

            return None

        total = len(self.players)

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

    def previous_player(self) -> Player | None:
        """
        Move to the previous player able to act.
        """

        if not self.players:

            return None

        total = len(self.players)

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

    # --------------------------------------------------

    def first_player(self) -> Player | None:
        """
        Return the first player able to act.
        """

        for player in self.players:

            if player.can_act():

                return player

        return None

    # --------------------------------------------------

    def last_player(self) -> Player | None:
        """
        Return the last player able to act.
        """

        for player in reversed(self.players):

            if player.can_act():

                return player

        return None

    # --------------------------------------------------

    def next_player_from(
        self,
        player: Player
    ) -> Player | None:
        """
        Return the next acting player after
        the specified player.
        """

        if player not in self.players:

            raise ValueError(
                "Player is not part of this betting round."
            )

        original_index = self.current_index

        self.current_index = self.players.index(
            player
        )

        result = self.next_player()

        self.current_index = original_index

        return result

    # --------------------------------------------------

    def previous_player_from(
        self,
        player: Player
    ) -> Player | None:
        """
        Return the previous acting player before
        the specified player.
        """

        if player not in self.players:

            raise ValueError(
                "Player is not part of this betting round."
            )

        original_index = self.current_index

        self.current_index = self.players.index(
            player
        )

        result = self.previous_player()

        self.current_index = original_index

        return result
        # ==================================================
    # Player Queries
    # ==================================================

    def players_in_hand(self) -> list[Player]:
        """
        Players still participating in the hand.

        Includes all-in players.
        """

        return [

            player

            for player in self.players

            if self.is_player_in_hand(player)

        ]

    # --------------------------------------------------

    def active_players(self) -> list[Player]:
        """
        Players still able to act.
        """

        return [

            player

            for player in self.players

            if player.can_act()

        ]

    # --------------------------------------------------

    def folded_players(self) -> list[Player]:

        return [

            player

            for player in self.players

            if player.folded

        ]

    # --------------------------------------------------

    def all_in_players(self) -> list[Player]:

        return [

            player

            for player in self.players

            if player.all_in

        ]

    # --------------------------------------------------

    def eliminated_players(self) -> list[Player]:

        return [

            player

            for player in self.players

            if player.eliminated

        ]

    # ==================================================
    # Counts
    # ==================================================

    def players_in_hand_count(self) -> int:

        return len(
            self.players_in_hand()
        )

    # --------------------------------------------------

    def active_player_count(self) -> int:

        return len(
            self.active_players()
        )

    # --------------------------------------------------

    def folded_player_count(self) -> int:

        return len(
            self.folded_players()
        )

    # --------------------------------------------------

    def all_in_player_count(self) -> int:

        return len(
            self.all_in_players()
        )

    # --------------------------------------------------

    def eliminated_player_count(self) -> int:

        return len(
            self.eliminated_players()
        )

    # ==================================================
    # Boolean Queries
    # ==================================================

    def has_players_in_hand(self) -> bool:

        return self.players_in_hand_count() > 0

    # --------------------------------------------------

    def has_active_players(self) -> bool:

        return self.active_player_count() > 0

    # --------------------------------------------------

    def is_player_in_hand(
        self,
        player: Player
    ) -> bool:
        """
        Returns True if the player has not
        folded or been eliminated.
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
        """
        Returns True if the player still
        needs to respond to the latest
        bet or raise.
        """

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
        Mark that the player has responded
        to the current bet.
        """

        self.first_action_taken = True

        self.players_to_act.discard(
            player
        )

    # --------------------------------------------------

    def reopen_action(
        self,
        aggressor: Player
    ):
        """
        Reopen betting after a bet or raise.

        Every active player except the
        aggressor must act again.
        """

        if aggressor not in self.players:

            raise ValueError(
                "Player is not part of this betting round."
            )

        self.last_aggressor = aggressor

        self.first_action_taken = True

        self.players_to_act.clear()

        for player in self.active_players():

            if player != aggressor:

                self.players_to_act.add(
                    player
                )

    # --------------------------------------------------

    def everyone_acted(self) -> bool:
        """
        Returns True when every player
        required to act has acted.
        """

        return len(
            self.players_to_act
        ) == 0

    # --------------------------------------------------

    def everyone_matched_bet(self) -> bool:
        """
        Returns True if every player still
        in the hand has matched the current
        table bet or is all-in.
        """

        current_bet = self.table.current_bet

        for player in self.players_in_hand():

            if player.all_in:

                continue

            if player.current_bet != current_bet:

                return False

        return True

    # --------------------------------------------------

    def everyone_all_in(self) -> bool:
        """
        Returns True if every player still
        in the hand is all-in.
        """

        players = self.players_in_hand()

        if not players:

            return False

        return all(

            player.all_in

            for player in players

        )

    # --------------------------------------------------

    def only_one_player_left(self) -> bool:
        """
        Returns True if only one player
        remains in the hand.
        """

        return (

            self.players_in_hand_count()

            == 1

        )

    # --------------------------------------------------

    def betting_complete(self) -> bool:
        """
        Returns True when the betting
        street is complete.
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

    def can_continue(self) -> bool:
        """
        Returns True if betting
        should continue.
        """

        return not self.betting_complete()
        # ==================================================
    # Validation
    # ==================================================

    def validate(self):
        """
        Validate the betting round state.

        Raises
        ------
        RuntimeError
            If the betting round contains
            an invalid state.
        """

        if self.current_index >= len(self.players):

            raise RuntimeError(
                "Current player index is invalid."
            )

        if self.current_index < -1:

            raise RuntimeError(
                "Current player index is invalid."
            )

        if (

            self.starting_player is not None

            and

            self.starting_player not in self.players

        ):

            raise RuntimeError(
                "Starting player is invalid."
            )

        if (

            self.last_aggressor is not None

            and

            self.last_aggressor not in self.players

        ):

            raise RuntimeError(
                "Last aggressor is invalid."
            )

        for player in self.players_to_act:

            if player not in self.players:

                raise RuntimeError(
                    "players_to_act contains an invalid player."
                )

    # ==================================================
    # Utility
    # ==================================================

    def pending_player_count(self) -> int:
        """
        Number of players still required
        to respond.
        """

        return len(self.players_to_act)

    # --------------------------------------------------

    def has_started(self) -> bool:
        """
        Returns True if betting has started.
        """

        return self.started

    # --------------------------------------------------

    def is_closed(self) -> bool:
        """
        Returns True if betting has ended.
        """

        return self.betting_closed

    # --------------------------------------------------

    def has_current_player(self) -> bool:
        """
        Returns True if a current player
        has been selected.
        """

        return self.current_index != -1

    # --------------------------------------------------

    def is_waiting_for_player(
        self,
        player: Player
    ) -> bool:
        """
        Returns True if the player still
        needs to act.
        """

        return player in self.players_to_act

    # ==================================================
    # Debug
    # ==================================================

    def __repr__(self):

        return (

            "BettingRound("

            f"started={self.started}, "

            f"closed={self.betting_closed}, "

            f"current_index={self.current_index}, "

            f"pending={len(self.players_to_act)}"

            ")"

        )

    # --------------------------------------------------

    def __str__(self):

        current = self.current_player_or_none()

        current_name = (

            current.name

            if current is not None

            else "None"

        )

        return (

            "========== BETTING ROUND ==========\n"

            f"Started          : {self.started}\n"

            f"Closed           : {self.betting_closed}\n"

            f"Current Player   : {current_name}\n"

            f"Players To Act   : {len(self.players_to_act)}"

        )