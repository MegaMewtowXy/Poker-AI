from engine.betting import BettingEngine
from engine.betting_round import BettingRound
from engine.dealer import Dealer
from engine.game_state import GameState
from engine.pot_manager import PotManager
from engine.showdown import Showdown

from models.deck import Deck
from models.player import Player
from models.table import Table


class Game:
    """
    Main Texas Hold'em game controller.

    Responsibilities
    ----------------
    • Manage the game lifecycle
    • Coordinate engine components
    • Start and end hands
    • Control game flow

    This class does NOT:
        • Evaluate hands
        • Move chips directly
        • Resolve betting
        • Determine winners
    """

    def __init__(
        self,
        players: list[Player]
    ):

        if len(players) < 2:

            raise ValueError(
                "At least two players are required."
            )

        self.players = players

        # ==========================================
        # Game Components
        # ==========================================

        self.table = Table()

        self.deck = Deck()

        self.dealer = Dealer(
            self.deck
        )

        self.pot_manager = PotManager()

        self.betting_engine = BettingEngine(
            self.table,
            self.pot_manager
        )

        self.betting_round = BettingRound(
            self.players,
            self.table
        )

        self.showdown = Showdown()

        # ==========================================
        # Game State
        # ==========================================

        self.state = GameState.WAITING

        self.hand_number = 0

        self.running = False

    # ==================================================
    # Game Lifecycle
    # ==================================================

    def start_game(self):
        """
        Start the poker game.
        """

        self.running = True

        self.state = GameState.WAITING

    # --------------------------------------------------

    def stop_game(self):
        """
        Stop the poker game.
        """

        self.running = False

    # --------------------------------------------------

    def is_running(self) -> bool:

        return self.running

    # --------------------------------------------------

    def current_hand(self) -> int:

        return self.hand_number
        # ==================================================
    # Hand Lifecycle
    # ==================================================

    def start_hand(self):
        """
        Start a new hand.
        """

        self.hand_number += 1

        self.state = GameState.PRE_FLOP

        self.reset_hand()

        self.rotate_dealer()

        self.assign_positions()

        self.post_blinds()

        self.deal_hole_cards()

    # --------------------------------------------------

    def reset_hand(self):
        """
        Prepare every component for a new hand.
        """

        self.deck.reset()

        self.deck.shuffle()

        self.table.reset_for_round()

        self.pot_manager.reset()

        self.betting_round.reset()

        for player in self.players:

            player.reset_for_round()

    # --------------------------------------------------

    def rotate_dealer(self):
        """
        Move the dealer button.
        """

        self.dealer.rotate_dealer(

            self.table,

            len(self.players)

        )

    # --------------------------------------------------

    def assign_positions(self):
        """
        Assign poker positions.
        """

        self.dealer.assign_positions(

            self.players,

            self.table

        )

    # --------------------------------------------------

    def post_blinds(self):
        """
        Post the small and big blinds.
        """

        small_blind = None

        big_blind = None

        for player in self.players:

            position = player.position

            if position.name == "SMALL_BLIND":

                small_blind = player

            elif position.name == "BIG_BLIND":

                big_blind = player

        if small_blind is None:

            raise RuntimeError(
                "Small blind not found."
            )

        if big_blind is None:

            raise RuntimeError(
                "Big blind not found."
            )

        self.betting_engine.post_small_blind(

            small_blind

        )

        self.betting_engine.post_big_blind(

            big_blind

        )

    # --------------------------------------------------

    def deal_hole_cards(self):
        """
        Deal two private cards to every
        active player.
        """

        self.dealer.deal_hole_cards(

            self.players

        )
        # ==================================================
    # Betting Streets
    # ==================================================

    def play_pre_flop(self):
        """
        Run the pre-flop betting round.
        """

        self.state = GameState.PRE_FLOP

        self.play_betting_round()

    # --------------------------------------------------

    def play_flop(self):
        """
        Deal the flop and run betting.
        """

        self.state = GameState.FLOP

        self.dealer.deal_flop(
            self.table
        )

        self.betting_round.reset_for_new_street()

        self.play_betting_round()

    # --------------------------------------------------

    def play_turn(self):
        """
        Deal the turn and run betting.
        """

        self.state = GameState.TURN

        self.dealer.deal_turn(
            self.table
        )

        self.betting_round.reset_for_new_street()

        self.play_betting_round()

    # --------------------------------------------------

    def play_river(self):
        """
        Deal the river and run betting.
        """

        self.state = GameState.RIVER

        self.dealer.deal_river(
            self.table
        )

        self.betting_round.reset_for_new_street()

        self.play_betting_round()

    # ==================================================
    # Betting
    # ==================================================

    def play_betting_round(self):
        """
        Execute one betting street.

        Actual player decisions are handled
        externally (UI / AI). This method
        advances until the betting round ends.
        """

        self.betting_round.start()

        while self.betting_round.can_continue():

            current_player = (
                self.betting_round.current_player()
            )

            #
            # Human / AI decision happens here.
            #
            # Examples:
            #
            # fold
            # check
            # call
            # bet
            # raise
            # all-in
            #
            # The chosen action should call the
            # appropriate BettingEngine method.
            #

            break

        self.betting_round.finish()
        # ==================================================
    # Showdown
    # ==================================================

    def play_showdown(self):
        """
        Resolve the showdown.
        """

        self.state = GameState.SHOWDOWN

        return self.showdown.resolve(

            self.players,

            self.table.community_cards,

            self.pot_manager

        )

    # --------------------------------------------------

    def finish_hand(self):
        """
        Finish the current hand.
        """

        self.play_showdown()

        self.eliminate_busted_players()

        self.state = GameState.HAND_COMPLETE

    # ==================================================
    # Player Management
    # ==================================================

    def eliminate_busted_players(self):
        """
        Eliminate players with no chips.
        """

        for player in self.players:

            if (

                player.chips == 0

                and

                not player.eliminated

            ):

                player.eliminate()

    # --------------------------------------------------

    def active_players(self) -> list[Player]:
        """
        Return every player still in
        the tournament.
        """

        return [

            player

            for player in self.players

            if not player.eliminated

        ]

    # --------------------------------------------------

    def active_player_count(self) -> int:
        """
        Number of players still in
        the tournament.
        """

        return len(

            self.active_players()

        )

    # ==================================================
    # Hand Flow
    # ==================================================

    def play_hand(self):
        """
        Play one complete hand.
        """

        self.start_hand()

        self.play_pre_flop()

        if self.active_player_count() > 1:

            self.play_flop()

        if self.active_player_count() > 1:

            self.play_turn()

        if self.active_player_count() > 1:

            self.play_river()

        self.finish_hand()
        # ==================================================
    # Tournament
    # ==================================================

    def next_hand(self):
        """
        Prepare for the next hand.
        """

        if self.is_game_over():

            return

        self.start_hand()

    # --------------------------------------------------

    def is_game_over(self) -> bool:
        """
        Returns True when only one player
        remains in the tournament.
        """

        return self.active_player_count() <= 1

    # --------------------------------------------------

    def winner(self) -> Player | None:
        """
        Return the tournament winner.
        """

        if not self.is_game_over():

            return None

        active = self.active_players()

        if not active:

            return None

        return active[0]

    # --------------------------------------------------

    def reset_game(self):
        """
        Reset the entire game.
        """

        self.running = False

        self.hand_number = 0

        self.state = GameState.WAITING

        self.table.reset()

        self.pot_manager.reset()

        self.betting_round.reset()

        for player in self.players:

            player.reset_for_round()

            player.eliminated = False

    # ==================================================
    # Debug
    # ==================================================

    def __repr__(self):

        return (

            "Game("

            f"players={len(self.players)}, "

            f"hand={self.hand_number}, "

            f"state={self.state.name}"

            ")"

        )

    # --------------------------------------------------

    def __str__(self):

        return (

            "========== GAME ==========\n"

            f"Players      : {len(self.players)}\n"

            f"Hand         : {self.hand_number}\n"

            f"State        : {self.state.name}\n"

            f"Running      : {self.running}"

        )