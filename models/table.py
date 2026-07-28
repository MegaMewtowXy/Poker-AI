from models.card import Card


class Table:
    """
    Represents the poker table.
    """

    def __init__(
        self,
        small_blind: int = 10,
        big_blind: int = 20
    ):
        # Community Cards
        self.community_cards: list[Card] = []

        # Pot
        self.pot = 0

        # Current highest bet in this betting round
        self.current_bet = 0

        # Dealer button position
        self.dealer_position = 0

        # Blind values
        self.small_blind = small_blind
        self.big_blind = big_blind

    # ------------------------------------
    # Round Management
    # ------------------------------------

    def reset_for_round(self):
        """
        Reset the table for a new hand.
        """

        self.community_cards.clear()

        self.pot = 0

        self.current_bet = 0

    # ------------------------------------
    # Community Cards
    # ------------------------------------

    def add_community_card(self, card: Card):
        """
        Add a community card.
        """

        self.community_cards.append(card)

    def show_community_cards(self):
        """
        Return community cards.
        """

        return " ".join(
            str(card)
            for card in self.community_cards
        )

    # ------------------------------------
    # Pot
    # ------------------------------------

    def add_to_pot(self, amount: int):
        """
        Add chips to the pot.
        """

        self.pot += amount

    # ------------------------------------
    # Betting
    # ------------------------------------

    def reset_betting_round(self):
        """
        Reset betting information for the
        next betting street.
        """

        self.current_bet = 0

    # ------------------------------------
    # Dealer
    # ------------------------------------

    def rotate_dealer(self, total_players: int):
        """
        Move dealer button clockwise.
        """

        self.dealer_position = (
            self.dealer_position + 1
        ) % total_players

    # ------------------------------------
    # String Representation
    # ------------------------------------

    def __str__(self):

        return (
            f"Pot: {self.pot}\n"
            f"Current Bet: {self.current_bet}\n"
            f"Dealer Position: {self.dealer_position}\n"
            f"Community Cards: {self.show_community_cards()}"
        )