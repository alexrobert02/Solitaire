from game import Game


def main():
    """
    Main function to run the game.

    This function creates an instance of the Game class, initializes the game slots and card deck,
    deals the cards, and then runs the game.

    Returns:
        None
    """
    game = Game()
    game.create_slots()
    game.create_card_deck()
    game.deal_cards()
    game.run()


if __name__ == "__main__":
    main()
