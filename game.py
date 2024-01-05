import pygame
import sys

from rank import Rank
from card import Card
from slot import Slot
from suite import Suite

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 71, 96
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Solitaire")

        self.clock = pygame.time.Clock()

        self.pile = [
            Card(100, 100, CARD_WIDTH, CARD_HEIGHT, BLACK, Suite("Hearts", "RED"), Rank("Ace", 1)),
            Card(100, 100, CARD_WIDTH, CARD_HEIGHT, (255, 0, 255), Suite("Hearts", "RED"), Rank("Ace", 1)),
            Card(100, 100, CARD_WIDTH, CARD_HEIGHT, (255, 0, 255), Suite("Hearts", "RED"), Rank("Ace", 1)),
            Card(100, 100, CARD_WIDTH, CARD_HEIGHT, (255, 0, 255), Suite("Hearts", "RED"), Rank("Ace", 1))
        ]

        self.slots = [
            Slot(100, 100, CARD_WIDTH, CARD_HEIGHT, (0, 0, 0), 2),
            Slot(400, 100, CARD_WIDTH, CARD_HEIGHT, (0, 0, 0), 2),
            Slot(500, 100, CARD_WIDTH, CARD_HEIGHT, (0, 0, 0), 2)
        ]

        # self.pile = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for slot in self.slots:
                    for card in reversed(slot.pile):
                        if card.rect.collidepoint(event.pos):
                            slot.start_dragging(event.pos, card)
                            slot.rect.height = slot.original_height
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                for slot in self.slots:
                    for card in slot.pile:
                        if card.dragging:
                            card.stop_dragging()
                            for target_slot in self.slots:
                                if target_slot.rect.collidepoint(event.pos):
                                    draggable_pile = slot.get_draggable_pile(card)
                                    slot.remove_pile(draggable_pile)
                                    target_slot.place_pile(draggable_pile)

    def create_card_deck(self):
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

        # for suite in suites:
        #     for rank in ranks:
        #         self.pile.append(Card(100, 100, CARD_WIDTH, CARD_HEIGHT, BLACK, suite, rank))

        for i, card in enumerate(self.pile):
            self.slots[0].place_card(card)

    def run(self):
        while True:
            self.handle_events()
            self.screen.fill(WHITE)

            self.slots[0].draw_stock(self.screen)
            self.slots[1].draw(self.screen)
            self.slots[2].draw(self.screen)

            for card in self.pile:
                if card.dragging:
                    for slot in self.slots:
                        if card in slot.pile:
                            for i, drag_card in enumerate(slot.get_draggable_pile(card)):
                                mouse_x, mouse_y = pygame.mouse.get_pos()
                                new_x = mouse_x - card.offset_x
                                new_y = mouse_y - card.offset_y
                                card.rect.topleft = (new_x, new_y)
                                self.pile.remove(drag_card)
                                self.pile.append(drag_card)

            for card in self.pile:
                card.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)
