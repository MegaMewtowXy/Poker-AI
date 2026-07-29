from engine.betting import BettingEngine
from engine.betting_round import BettingRound
from engine.dealer import Dealer
from engine.game_state import GameState
from engine.pot_manager import PotManager
from engine.showdown import Showdown


from models import player
from models.deck import Deck
from models.player import Player
from models.player_role import PlayerRole
from models.table import Table
from models.street import Street
from models.action import Action
from models.player_position import PlayerPosition

from AI.game_context import GameContext

from simulation.logger import GameLogger





class Game:
    """
    Main Texas Hold'em game controller.

    Supports:

    - Human vs Human
    - Human vs AI
    - AI vs Human
    - AI vs AI


    Responsibilities:

    • Manage hand lifecycle
    • Control streets
    • Request player decisions
    • Coordinate engine systems


    Does NOT:

    • Calculate hand strength
    • Decide AI strategy
    • Move chips directly
    """





    def __init__(
        self,
        players: list[Player],
        logger: GameLogger = None
    ):


        if len(players) < 2:

            raise ValueError(
                "At least two players are required."
            )



        self.players = players


        self.logger = logger





        # ==========================================
        # Core Systems
        # ==========================================


        self.table = Table()


        self.deck = Deck()


        self.dealer = Dealer(

            self.deck

        )


        self.pot_manager = PotManager()





        # BettingRound first

        self.betting_round = BettingRound(

            self.players,

            self.table,

            self.logger

        )





        # BettingEngine connects to round

        self.betting_engine = BettingEngine(

            self.table,

            self.pot_manager,

            self.betting_round

        )





        self.showdown = Showdown()





        # ==========================================
        # State
        # ==========================================


        self.state = GameState.WAITING


        self.hand_number = 0


        self.running = False
        # ==========================================
    # Start Hand
    # ==========================================

    def start_hand(
        self
    ):
        """
        Initialize a new poker hand.
        """

        self.hand_number += 1


        self.state = GameState.PRE_FLOP



        # Reset systems

        self.deck.reset()

        self.table.reset()

        self.pot_manager.reset()

        self.betting_round.reset()

        # Reset players
        for player in self.players:
            player.reset_for_round()
            if hasattr(player, "new_hand"):
                player.new_hand()


        # Shuffle

        self.deck.shuffle()



        # Assign seats

        self.assign_positions()
        # ======================================
        # Logger
        # ======================================
        
        if self.logger:
            self.logger.start_hand(
        
                self.players,
        
                self.table.small_blind,

                self.table.big_blind,
        
                self.dealer.dealer_position
        
                    )


        # Post blinds

        self.post_blinds()
        

        # Deal hole cards

        self.dealer.deal_hole_cards(

            self.players

        )





        



        if self.logger:
            for player in self.players:
                self.logger.log_hole_cards(
                    player,
                    player.hand
                )








    # ==========================================
    # Reset Hand
    # ==========================================

    def reset_hand(
        self
    ):
        """
        Reset current hand only.
        """



        for player in self.players:


            player.reset_for_round()





        self.table.reset()


        self.deck.reset()


        self.pot_manager.reset()


        self.betting_round.reset()



        self.state = GameState.WAITING





    # ==========================================
    # Assign Positions
    # ==========================================

    def assign_positions(
    self
):
        """
        Assign dealer button,
        blinds and roles.
        """



        # Clear previous roles

        for player in self.players:

            player.clear_roles()



        n = len(self.players)
        btn_idx = (self.hand_number - 1) % n

        if n == 2:
            dealer = self.players[btn_idx]
            big_blind = self.players[(btn_idx + 1) % n]

            dealer.set_position(PlayerPosition.BUTTON)
            dealer.add_role(PlayerRole.DEALER)
            dealer.add_role(PlayerRole.SMALL_BLIND)

            big_blind.set_position(PlayerPosition.BIG_BLIND)
            big_blind.add_role(PlayerRole.BIG_BLIND)
            self.dealer.dealer_position = dealer.name
        else:
            dealer = self.players[btn_idx]
            sb_player = self.players[(btn_idx + 1) % n]
            bb_player = self.players[(btn_idx + 2) % n]

            dealer.set_position(PlayerPosition.BUTTON)
            dealer.add_role(PlayerRole.DEALER)

            sb_player.add_role(PlayerRole.SMALL_BLIND)
            bb_player.add_role(PlayerRole.BIG_BLIND)
            bb_player.set_position(PlayerPosition.BIG_BLIND)

            self.dealer.dealer_position = dealer.name

    # ==========================================
    # Post Blinds
    # ==========================================

    # ==========================================
# Post Blinds
# ==========================================

    def post_blinds(
        self
    ):
        """
        Post the small blind and big blind.
        """

        small_blind_player = None
        big_blind_player = None

        for player in self.players:

            if player.has_role(PlayerRole.SMALL_BLIND):
                small_blind_player = player

            elif player.has_role(PlayerRole.BIG_BLIND):
                big_blind_player = player

        if small_blind_player is None:
            raise RuntimeError("Small blind player not found.")

        if big_blind_player is None:
            raise RuntimeError("Big blind player not found.")

        # Post blinds
        self.betting_engine.post_blind(
            small_blind_player,
            self.table.small_blind
        )

        self.betting_engine.post_blind(
            big_blind_player,
            self.table.big_blind
        )

        # Update table betting state
        self.table.current_bet = self.table.big_blind
        self.table.minimum_raise = self.table.big_blind        
    # ==========================================
    # Deal Flop
    # ==========================================

    def deal_flop(
        self
    ):
        """
        Deal first three community cards.
        """



        self.dealer.deal_flop(

            self.table

        )
        self.table.reset_betting()

        for player in self.players:
            player.reset_betting_round()

       


        self.state = GameState.FLOP



        self.betting_round.set_street(

            Street.FLOP

        )





        if self.logger:


            self.logger.log_community_cards(

                self.table.community_cards

            )







    # ==========================================
    # Deal Turn
    # ==========================================

    def deal_turn(
        self
    ):
        """
        Deal fourth community card.
        """



        self.dealer.deal_turn(

            self.table

        )

        self.table.reset_betting()

        for player in self.players:
            player.reset_betting_round()

       
        self.state = GameState.TURN



        self.betting_round.set_street(

            Street.TURN

        )





        if self.logger:


            self.logger.log_community_cards(

                [

                    self.table.community_cards[-1]

                ]

            )







    # ==========================================
    # Deal River
    # ==========================================

    def deal_river(
        self
    ):
        """
        Deal fifth community card.
        """



        self.dealer.deal_river(

            self.table

        )

        for player in self.players:
            player.reset_betting_round()


        self.state = GameState.RIVER



        self.betting_round.set_street(

            Street.RIVER

        )





        if self.logger:


            self.logger.log_community_cards(

                [

                    self.table.community_cards[-1]

                ]

            )







    # ==========================================
    # Create AI Context
    # ==========================================

    def create_context(
        self,
        player: Player
    ):
        """
        Create information available
        to AI player.
        """



        call_amount = max(

            0,

            self.table.current_bet

            -

            player.current_bet

        )





        return GameContext(

            hole_cards=player.hand,


            community_cards=self.table.community_cards,


            position=getattr(

                player,

                "position",

                None

            ),


            street=self.betting_round.street,


            pot_size=self.pot_manager.total_pot(),


            current_bet=self.table.current_bet,

            player_current_bet=player.current_bet,

            call_amount=call_amount,


            min_raise=self.table.minimum_raise,


            big_blind=self.table.big_blind,


            player_stack=player.chips,


            players_remaining=len(

                [

                    p

                    for p in self.players

                    if not p.folded

                ]

            ),


            betting_history=self.betting_round.action_history.copy()

        )
        # ==========================================
    # Get Player Decision
    # ==========================================

    def get_player_action(
        self,
        player
    ):
        """
        Get action from human or AI player.
        """



        # ======================================
        # AI Player
        # ======================================

        if hasattr(
            player,
            "decide"
        ):
            context = self.create_context(
                player
            )

            # Determine primary opponent name
            opponent_name = None
            active_opponents = [p.name for p in self.players if p != player and not getattr(p, "folded", False)]
            if not active_opponents:
                active_opponents = [p.name for p in self.players if p != player]
            if active_opponents:
                opponent_name = active_opponents[0]

            return player.decide(
                context,
                opponent_name=opponent_name
            )






        # ======================================
        # Human Player
        # ======================================

        return self.get_human_action(

            player

        )





    # ==========================================
    # Human Input
    # ==========================================

    def get_human_action(
        self,
        player
    ):
        """
        Temporary console input.

        Can later be replaced by:
        - GUI
        - Web
        - Mobile
        """



        print()

        print(

            f"{player.name}'s turn"

        )


        print(

            "1. Fold"

        )

        print(

            "2. Check"

        )

        print(

            "3. Call"

        )

        print(

            "4. Bet"

        )

        print(

            "5. Raise"

        )

        print(

            "6. All In"

        )





        choice = int(

            input(

                "Choose action: "

            )

        )





        if choice == 1:

            return {

                "action": Action.FOLD,

                "amount": 0

            }





        elif choice == 2:

            return {

                "action": Action.CHECK,

                "amount": 0

            }





        elif choice == 3:

            return {

                "action": Action.CALL,

                "amount": 0

            }





        elif choice == 4:

            amount = int(

                input(

                    "Bet amount: "

                )

            )


            return {

                "action": Action.BET,

                "amount": amount

            }





        elif choice == 5:

            amount = int(

                input(

                    "Raise amount: "

                )

            )


            return {

                "action": Action.RAISE,

                "amount": amount

            }





        elif choice == 6:

            return {

                "action": Action.ALL_IN,

                "amount": 0

            }





        else:

            raise ValueError(

                "Invalid action."

            )







    # ==========================================
    # Execute Betting Round
    # ==========================================

    def play_betting_round(
        self
    ):
        """
        Execute one complete betting street.
        """



        self.betting_round.start()





        while not self.betting_round.betting_complete():



            player = self.betting_round.current_player()





            if player is None:

                break





            if not player.can_act():


                self.betting_round.next_player()

                continue





            decision = self.get_player_action(

                player

            )





            if decision is None:

                raise ValueError(

                    f"{player.name} returned no action."

                )





            action = decision.get(

                "action"

            )


            amount = decision.get(

                "amount",

                0

            )





            # ==================================
            # Send to Betting Engine
            # ==================================

            if action == Action.FOLD:


                self.betting_engine.fold(

                    player

                )



            elif action == Action.CHECK:


                self.betting_engine.check(

                    player

                )



            elif action == Action.CALL:


                self.betting_engine.call(

                    player

                )



            elif action == Action.BET:

                print("\n========== BET DEBUG ==========")
                print("Street            :", self.betting_round.street)
                print("Table Current Bet :", self.table.current_bet)
                print("Player Current Bet:", player.current_bet)
                print("Call Amount       :", self.table.current_bet - player.current_bet)
                print("Amount            :", amount)
                print("===============================\n")
                self.betting_engine.bet(

                    player,

                    amount

                )



            elif action == Action.RAISE:
                
                self.betting_engine.raise_bet(

                    player,

                    amount

                )



            elif action == Action.ALL_IN:


                self.betting_engine.all_in(

                    player

                )



            else:
                raise ValueError(
                    f"Unknown action: {action}"
                )

            # Broadcast action to other players for real-time tracking
            for other in self.players:
                if other != player and hasattr(other, "record_opponent_action"):
                    other.record_opponent_action(
                        player.name,
                        action,
                        getattr(player, "position", None)
                    )

            self.betting_round.next_player()






        self.betting_round.finish()





        if self.logger:


            self.logger.log_pot(

                self.pot_manager.total_pot()

            )





        return True
        # ==========================================
    # Play Complete Hand
    # ==========================================

    def play_hand(
        self
    ):
        """
        Run one complete Texas Hold'em hand.
        """



        self.start_hand()





        # ------------------------------
        # Pre Flop
        # ------------------------------

        self.betting_round.set_street(

            Street.PRE_FLOP

        )


        self.play_betting_round()





        # ------------------------------
        # Flop
        # ------------------------------

        self.deal_flop()


        self.play_betting_round()





        # ------------------------------
        # Turn
        # ------------------------------

        self.deal_turn()


        self.play_betting_round()





        # ------------------------------
        # River
        # ------------------------------

        self.deal_river()


        self.play_betting_round()





        return self.finish_hand()








    # ==========================================
    # Finish Hand
    # ==========================================

    def finish_hand(
        self
    ):
        """
        Determine winner and
        complete hand.
        """



        active_players = [

            player

            for player in self.players

            if not player.folded

        ]





        # ======================================
        # Everyone folded except one
        # ======================================

        if len(active_players) == 1:


            winner = active_players[0]



            winner.chips += (

                self.pot_manager.total_pot()

            )





            if self.logger:


                self.logger.log_winner(

                    winner

                )


                self.logger.finish_hand(

                    self.players

                )





            self.state = GameState.HAND_COMPLETE





            return {


                "winner":

                    winner,


                "method":

                    "fold"

            }





        # ======================================
        # Showdown
        # ======================================

        self.betting_round.set_street(

            Street.SHOWDOWN

        )





        result = self.showdown.resolve(

            active_players,

            self.table.community_cards,
            self.pot_manager

        )





        winners = result.get(

            "winners",

            []

        )





        winner = None





        if winners:

            winner = winners[0] if winners else None




        # ======================================
        # Logger
        # ======================================

        if self.logger:


            if winner:


                self.logger.log_winner(

                    winner

                )



            self.logger.finish_hand(

                self.players

            )





        self.state = GameState.HAND_COMPLETE





        return {


            "winner":

                winner,


            "method":

                "showdown",


            "result":

                result

        }







    # ==========================================
    # Current State
    # ==========================================

    def get_state(
        self
    ):
        """
        Return current game state.
        """

        return self.state







    # ==========================================
    # Players
    # ==========================================

    def get_players(
        self
    ):
        """
        Return players.
        """

        return self.players.copy()







    # ==========================================
    # Reset Game
    # ==========================================

    def reset(
        self
    ):
        """
        Reset complete game.
        """



        self.table.reset()


        self.deck.reset()


        self.pot_manager.reset()


        self.betting_round.reset()



        if self.logger:

            self.logger.clear()





        for player in self.players:


            player.reset_for_round()





        self.state = GameState.WAITING


        self.hand_number = 0








    # ==========================================
    # Profile
    # ==========================================

    def profile(
        self
    ):
        """
        Return game information.
        """



        return {


            "players":

                [

                    player.name

                    for player in self.players

                ],



            "state":

                self.state.name

                if hasattr(

                    self.state,

                    "name"

                )

                else self.state,



            "hands_played":

                self.hand_number,



            "logger_enabled":

                self.logger is not None

        }







    # ==========================================
    # Debug
    # ==========================================

    def __str__(
        self
    ):

        return (

            f"Texas Hold'em Game | "

            f"Players: {len(self.players)}"

        )





    def __repr__(
        self
    ):

        return (

            f"Game("

            f"players={len(self.players)}, "

            f"logger={self.logger is not None})"

        )