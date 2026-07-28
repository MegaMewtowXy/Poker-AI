from models.card import Card
from models.street import Street



class Table:
    """
    Represents the physical poker table.

    Responsibilities
    ----------------
    • Community cards
    • Dealer button position
    • Blind values
    • Betting state
    • Current street
    • Hand counter

    Does NOT handle:
    • Players
    • Pot management
    • Betting decisions
    • AI
    """



    def __init__(
        self,
        small_blind: int = 10,
        big_blind: int = 20
    ):


        # =====================================
        # Validation
        # =====================================

        self.validate_blinds(
            small_blind,
            big_blind
        )



        # =====================================
        # Community Cards
        # =====================================

        self.community_cards: list[Card] = []



        # =====================================
        # Dealer Button
        # =====================================

        self.dealer_position = 0



        # =====================================
        # Blinds
        # =====================================

        self.small_blind = small_blind

        self.big_blind = big_blind



        # =====================================
        # Betting State
        # =====================================

        self.current_bet = 0

        self.minimum_raise = big_blind



        # =====================================
        # Hand State
        # =====================================

        self.street = Street.PRE_FLOP

        self.hand_number = 1



    # ==================================================
    # Validation
    # ==================================================


    def validate_blinds(
        self,
        small_blind,
        big_blind
    ):

        if small_blind <= 0:

            raise ValueError(
                "Small blind must be positive."
            )


        if big_blind <= small_blind:

            raise ValueError(
                "Big blind must be greater than small blind."
            )



    # ==================================================
    # Community Cards
    # ==================================================


    def add_community_card(
        self,
        card: Card
    ):

        if len(self.community_cards) >= 5:

            raise RuntimeError(
                "Board already has five cards."
            )


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


    def board_size(self):

        return len(
            self.community_cards
        )



    # --------------------------------------------------


    def flop_dealt(self):

        return self.board_size() >= 3



    # --------------------------------------------------


    def turn_dealt(self):

        return self.board_size() >= 4



    # --------------------------------------------------


    def river_dealt(self):

        return self.board_size() == 5



    # --------------------------------------------------


    def board_complete(self):

        return self.board_size() == 5



    # --------------------------------------------------


    def can_add_card(self):

        return self.board_size() < 5



    # --------------------------------------------------


    def cards_needed(self):

        return 5 - self.board_size()



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


    def next_street(self):

        transitions = {

            Street.PRE_FLOP:
                Street.FLOP,

            Street.FLOP:
                Street.TURN,

            Street.TURN:
                Street.RIVER,

            Street.RIVER:
                Street.SHOWDOWN

        }


        if self.street in transitions:

            self.street = transitions[
                self.street
            ]



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
    # Betting State
    # ==================================================


    def reset_betting(self):

        self.current_bet = 0

        self.minimum_raise = self.big_blind



    # ==================================================
    # Dealer Button
    # ==================================================


    def rotate_dealer(
        self,
        total_players: int
    ):

        if total_players <= 0:

            raise ValueError(
                "Table requires players."
            )


        self.dealer_position = (

            self.dealer_position + 1

        ) % total_players



    # ==================================================
    # Blind Management
    # ==================================================


    def update_blinds(
        self,
        small_blind,
        big_blind
    ):

        self.validate_blinds(
            small_blind,
            big_blind
        )


        self.small_blind = small_blind

        self.big_blind = big_blind

        self.minimum_raise = big_blind



    # ==================================================
    # Hand Management
    # ==================================================


    def next_hand(self):

        self.hand_number += 1



    # --------------------------------------------------


    def reset_for_round(self):

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

        return len(
            self.community_cards
        ) > 0



    # --------------------------------------------------


    def clear(self):

        self.reset_for_round()


        # --------------------------------------------------

    def reset(self):
        """
        Backward-compatible alias.

        Older engine code calls table.reset().
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

            "========== TABLE ==========\n"

            f"Hand Number   : {self.hand_number}\n"

            f"Street        : {self.street}\n"

            f"Dealer Button : {self.dealer_position}\n"

            f"Small Blind   : ${self.small_blind}\n"

            f"Big Blind     : ${self.big_blind}\n"

            f"Current Bet   : ${self.current_bet}\n"

            f"Min Raise     : ${self.minimum_raise}\n"

            f"Board         : {self.show_community_cards()}"

        )