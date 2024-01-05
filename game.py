import pygame
import sys
from card import Card
from slot import Slot

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

        self.cards = [
            Card(100, 100, CARD_WIDTH, CARD_HEIGHT, BLACK),
            Card(100, 100, CARD_WIDTH, CARD_HEIGHT, (255, 0, 255))
        ]

        self.slots = [
            Slot(100, 100, CARD_WIDTH, CARD_HEIGHT, (0, 0, 0), 2),
            Slot(400, 100, CARD_WIDTH, CARD_HEIGHT, (0, 0, 0), 2),
            Slot(500, 100, CARD_WIDTH, CARD_HEIGHT, (0, 0, 0), 2)
        ]

        for i, card in enumerate(self.cards):
            self.slots[1].place_card(card)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for slot in reversed(self.slots):
                    for card in reversed(slot.cards):
                        if card.rect.collidepoint(event.pos):
                            print("da")
                            print(card.color)
                            slot.start_dragging(event.pos, card)
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                for slot in self.slots:
                    for card in slot.cards:
                        if card.dragging:
                            card.stop_dragging()
                            for target_slot in self.slots:
                                if target_slot.rect.collidepoint(event.pos):
                                    draggable_pile = slot.get_draggable_pile(card)
                                    for remove_card in draggable_pile:
                                        slot.remove_card()
                                        remove_card.stop_dragging()
                                    print("inainte de place")
                                    target_slot.place(draggable_pile)

    def run(self):
        while True:
            self.handle_events()

            self.screen.fill(WHITE)

            for slot in self.slots:
                slot.draw(self.screen)

            for card in self.cards:
                if card.dragging:
                    for slot in self.slots:
                        if card in slot.cards:
                            for i, drag_card in enumerate(slot.get_draggable_pile(card)):
                                print(len(slot.get_draggable_pile(card)))
                                mouse_x, mouse_y = pygame.mouse.get_pos()
                                new_x = mouse_x - card.offset_x
                                new_y = mouse_y - card.offset_y
                                card.rect.topleft = (new_x, new_y)
                                self.cards.remove(drag_card)
                                self.cards.append(drag_card)

            for card in self.cards:
                card.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)
