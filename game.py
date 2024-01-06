import random

import pygame
import sys

from rank import Rank
from card import Card
from slot import Slot
from suite import Suite

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
CARD_WIDTH, CARD_HEIGHT = 85, 115
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Solitaire")

        self.clock = pygame.time.Clock()

        self.pile = [
            Card(200, 200, CARD_WIDTH, CARD_HEIGHT, Suite("Hearts", "RED"), Rank("Ace", 1)),
            Card(200, 200, CARD_WIDTH, CARD_HEIGHT, Suite("Hearts", "RED"), Rank("2", 2)),
            Card(200, 200, CARD_WIDTH, CARD_HEIGHT, Suite("Hearts", "RED"), Rank("3", 3)),
            Card(200, 200, CARD_WIDTH, CARD_HEIGHT, Suite("Hearts", "RED"), Rank("4", 4))
        ]

        # self.slots = [
        #     Slot(200, 200, CARD_WIDTH, CARD_HEIGHT, (0, 0, 0), 2),
        #     Slot(300, 100, CARD_WIDTH, CARD_HEIGHT, (0, 0, 0), 2),
        #     Slot(400, 100, CARD_WIDTH, CARD_HEIGHT, (0, 0, 0), 2)
        # ]
        self.stock = None
        self.waste = None
        self.foundations = []
        self.tableau = []

        self.slots = []

    def create_slots(self):
        self.stock = Slot(100, 100, CARD_WIDTH, CARD_HEIGHT, (0, 0, 0), 2)
        self.waste = Slot(225, 100, CARD_WIDTH, CARD_HEIGHT, (0, 0, 0), 2)

        x = 475
        for i in range(4):
            self.foundations.append(Slot(x, 100, CARD_WIDTH, CARD_HEIGHT, (0, 0, 0), 2))
            x += 125

        x = 100
        for i in range(7):
            self.tableau.append(Slot(x, 300, CARD_WIDTH, CARD_HEIGHT, (0, 0, 0), 2))
            x += 125

        self.slots.append(self.stock)
        self.slots.append(self.waste)

        for slot in self.foundations:
            self.slots.append(slot)

        for slot in self.tableau:
            self.slots.append(slot)

        # self.slots.append(self.tableau)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for slot in self.slots[1:]:
                    for card in reversed(slot.pile):
                        if card.rect.collidepoint(event.pos):
                            slot.start_dragging(event.pos, card)
                            slot.rect.height = slot.original_height
                            break
                if self.slots[0].rect.collidepoint(event.pos):
                    if self.slots[0].is_empty():
                        print("nu")
                        for card in reversed(self.slots[1].pile):
                            card.face_up = False
                            card.draw(self.screen)
                            self.slots[1].remove_card(card)
                            self.slots[0].place_card(card)
                    else:
                        print("da")
                        self.slots[1].place_card(self.slots[0].pile.pop())
                        self.slots[1].get_top_card().face_up = True
                        self.slots[1].get_top_card().draw_front(self.screen)
            elif event.type == pygame.MOUSEBUTTONUP:
                for slot in self.slots:
                    break_flag = False
                    for card in slot.pile:
                        if card.dragging:
                            card.stop_dragging()
                            for target_slot in self.slots[6:]:
                                if target_slot.rect.collidepoint(event.pos):
                                    draggable_pile = slot.get_draggable_pile(card)
                                    slot.remove_pile(draggable_pile)
                                    if slot.is_empty() is False:
                                        slot.get_top_card().face_up = True
                                        slot.get_top_card().draw_front(self.screen)
                                    target_slot.place_pile(draggable_pile)

                            for target_slot in self.slots[2:6]:
                                if target_slot.rect.collidepoint(event.pos):
                                    if len(slot.get_draggable_pile(card)) > 1:
                                        for pile_card in slot.get_draggable_pile(card):
                                            pile_card.stop_dragging()
                                        break_flag = True
                                        print("break")
                                        break
                                    slot.remove_card(card)
                                    if slot.is_empty() is False:
                                        slot.get_top_card().face_up = True
                                        slot.get_top_card().draw_front(self.screen)
                                    print("test")
                                    target_slot.place_card(card)
                    if break_flag:
                        break


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

        for suite in suites:
            for rank in ranks:
                self.pile.append(Card(100, 100, CARD_WIDTH, CARD_HEIGHT, suite, rank))

    def deal_cards(self):
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
            slot.get_top_card().face_up = True
            slot.get_top_card().draw_front(self.screen)

    def run(self):
        while True:
            self.handle_events()
            self.screen.fill(WHITE)

            self.slots[0].draw_stock(self.screen)
            self.slots[1].draw_stock(self.screen)

            for slot in self.slots[2:6]:
                slot.draw_stock(self.screen)

            for slot in self.slots[6:]:
                slot.draw(self.screen)

            for slot in self.slots:
                for card in slot.pile:
                    if card.dragging:
                        for i, drag_card in enumerate(slot.get_draggable_pile(card)):
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            new_x = mouse_x - card.offset_x
                            new_y = mouse_y - card.offset_y
                            card.rect.topleft = (new_x, new_y)
                            # slot.pile.remove(drag_card)
                            # slot.pile.append(drag_card)

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

            pygame.display.flip()
            self.clock.tick(FPS)
