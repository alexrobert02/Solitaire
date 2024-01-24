import random
import pygame
import sys

from rank import Rank
from card import Card
from slot import Slot
from suite import Suite

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
CARD_WIDTH, CARD_HEIGHT = 85, 115
BORDER_WIDTH = 2
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def check_foundations_rules(card: Card, slot: Slot):
    """
    Check if the provided card can be placed on the foundations slot based on Solitaire rules.
    :param card: Card object to be checked.
    :param slot: Slot object representing the foundations slot.
    :return: true if the card can be placed on the slot, false otherwise.
    """
    if slot.is_empty():
        return card.rank.name == "Ace"
    top_card = slot.get_top_card()
    return card.suite.name == top_card.suite.name and card.rank.value - top_card.rank.value == 1


def check_tableau_rules(card: Card, slot: Slot):
    """
    Check if the provided card can be placed on the tableau slot based on Solitaire rules.
    :param card: Card object to be checked.
    :param slot: Slot object representing the tableau slot.
    :return: true if the card can be placed on the slot, false otherwise.
    """
    if slot.is_empty():
        return card.rank.name == "King"
    top_card = slot.get_top_card()
    return (
        card.suite.color != top_card.suite.color
        and top_card.rank.value - card.rank.value == 1
        and top_card.face_up
    )


class Game:
    """
    Game object for a Solitaire game.
    Attributes
    ----------
    screen : pygame.Surface
        Pygame surface object representing the screen for rendering.
    clock : pygame.time.Clock
        Pygame clock object for controlling the frame rate.
    pile : list of Card
        List to store the initial card deck.
    stock : Slot
        Slot object representing the stock pile.
    waste : Slot
        Slot object representing the waste pile.
    foundations : list of Slot
        List of Slot objects representing the foundation piles.
    tableau : list of Slot
        List of Slot objects representing the tableau piles.
    slots : list of Slot
        Combined list of all game slots.
    new_game_rect : pygame.Rect
        Pygame rect object representing the new game button's position and size.
    victory_rect : pygame.Rect
        Pygame rect object representing the victory screen's position and size.
    """
    def __init__(self):
        """
        Initialize a Game object representing a Solitaire game.
        """
        pygame.init()
        pygame.display.set_caption("Solitaire")

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.pile = []
        self.stock = None
        self.waste = None
        self.foundations = []
        self.tableau = []
        self.slots = []

        self.new_game_rect = pygame.Rect(400, 600, 200, 40)
        self.victory_rect = pygame.Rect(350, 250, 300, 80)

    def create_slots(self):
        """
        Create and initialize the game slots including stock, waste, foundations, tableau, and others.

        This method creates instances of the Slot class for various game components such as stock, waste, foundations,
        and tableau piles. The slots are positioned on the screen, and the list 'slots' is populated accordingly.

        The stock and waste slots are positioned at (100, 100) and (225, 100) respectively.
        The foundation slots are positioned starting from (475, 100) with a gap of 125 units.
        The tableau slots are positioned starting from (100, 300) with a gap of 125 units.

        All slots have dimensions defined by CARD_WIDTH and CARD_HEIGHT,
        color defined by WHITE, and border width defined by BORDER_WIDTH.
        """
        self.stock = Slot(100, 100, CARD_WIDTH, CARD_HEIGHT, WHITE, BORDER_WIDTH)
        self.waste = Slot(225, 100, CARD_WIDTH, CARD_HEIGHT, WHITE, BORDER_WIDTH)

        x = 475
        for i in range(4):
            self.foundations.append(Slot(x, 100, CARD_WIDTH, CARD_HEIGHT, WHITE, BORDER_WIDTH))
            x += 125

        x = 100
        for i in range(7):
            self.tableau.append(Slot(x, 300, CARD_WIDTH, CARD_HEIGHT, WHITE, BORDER_WIDTH))
            x += 125

        self.slots.append(self.stock)
        self.slots.append(self.waste)

        for slot in self.foundations:
            self.slots.append(slot)

        for slot in self.tableau:
            self.slots.append(slot)

    def handle_events(self):
        """
        Handle all the events in the game.

        It loops through all the pygame events and performs actions based on the type of the event.

        The method handles three types of events: pygame.QUIT, pygame.MOUSEBUTTONDOWN, and pygame.MOUSEBUTTONUP.
        For pygame.MOUSEBUTTONDOWN, it checks if the mouse position collides with any card or button and performs the
        corresponding action. For pygame.MOUSEBUTTONUP, it stops dragging the card and checks if the card can be placed
        in the target slot.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for slot in self.slots[1:]:
                    for card in reversed(slot.pile):
                        if card.face_up is False:
                            break
                        if card.rect.collidepoint(event.pos):
                            slot.start_dragging(event.pos, card)
                            slot.rect.height = slot.original_height
                            break
                if self.slots[0].rect.collidepoint(event.pos):
                    # If the stock pile is empty, put the waste pile onto the stock pile
                    if self.slots[0].is_empty():
                        for card in reversed(self.slots[1].pile):
                            card.turn_face_down(self.screen)
                            self.slots[1].remove_card(card)
                            self.slots[0].place_card(card)
                    else:
                        self.slots[1].place_card(self.slots[0].pile.pop())
                        self.slots[1].get_top_card().turn_face_up(self.screen)
                if self.new_game_rect.collidepoint(event.pos):
                    self.restart_game()
            elif event.type == pygame.MOUSEBUTTONUP:
                for slot in self.slots:
                    for card in slot.pile:
                        if card.dragging:
                            card.stop_dragging()
                            # Tableau slots
                            for target_slot in self.slots[6:]:
                                if target_slot.rect.collidepoint(event.pos) and check_tableau_rules(card, target_slot):
                                    draggable_pile = slot.get_draggable_pile(card)
                                    slot.remove_pile(draggable_pile)
                                    if slot.is_empty() is False:
                                        slot.get_top_card().turn_face_up(self.screen)
                                    target_slot.place_pile(draggable_pile)
                            # Foundation slots
                            for target_slot in self.slots[2:6]:
                                if (
                                    target_slot.rect.collidepoint(event.pos)
                                    and check_foundations_rules(card, target_slot)
                                ):
                                    if len(slot.get_draggable_pile(card)) > 1:
                                        # Place the entire pile to the target slot
                                        for pile_card in slot.get_draggable_pile(card):
                                            pile_card.stop_dragging()
                                        break
                                    slot.remove_card(card)
                                    if slot.is_empty() is False:
                                        slot.get_top_card().turn_face_up(self.screen)
                                    target_slot.place_card(card)

    def create_card_deck(self):
        """
        Create and initialize a deck of cards.

        This method creates a standard deck of 52 playing cards. The deck consists of four suites:
        hearts, diamonds, clubs, and spades. Each suite has 13 ranks: Ace, 2-10, Jack, Queen, and King.

        Each card is created with a position of (100, 100), dimensions defined by CARD_WIDTH and CARD_HEIGHT,
        and the corresponding suite and rank.
        """
        suites = [
            Suite("hearts", "RED"),
            Suite("diamonds", "RED"),
            Suite("clubs", "BLACK"),
            Suite("spades", "BLACK"),
        ]
        ranks = [
            Rank("Ace", 1),
            Rank("2", 2),
            Rank("3", 3),
            Rank("4", 4),
            Rank("5", 5),
            Rank("6", 6),
            Rank("7", 7),
            Rank("8", 8),
            Rank("9", 9),
            Rank("10", 10),
            Rank("Jack", 11),
            Rank("Queen", 12),
            Rank("King", 13),
        ]

        for suite in suites:
            for rank in ranks:
                self.pile.append(Card(100, 100, CARD_WIDTH, CARD_HEIGHT, suite, rank))

    def deal_cards(self):
        """
        Shuffle and deal the cards to the slots.

        This method shuffles the pile of cards and deals them to the slots.
        The cards are dealt in a specific order to the slots starting from the seventh slot (the first tableau slot).
        Each tableau slot receives one card more than the previous slot in each round until all slots have cards.

        The remaining cards are placed in the stock. The top card of each tableau slot is then turned face up.
        """
        random.shuffle(self.pile)

        first_slot = 0
        remaining_cards = self.pile
        card_list = []

        while first_slot < len(self.slots[6:]):
            for slot in self.slots[6:][first_slot:]:
                top_card = remaining_cards[0]
                top_card.rect.topleft = slot.rect.topleft
                card_list.append(top_card)
                slot.place_pile(card_list)
                card_list.remove(top_card)
                remaining_cards.remove(top_card)
            first_slot += 1

        for card in remaining_cards:
            self.stock.place_card(card)

        for slot in self.slots[6:]:
            slot.get_top_card().turn_face_up(self.screen)

    def run(self):
        """
        Run the main game loop.
        """
        while True:
            self.draw_game()
            self.handle_events()

            if self.check_win():
                self.draw_win_screen()

            pygame.display.flip()
            self.clock.tick(FPS)

    def check_win(self):
        """
        Check if the player has won the game by completing the foundations.
        :return: true if the player has won by completing the foundations, false otherwise.
        """
        cards_num = 0
        for slot in self.slots[2:6]:
            cards_num += len(slot.pile)
        if cards_num == 52:
            return True
        return False

    def restart_game(self):
        """
        Restart the game by resetting slots, creating a new card deck, and dealing cards.

        This method resets the game state, creating a new card deck, shuffling, and dealing cards to the tableau slots.
        """
        self.pile = []
        self.stock = None
        self.waste = None
        self.foundations = []
        self.tableau = []
        self.slots = []

        self.create_slots()
        self.create_card_deck()
        self.deal_cards()

    def draw_win_screen(self):
        """
        Draw the victory screen and restart the game.

        This method draws a victory screen with a black rectangle filled with white border.
        It then renders the text 'VICTORY' in white and blits it to the screen at the center of the victory rectangle.
        The screen is updated and a delay of 3000 milliseconds is introduced before the game is restarted.
        """
        pygame.draw.rect(self.screen, BLACK, self.victory_rect)
        pygame.draw.rect(self.screen, WHITE, self.victory_rect, BORDER_WIDTH)
        font = pygame.font.SysFont('mspgothic', 36)
        text = font.render('VICTORY', False, WHITE)
        text_rect = text.get_rect(center=self.victory_rect.center)

        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)  # in milliseconds

        self.restart_game()

    def draw_game(self):
        """
        Draw the game state on the screen.

        This method fills the screen with black color and then draws the stock and other slots.
        It also handles the dragging of cards by updating their positions based on the mouse position.
        It then draws the cards in the slots, with special handling for cards that are being dragged.
        Finally, it draws the 'New Game' button on the screen.
        """
        self.screen.fill(BLACK)

        self.slots[0].draw_stock(self.screen)
        self.slots[1].draw_stock(self.screen)

        for slot in self.slots[2:6]:
            slot.draw_stock(self.screen)

        for slot in self.slots[6:]:
            slot.draw(self.screen)

        for slot in self.slots:
            for card in slot.pile:
                if card.dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    new_x = mouse_x - card.offset_x
                    new_y = mouse_y - card.offset_y
                    card.rect.topleft = (new_x, new_y)

        for slot in self.slots:
            for card in slot.pile:
                if card.dragging is not True:
                    if card.face_up is True:
                        card.draw_front(self.screen)
                    else:
                        card.draw(self.screen)

        for slot in self.slots:
            for card in slot.pile:
                if card.dragging is True:
                    if card.face_up is True:
                        card.draw_front(self.screen)
                    else:
                        card.draw(self.screen)

        pygame.draw.rect(self.screen, WHITE, self.new_game_rect, BORDER_WIDTH)
        font = pygame.font.SysFont('mspgothic', 20)
        text = font.render('NEW GAME', False, WHITE)
        text_rect = text.get_rect(center=self.new_game_rect.center)
        self.screen.blit(text, text_rect)
