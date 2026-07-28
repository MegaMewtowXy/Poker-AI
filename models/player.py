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

        # Cards
        self.hand: list[Card] = []

        # Betting
        self.current_bet = 0
        self.total_bet = 0

        # Status
        self.folded = False
        self.all_in = False
        self.eliminated = False

    # ----------------------------
    # Round Management
    # ----------------------------

    def reset_for_round(self):
        """
        Reset player state for a new round.
        """

        self.hand.clear()

        self.current_bet = 0
        self.total_bet = 0

        self.folded = False
        self.all_in = False

    # ----------------------------
    # Cards
    # ----------------------------

    def receive_card(self, card: Card):
        """
        Add a dealt card to the player's hand.
        """

        self.hand.append(card)

    def show_hand(self):
        """
        Return the player's cards.
        """

        return " ".join(str(card) for card in self.hand)

    # ----------------------------
    # Betting
    # ----------------------------

    def place_bet(self, amount: int) -> int:
        """
        Place chips into the pot.

        Returns
        -------
        int
            Actual amount bet.
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

    def win_chips(self, amount: int):
        """
        Award chips to the player.
        """

        self.chips += amount

    def fold(self):
        """
        Fold the current hand.
        """

        self.folded = True

    def check(self):
        """
        Placeholder for a check action.
        """

        pass

    def call(self, amount: int):
        """
        Call the current bet.
        """

        return self.place_bet(amount)

    def raise_bet(self, amount: int):
        """
        Raise the current bet.
        """

        return self.place_bet(amount)

    # ----------------------------
    # Status
    # ----------------------------

    def is_active(self) -> bool:
        """
        Returns True if the player is still active in the current hand.
        """

        return (
            not self.folded
            and not self.eliminated
        )

    def is_busted(self) -> bool:
        """
        Returns True if the player has no chips left.
        """

        return self.chips <= 0

    # ----------------------------
    # String Representation
    # ----------------------------

    def __str__(self):

        player_type = "AI" if self.is_ai else "Human"

        return (
            f"{self.name} "
            f"({player_type}) | "
            f"Chips: {self.chips}"
        )