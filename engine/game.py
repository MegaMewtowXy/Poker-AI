from engine.betting import BettingEngine
from engine.dealer import Dealer
from engine.game_state import GameState
from engine.pot_manager import PotManager
from engine.showdown import Showdown

from models.deck import Deck
from models.table import Table


class Game:
    """
    Main Texas Hold'em game controller.
    """

    def __init__(self, players):

        self.players = players

        self.table = Table()

        self.pot_manager = PotManager()

        self.deck = Deck()
        self.deck.shuffle()

        self.dealer = Dealer(self.deck)

        self.betting = BettingEngine(
            self.table,
            self.pot_manager
        )

        self.showdown_engine = Showdown()

        self.state = GameState.WAITING

    # ==================================================

    def start_round(self):

        print("\n========== NEW ROUND ==========\n")

        self.reset_round()

        self.post_blinds()

        self.pre_flop()

        self.betting_round()

        self.flop()

        self.betting_round()

        self.turn()

        self.betting_round()

        self.river()

        self.betting_round()

        self.showdown()

    # ==================================================

    def reset_round(self):

        self.deck = Deck()
        self.deck.shuffle()

        self.dealer = Dealer(self.deck)

        self.table.reset_for_round()

        self.pot_manager.reset()

        for player in self.players:

            player.reset_for_round()

    # ==================================================

    def post_blinds(self):

        sb = (
            self.table.dealer_position + 1
        ) % len(self.players)

        bb = (
            self.table.dealer_position + 2
        ) % len(self.players)

        self.betting.post_small_blind(
            self.players[sb]
        )

        self.betting.post_big_blind(
            self.players[bb]
        )

    # ==================================================

    def pre_flop(self):

        self.state = GameState.PRE_FLOP

        self.dealer.deal_hole_cards(
            self.players
        )

        print("Hole cards dealt.")

    # ==================================================

    def betting_round(self):

        print("\n========== BETTING ==========\n")

        print(
            f"Total Pot : ${self.pot_manager.total_pot()}"
        )

        print(
            f"Current Bet : ${self.table.current_bet}"
        )

        for player in self.players:

            if player.folded:
                continue

            print("--------------------------------")

            print(f"Player : {player.name}")

            print(f"Cards : {player.show_hand()}")

            print(f"Chips : {player.chips}")

            print(f"Current Bet : {player.current_bet}")

            print("--------------------------------")

    # ==================================================

    def flop(self):

        self.state = GameState.FLOP

        self.dealer.deal_flop(
            self.table
        )

        print(
            "\nFlop :",
            self.table.show_community_cards()
        )

    # ==================================================

    def turn(self):

        self.state = GameState.TURN

        self.dealer.deal_turn(
            self.table
        )

        print(
            "\nTurn :",
            self.table.show_community_cards()
        )

    # ==================================================

    def river(self):

        self.state = GameState.RIVER

        self.dealer.deal_river(
            self.table
        )

        print(
            "\nRiver :",
            self.table.show_community_cards()
        )

    # ==================================================

    def showdown(self):

        self.state = GameState.SHOWDOWN

        print("\n========== SHOWDOWN ==========\n")

        winner, result = self.showdown_engine.resolve(
            self.players,
            self.table.community_cards,
            self.pot_manager
        )

        print()

        print(
            f"Winner       : {winner.name}"
        )

        print(
            f"Winning Hand : {result.hand_name}"
        )

        print(
            f"Score        : {result.score}"
        )

        print(
            f"Pot Won      : ${self.pot_manager.total_pot()}"
        )