from models.card import Card


class Player:

    def __init__(self, name: str, chips: int = 1000, is_ai: bool = False):
        self.name = name
        self.chips = chips
        self.is_ai = is_ai

        self.hand = []

        self.current_bet = 0

        self.folded = False
        self.all_in = False

    def receive_card(self, card: Card):
        """Add a card to the player's hand."""
        self.hand.append(card)

    def clear_hand(self):
        """Prepare player for a new round."""
        self.hand.clear()
        self.current_bet = 0
        self.folded = False
        self.all_in = False

    def place_bet(self, amount: int):
        """Place a bet."""

        if amount >= self.chips:
            amount = self.chips
            self.all_in = True

        self.chips -= amount
        self.current_bet += amount

        return amount

    def fold(self):
        """Fold the current hand."""
        self.folded = True

    def show_hand(self):
        """Return the player's cards as a string."""
        return " ".join(str(card) for card in self.hand)

    def __str__(self):
        player_type = "AI" if self.is_ai else "Human"
        return f"{self.name} ({player_type}) - Chips: {self.chips}"