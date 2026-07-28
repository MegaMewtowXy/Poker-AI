from models.action import Action
from models.card import Card
from models.player_position import PlayerPosition


class Player:
    """
    Represents a Texas Hold'em player.

    This class stores all player-related state used by
    the engine, AI, showdown, UI and tournament mode.
    """

    def __init__(
        self,
        name: str,
        chips: int,
        is_ai: bool = False
    ):

        # ==================================================
        # Identity
        # ==================================================

        self.name = name

        self.is_ai = is_ai

        # ==================================================
        # Table Position
        # ==================================================

        self.position: PlayerPosition = (
            PlayerPosition.UNKNOWN
        )

        # ==================================================
        # Chip Stack
        # ==================================================

        self.chips = chips

        # ==================================================
        # Hole Cards
        # ==================================================

        self.hand: list[Card] = []

        # ==================================================
        # Betting
        # ==================================================

        # Current betting street
        self.current_bet = 0

        # Total contribution this hand
        self.total_bet = 0

        # ==================================================
        # Player State
        # ==================================================

        self.folded = False

        self.all_in = False

        self.eliminated = False

        # Last poker action
        self.last_action: Action | None = None

        # ==================================================
        # Statistics
        # ==================================================

        self.hands_played = 0

        self.hands_won = 0

        self.total_profit = 0

    # ==================================================
    # Round Management
    # ==================================================

    def reset_for_round(self):
        """
        Prepare player for a new hand.
        """

        self.clear_hand()

        self.current_bet = 0

        self.total_bet = 0

        self.folded = False

        self.all_in = False

        self.last_action = None

    # --------------------------------------------------

    def reset_betting_round(self):
        """
        Reset betting information for a new street.
        """

        self.current_bet = 0

    # ==================================================
    # Cards
    # ==================================================

    def receive_card(
        self,
        card: Card
    ):

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

        self.position = position

    # ==================================================
    # Action
    # ==================================================

    def set_last_action(
        self,
        action: Action
    ):

        self.last_action = action
        # ==================================================
    # Betting
    # ==================================================

    def place_bet(
        self,
        amount: int
    ) -> int:
        """
        Place chips into the pot.

        Returns the actual amount placed.
        """

        if amount <= 0:
            return 0

        amount = min(amount, self.chips)

        self.chips -= amount

        self.current_bet += amount

        self.total_bet += amount

        if self.chips == 0:
            self.all_in = True

        return amount

    # --------------------------------------------------

    def win_chips(
        self,
        amount: int
    ):

        if amount < 0:
            raise ValueError(
                "Cannot win a negative amount."
            )

        self.chips += amount

        self.total_profit += amount

    # --------------------------------------------------

    def lose_chips(
        self,
        amount: int
    ):

        if amount < 0:
            raise ValueError(
                "Cannot lose a negative amount."
            )

        self.total_profit -= amount

    # --------------------------------------------------

    def go_all_in(self) -> int:
        """
        Push entire remaining stack.
        """

        self.last_action = Action.ALL_IN

        return self.place_bet(self.chips)

    # ==================================================
    # Player Actions
    # ==================================================

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
    # Status
    # ==================================================

    def is_active(self) -> bool:
        """
        Player is still participating in this hand.
        """

        return (

            not self.folded

            and

            not self.eliminated

        )

    # --------------------------------------------------

    def can_act(self) -> bool:
        """
        Player is allowed to make an action.
        """

        return (

            not self.folded

            and

            not self.all_in

            and

            not self.eliminated

        )

    # --------------------------------------------------

    def is_busted(self) -> bool:
        """
        Player has been eliminated from the game.
        """

        return self.eliminated

    # --------------------------------------------------

    def has_chips(self) -> bool:

        return self.chips > 0

    # ==================================================
    # Tournament
    # ==================================================

    def eliminate(self):

        self.eliminated = True

    # ==================================================
    # Statistics
    # ==================================================

    def record_hand(self):

        self.hands_played += 1

    # --------------------------------------------------

    def record_win(self):

        self.hands_won += 1

    # --------------------------------------------------

    @property
    def win_rate(self) -> float:

        if self.hands_played == 0:
            return 0.0

        return self.hands_won / self.hands_played

    # ==================================================
    # Utility
    # ==================================================

    def reset_statistics(self):

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

            f"position={self.position}"

            ")"

        )

    # --------------------------------------------------

    def __str__(self):

        player_type = (

            "AI"

            if self.is_ai

            else "Human"

        )

        position = str(self.position)

        return (

            f"{self.name} "

            f"[{player_type}] | "

            f"{position} | "

            f"Chips: ${self.chips}"

        )