import os

import json

from simulation.hand_history import HandHistory





class ReplaySystem:
    """
    Poker hand replay system.


    Responsibilities
    ----------------
    • Load saved hand histories
    • Reconstruct hand timeline
    • Replay actions
    • Display hand information


    Does NOT
    --------
    • Run poker engine
    • Calculate outcomes
    • Make decisions
    • Modify game state
    """





    def __init__(
        self,
        history_directory="data/hand_history"
    ):

        self.history_directory = history_directory


        self.hands = []


        self.current_hand = None


        self.current_action = 0





    # ==========================================
    # Load Single Hand
    # ==========================================

    def load_hand(
        self,
        file_path
    ):
        """
        Load one hand history file.
        """



        if not os.path.exists(file_path):

            raise FileNotFoundError(

                "Hand history file not found."

            )





        with open(

            file_path,

            "r",

            encoding="utf-8"

        ) as file:


            data = json.load(file)





        hand = HandHistory()



        hand.from_dict(

            data

        )





        self.current_hand = hand


        self.current_action = 0





        return hand





    # ==========================================
    # Load All Hands
    # ==========================================

    def load_all(
        self
    ):
        """
        Load all saved hands.
        """



        path = os.path.join(

            self.history_directory,

            "all_hands.json"

        )





        if not os.path.exists(path):

            return []





        with open(

            path,

            "r",

            encoding="utf-8"

        ) as file:


            data = json.load(file)





        self.hands.clear()





        for item in data:


            hand = HandHistory()



            hand.from_dict(

                item

            )



            self.hands.append(

                hand

            )





        return self.hands
    
    # ==========================================
    # Start Replay
    # ==========================================

    def start_replay(
        self,
        hand
    ):
        """
        Start replaying selected hand.
        """



        self.current_hand = hand


        self.current_action = 0





        return self.get_summary()





    # ==========================================
    # Get Next Action
    # ==========================================

    def next_action(
        self
    ):
        """
        Return next recorded action.

        Moves replay pointer forward.
        """



        if self.current_hand is None:

            raise ValueError(

                "No hand loaded."

            )





        actions = self.current_hand.actions





        if self.current_action >= len(actions):

            return None





        action = actions[

            self.current_action

        ]





        self.current_action += 1





        return action





    # ==========================================
    # Replay All Actions
    # ==========================================

    def replay_actions(
        self
    ):
        """
        Return complete action timeline.
        """



        if self.current_hand is None:

            raise ValueError(

                "No hand loaded."

            )





        return self.current_hand.actions.copy()





    # ==========================================
    # Current Progress
    # ==========================================

    def progress(
        self
    ):
        """
        Return replay progress.
        """



        if self.current_hand is None:

            return {


                "loaded": False

            }





        return {


            "loaded": True,


            "current_action":

                self.current_action,


            "total_actions":

                len(

                    self.current_hand.actions

                ),


            "finished":

                self.current_action >= len(

                    self.current_hand.actions

                )

        }





    # ==========================================
    # Show Board
    # ==========================================

    def board_state(
        self
    ):
        """
        Return recorded community cards.
        """



        if self.current_hand is None:

            raise ValueError(

                "No hand loaded."

            )





        return self.current_hand.community_cards.copy()





    # ==========================================
    # Players
    # ==========================================

    def players(
        self
    ):
        """
        Return players in replay.
        """



        if self.current_hand is None:

            return []





        return self.current_hand.players.copy()
    
    # ==========================================
    # Hand Summary
    # ==========================================

    def get_summary(
        self
    ):
        """
        Return complete hand summary.
        """



        if self.current_hand is None:

            return {


                "loaded": False

            }





        return {


            "hand_id":

                self.current_hand.hand_id,



            "players":

                self.current_hand.players,



            "actions":

                len(

                    self.current_hand.actions

                ),



            "community_cards":

                self.current_hand.community_cards,



            "winner":

                self.current_hand.winner,



            "pot":

                self.current_hand.pot,



            "completed":

                self.current_hand.completed

        }





    # ==========================================
    # Winner Information
    # ==========================================

    def winner(
        self
    ):
        """
        Return winner information.
        """



        if self.current_hand is None:

            return None





        return self.current_hand.winner





    # ==========================================
    # Replay Multiple Hands
    # ==========================================

    def replay_all(
        self
    ):
        """
        Return summaries of all loaded hands.
        """



        results = []





        for hand in self.hands:


            results.append({


                "hand_id":

                    hand.hand_id,



                "players":

                    hand.players,



                "winner":

                    hand.winner,



                "actions":

                    len(

                        hand.actions

                    )



            })





        return results





    # ==========================================
    # Select Hand By Index
    # ==========================================

    def select_hand(
        self,
        index
    ):
        """
        Select a loaded hand.
        """



        if index < 0 or index >= len(self.hands):

            raise IndexError(

                "Invalid hand index."

            )





        self.current_hand = self.hands[index]


        self.current_action = 0





        return self.current_hand





    # ==========================================
    # Reset Replay
    # ==========================================

    def reset(
        self
    ):
        """
        Reset replay state.
        """



        self.current_hand = None


        self.current_action = 0





    # ==========================================
    # Profile
    # ==========================================

    def profile(
        self
    ):
        """
        Replay system information.
        """



        return {


            "history_directory":

                self.history_directory,



            "loaded_hands":

                len(

                    self.hands

                ),



            "current_hand":

                self.current_hand.hand_id

                if self.current_hand

                else None

        }





    # ==========================================
    # Debug
    # ==========================================

    def __str__(
        self
    ):

        return (

            "Poker Replay System"

        )





    def __repr__(
        self
    ):

        return (

            f"ReplaySystem("

            f"hands={len(self.hands)})"

        )