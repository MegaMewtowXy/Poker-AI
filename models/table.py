from models.card import Card


class Table:
    """
    Represents the physical poker table.
    """

    def __init__(
        self,
        small_blind: int = 10,
        big_blind: int = 20
    ):

        # -------------------------
        # Community Cards
        # -------------------------

        self.community_cards: list[Card] = []

        # -------------------------
        # Dealer Button
        # -------------------------

        self.dealer_position = 0

        # -------------------------
        # Blinds
        # -------------------------

        self.small_blind = small_blind
        self.big_blind = big_blind

        # -------------------------
        # Betting
        # -------------------------

        self.current_bet = 0

        self.minimum_raise = big_blind

    # =========================================

    def reset_for_round(self):

        self.community_cards.clear()

        self.current_bet = 0

        self.minimum_raise = self.big_blind

    # =========================================

    def add_community_card(
        self,
        card: Card
    ):

        self.community_cards.append(card)

    # =========================================

    def show_community_cards(self):

        return " ".join(
            str(card)
            for card in self.community_cards
        )

    # =========================================

    def rotate_dealer(
        self,
        total_players: int
    ):

        self.dealer_position = (
            self.dealer_position + 1
        ) % total_players

    # =========================================

    def __str__(self):

        return (
            f"Dealer Position : {self.dealer_position}\n"
            f"Current Bet     : {self.current_bet}\n"
            f"Minimum Raise   : {self.minimum_raise}\n"
            f"Community Cards : {self.show_community_cards()}"
        )