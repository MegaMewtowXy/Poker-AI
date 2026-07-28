from models.action import Action


class ConsoleUI:

    @staticmethod
    def show_player(player):

        print("\n--------------------------------")

        print(f"Player : {player.name}")

        print(f"Chips  : {player.chips}")

        print(f"Cards  : {player.show_hand()}")

        print("--------------------------------")

    @staticmethod
    def choose_action():

        print()

        print("1. Fold")

        print("2. Call")

        print("3. Check")

        print("4. Raise")

        print("5. All In")

        while True:

            choice = input("\nChoose action: ")

            match choice:

                case "1":
                    return Action.FOLD

                case "2":
                    return Action.CALL

                case "3":
                    return Action.CHECK

                case "4":
                    return Action.RAISE

                case "5":
                    return Action.ALL_IN

            print("Invalid choice.")