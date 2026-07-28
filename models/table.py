from models.card import Card
from models.street import Street


class Table:
    """
    Represents the physical poker table.

    Responsibilities
    ----------------
    • Community cards
    • Dealer button
    • Blind values
    • Betting state
    • Current street
    • Hand counter

    Pot management is handled by PotManager.
    """

    def __init__(
        self,
        small_blind: int = 10,
        big_blind: int = 20
    ):

        # =====================================
        # Community Cards
        # =====================================

        self.community_cards: list[Card] = []

        # =====================================
        # Dealer
        # =====================================

        self.dealer_position = 0

        # =====================================
        # Blinds
        # =====================================

        self.small_blind = small_blind
        self.big_blind = big_blind

        # =====================================
        # Betting
        # =====================================

        self.current_bet = 0

        # Size of previous full raise
        self.minimum_raise = big_blind

        # =====================================
        # Hand State
        # =====================================

        self.street = Street.PRE_FLOP

        self.hand_number = 1

    # ==================================================
    # Community Cards
    # ==================================================

    def add_community_card(
        self,
        card: Card
    ):

        self.community_cards.append(card)

    # --------------------------------------------------

    def reset_board(self):

        self.community_cards.clear()

    # --------------------------------------------------

    def community_card(
        self,
        index: int
    ) -> Card:

        return self.community_cards[index]

    # --------------------------------------------------

    def board_size(self) -> int:

        return len(self.community_cards)

    # --------------------------------------------------

    def flop_dealt(self) -> bool:

        return self.board_size() >= 3

    # --------------------------------------------------

    def turn_dealt(self) -> bool:

        return self.board_size() >= 4

    # --------------------------------------------------

    def river_dealt(self) -> bool:

        return self.board_size() == 5

    # --------------------------------------------------

    def board_complete(self) -> bool:

        return self.board_size() == 5

    # --------------------------------------------------

    def show_community_cards(self):

        if not self.community_cards:
            return "(Empty)"

        return " ".join(

            str(card)

            for card in self.community_cards

        )
        # ==================================================
    # Street Management
    # ==================================================

    def set_street(
        self,
        street: Street
    ):

        self.street = street

    # --------------------------------------------------

    def is_pre_flop(self):

        return self.street == Street.PRE_FLOP

    # --------------------------------------------------

    def is_flop(self):

        return self.street == Street.FLOP

    # --------------------------------------------------

    def is_turn(self):

        return self.street == Street.TURN

    # --------------------------------------------------

    def is_river(self):

        return self.street == Street.RIVER

    # --------------------------------------------------

    def is_showdown(self):

        return self.street == Street.SHOWDOWN

    # ==================================================
    # Betting
    # ==================================================

    def reset_betting(self):
        """
        Called before every betting street.
        """

        self.current_bet = 0

        self.minimum_raise = self.big_blind

    # ==================================================
    # Dealer
    # ==================================================

    def rotate_dealer(
        self,
        total_players: int
    ):

        if total_players <= 0:

            raise ValueError(
                "Table must contain at least one player."
            )

        self.dealer_position = (

            self.dealer_position + 1

        ) % total_players

    # ==================================================
    # Hand Management
    # ==================================================

    def next_hand(self):
        """
        Increment hand counter.
        """

        self.hand_number += 1

    # --------------------------------------------------

    def reset_for_round(self):
        """
        Prepare the table for a new hand.
        """

        self.reset_board()

        self.reset_betting()

        self.street = Street.PRE_FLOP

    # ==================================================
    # Utility
    # ==================================================

    def board(self):

        return self.community_cards.copy()

    # --------------------------------------------------

    def has_board(self):

        return len(self.community_cards) > 0

    # --------------------------------------------------

    def clear(self):
        """
        Completely reset table state.
        """

        self.reset_for_round()

    # ==================================================
    # Debug
    # ==================================================

    def __repr__(self):

        return (

            "Table("

            f"Hand={self.hand_number}, "

            f"Street={self.street}, "

            f"Dealer={self.dealer_position}, "

            f"Board={self.show_community_cards()}"

            ")"

        )

    # --------------------------------------------------

    def __str__(self):

        return (

            f"========== TABLE ==========\n"

            f"Hand Number   : {self.hand_number}\n"

            f"Street        : {self.street}\n"

            f"Dealer Button : {self.dealer_position}\n"

            f"Small Blind   : ${self.small_blind}\n"

            f"Big Blind     : ${self.big_blind}\n"

            f"Current Bet   : ${self.current_bet}\n"

            f"Min Raise     : ${self.minimum_raise}\n"

            f"Board         : {self.show_community_cards()}"

        )