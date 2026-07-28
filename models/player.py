from models.card import Card


class Player:
    """
    Represents a poker player (Human or AI).
    """

    def __init__(
        self,
        name: str,
        chips: int = 1000,
        is_ai: bool = False
    ):

        self.name = name
        self.chips = chips
        self.is_ai = is_ai

        # -------------------------
        # Cards
        # -------------------------

        self.hand: list[Card] = []

        # -------------------------
        # Betting
        # -------------------------

        # Amount contributed during the CURRENT betting street
        self.current_bet = 0

        # Amount contributed during the ENTIRE hand
        self.total_bet = 0

        # -------------------------
        # Player Status
        # -------------------------

        self.folded = False

        self.all_in = False

        self.eliminated = False

    # ==================================================
    # Round Management
    # ==================================================

    def reset_for_round(self):
        """
        Prepare player for a new hand.
        """

        self.hand.clear()

        self.current_bet = 0

        self.total_bet = 0

        self.folded = False

        self.all_in = False

    def reset_betting_round(self):
        """
        Called after each betting street.
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

    def show_hand(self):

        return " ".join(
            str(card)
            for card in self.hand
        )

    # ==================================================
    # Betting
    # ==================================================

    def place_bet(
        self,
        amount: int
    ) -> int:
        """
        Put chips into the pot.

        Returns the ACTUAL amount bet.
        """

        if amount <= 0:
            return 0

        if amount >= self.chips:

            amount = self.chips

            self.all_in = True

        self.chips -= amount

        self.current_bet += amount

        self.total_bet += amount

        if self.chips == 0:

            self.all_in = True

        return amount

    def win_chips(
        self,
        amount: int
    ):

        self.chips += amount

    def fold(self):

        self.folded = True

    def check(self):

        pass

    def call(
        self,
        amount: int
    ):

        return self.place_bet(amount)

    def raise_bet(
        self,
        amount: int
    ):

        return self.place_bet(amount)

    def go_all_in(self):

        return self.place_bet(
            self.chips
        )

    # ==================================================
    # Status
    # ==================================================

    def is_active(self):

        return (
            not self.folded
            and not self.eliminated
        )

    def is_busted(self):

        return (
            self.chips <= 0
        )

    # ==================================================
    # String Representation
    # ==================================================

    def __str__(self):

        player_type = (
            "AI"
            if self.is_ai
            else "Human"
        )

        return (
            f"{self.name} "
            f"({player_type}) | "
            f"Chips: {self.chips}"
        )