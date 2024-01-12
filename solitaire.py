from game import Game


def main():
    game = Game()
    game.create_slots()
    game.create_card_deck()
    game.deal_cards()
    game.run()


if __name__ == "__main__":
    main()
