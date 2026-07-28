from models.action import Action


class ConsoleUI:
    """
    Console interface for human players.
    """

    @staticmethod
    def show_player(player):

        print("\n--------------------------------")

        print(f"Player : {player.name}")

        print(f"Cards  : {player.show_hand()}")

        print(f"Chips  : {player.chips}")

        print("--------------------------------")

    @staticmethod
    def choose_action():

        print()

        print("1. Fold")

        print("2. Check")

        print("3. Call")

        print("4. Raise")

        print("5. All In")

        while True:

            choice = input("\nChoose Action : ")

            match choice:

                case "1":
                    return Action.FOLD

                case "2":
                    return Action.CHECK

                case "3":
                    return Action.CALL

                case "4":
                    return Action.RAISE

                case "5":
                    return Action.ALL_IN

            print("Invalid choice.")