from models.action import Action
from models.card import Card
from models.player_position import PlayerPosition
from models.player_role import PlayerRole

class Player:
    """
    Represents a Texas Hold'em player.

    Stores:

    - Identity
    - Position
    - Roles
    - Chips
    - Cards
    - Betting state
    - Statistics
    """

    def __init__(
        self,
        name: str,
        chips: int,
        is_ai: bool = False
    ):

        if not name:

            raise ValueError(
                "Player name is required."
            )

        if chips < 0:

            raise ValueError(
                "Player chips cannot be negative."
            )

        # ==========================================
        # Identity
        # ==========================================

        self.name = name

        self.is_ai = is_ai

        # ==========================================
        # Position + Roles
        # ==========================================

        self.position = PlayerPosition.UNKNOWN

        # Multiple roles possible
        #
        # Heads Up:
        #
        # BUTTON player:
        #   DEALER
        #   SMALL_BLIND

        self.roles: set[PlayerRole] = set()

        # ==========================================
        # Chips
        # ==========================================

        self.chips = chips

        # ==========================================
        # Cards
        # ==========================================

        self.hand: list[Card] = []

        # ==========================================
        # Betting
        # ==========================================

        self.current_bet = 0

        self.total_bet = 0

        # ==========================================
        # State
        # ==========================================

        self.folded = False

        self.all_in = False

        self.eliminated = False

        self.last_action: Action | None = None

        # ==========================================
        # Statistics
        # ==========================================

        self.hands_played = 0

        self.hands_won = 0

        self.total_profit = 0
        # ==================================================
    # Round Management
    # ==================================================

    def reset_for_round(self):
        """
        Reset player state for a new hand.

        Keeps:
        - chips
        - statistics

        Resets:
        - cards
        - betting
        - roles
        - actions
        """

        self.clear_hand()

        self.clear_betting()

        self.folded = False

        self.all_in = False

        self.last_action = None

        self.clear_roles()

    # --------------------------------------------------

    def reset_betting_round(self):
        """
        Reset betting information
        for a new street.
        """

        self.current_bet = 0

    # --------------------------------------------------

    def clear_betting(self):
        """
        Completely clear betting data.

        Used when starting a new hand.

        Resets:
        - current street bet
        - total hand contribution
        """

        self.current_bet = 0

        self.total_bet = 0

    # ==================================================
    # Roles
    # ==================================================

    def add_role(
        self,
        role: PlayerRole
    ):
        """
        Add temporary poker role.

        Example:

        Heads-up player:
            DEALER
            SMALL_BLIND
        """

        self.roles.add(role)

    # --------------------------------------------------

    def remove_role(
        self,
        role: PlayerRole
    ):

        self.roles.discard(role)

    # --------------------------------------------------

    def has_role(
        self,
        role: PlayerRole
    ) -> bool:

        return role in self.roles

    # --------------------------------------------------

    def clear_roles(self):

        self.roles.clear()

    # --------------------------------------------------

    def is_dealer(self):

        return self.has_role(
            PlayerRole.DEALER
        )

    # --------------------------------------------------

    def is_small_blind(self):

        return self.has_role(
            PlayerRole.SMALL_BLIND
        )

    # --------------------------------------------------

    def is_big_blind(self):

        return self.has_role(
            PlayerRole.BIG_BLIND
        )

    # ==================================================
    # Cards
    # ==================================================

    def receive_card(
        self,
        card: Card
    ):
        """
        Add hole card.
        """

        if len(self.hand) >= 2:

            raise ValueError(
                "Player already has two hole cards."
            )

        self.hand.append(card)

    # --------------------------------------------------

    def clear_hand(self):

        self.hand.clear()

    # --------------------------------------------------

    def has_cards(self):

        return len(self.hand) == 2

    # --------------------------------------------------

    def show_hand(self):

        if not self.hand:

            return "(No Cards)"

        return " ".join(

            str(card)

            for card in self.hand

        )
        # ==================================================
    # Position
    # ==================================================

    def set_position(
        self,
        position: PlayerPosition
    ):
        """
        Assign table position.
        """

        self.position = position

    # --------------------------------------------------

    def is_button(self):

        return (

            self.position

            ==

            PlayerPosition.BUTTON

        )

    # ==================================================
    # Actions
    # ==================================================

    def set_last_action(
        self,
        action: Action
    ):
        """
        Store latest poker action.
        """

        self.last_action = action

    # --------------------------------------------------

    def fold(self):

        self.folded = True

        self.last_action = Action.FOLD

    # --------------------------------------------------

    def check(self):

        self.last_action = Action.CHECK

    # --------------------------------------------------

    def call(self):

        self.last_action = Action.CALL

    # --------------------------------------------------

    def bet(self):

        self.last_action = Action.BET

    # --------------------------------------------------

    def raise_bet(self):

        self.last_action = Action.RAISE

    # ==================================================
    # Betting
    # ==================================================

    def place_bet(
        self,
        amount: int
    ) -> int:
        """
        Move chips into the pot.

        Returns actual amount placed.
        """

        if amount < 0:

            raise ValueError(
                "Bet amount cannot be negative."
            )

        if amount == 0:

            return 0

        actual_amount = min(

            amount,

            self.chips

        )

        self.chips -= actual_amount

        self.current_bet += actual_amount

        self.total_bet += actual_amount

        if self.chips == 0:

            self.all_in = True

        return actual_amount

    # --------------------------------------------------

    def win_chips(
        self,
        amount: int
    ):
        """
        Add chips after winning pot.
        """

        if amount < 0:

            raise ValueError(
                "Cannot win negative chips."
            )

        self.chips += amount

        self.total_profit += amount

    # --------------------------------------------------

    def lose_chips(
        self,
        amount: int
    ):
        """
        Record lost chips.
        """

        if amount < 0:

            raise ValueError(
                "Cannot lose negative chips."
            )

        self.total_profit -= amount

    # --------------------------------------------------

    def go_all_in(self) -> int:
        """
        Push entire stack.
        """

        self.last_action = Action.ALL_IN

        return self.place_bet(

            self.chips

        )
        # ==================================================
    # Status
    # ==================================================

    def is_active(self) -> bool:
        """
        Player is still participating
        in current hand.
        """

        return (

            not self.folded

            and

            not self.eliminated

        )

    # --------------------------------------------------

    def can_act(self) -> bool:
        """
        Check whether player can make an action.
        """

        return (

            not self.folded

            and

            not self.all_in

            and

            not self.eliminated

        )

    # --------------------------------------------------

    def is_all_in(self) -> bool:
        """
        Returns True if player is all-in.
        """

        return self.all_in

    # --------------------------------------------------

    def is_folded(self) -> bool:

        return self.folded

    # --------------------------------------------------

    def is_busted(self) -> bool:
        """
        Player eliminated from tournament.
        """

        return self.eliminated

    # --------------------------------------------------

    def has_chips(self) -> bool:

        return self.chips > 0

    # ==================================================
    # Betting Helpers
    # ==================================================

    @property
    def stack_size(self) -> int:
        """
        Remaining chips.
        """

        return self.chips

    # --------------------------------------------------

    @property
    def invested(self) -> int:
        """
        Total chips invested
        in current hand.
        """

        return self.total_bet

    # --------------------------------------------------

    def needs_to_call(
        self,
        current_bet: int
    ) -> int:
        """
        Return chips required to call.
        """

        return max(

            0,

            current_bet - self.current_bet

        )

    # ==================================================
    # Tournament
    # ==================================================

    def eliminate(self):
        """
        Remove player from tournament.
        """

        self.eliminated = True

    # ==================================================
    # Statistics
    # ==================================================

    def record_hand(self):
        """
        Record played hand.
        """

        self.hands_played += 1

    # --------------------------------------------------

    def record_win(
        self,
        amount: int = 1
    ):
        """
        Record won hand(s).
        """

        self.hands_won += amount

    # --------------------------------------------------

    @property
    def win_rate(self) -> float:

        if self.hands_played == 0:

            return 0.0

        return (

            self.hands_won

            /

            self.hands_played

        )

    # --------------------------------------------------

    def reset_statistics(self):
        """
        Reset lifetime statistics.
        """

        self.hands_played = 0

        self.hands_won = 0

        self.total_profit = 0
        # ==================================================
    # Debug
    # ==================================================

    def __repr__(self):

        return (

            "Player("

            f"name='{self.name}', "

            f"chips={self.chips}, "

            f"position={self.position}, "

            f"roles={list(self.roles)}"

            ")"

        )

    # --------------------------------------------------

    def __str__(self):

        player_type = (

            "AI"

            if self.is_ai

            else "Human"

        )

        roles = ", ".join(

            str(role)

            for role in sorted(

                self.roles,

                key=lambda r: r.value

            )

        )

        if not roles:

            roles = "None"

        return (

            f"{self.name} "

            f"[{player_type}] | "

            f"Position: {self.position} | "

            f"Roles: {roles} | "

            f"Chips: ${self.chips}"

        )