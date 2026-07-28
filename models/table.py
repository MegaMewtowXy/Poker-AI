from models.card import Card


class Table:

    def __init__(self):
        self.community_cards = []

        self.pot = 0

        self.dealer_position = 0

        self.small_blind = 10
        self.big_blind = 20

    def add_community_card(self, card: Card):
        """Add a community card to the table."""
        self.community_cards.append(card)

    def reset_table(self):
        """Reset the table for a new round."""
        self.community_cards.clear()
        self.pot = 0

    def add_to_pot(self, amount: int):
        """Add chips to the pot."""
        self.pot += amount

    def rotate_dealer(self, total_players: int):
        """Move dealer button to the next player."""
        self.dealer_position = (self.dealer_position + 1) % total_players

    def show_community_cards(self):
        """Return community cards as a string."""
        return " ".join(str(card) for card in self.community_cards)

    def __str__(self):
        return (
            f"Pot: {self.pot}\n"
            f"Dealer Position: {self.dealer_position}\n"
            f"Community Cards: {self.show_community_cards()}"
        )