import pygame
import sys
from card import Card
from pile import Pile

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
            Card(100, 100, CARD_WIDTH, CARD_HEIGHT, BLACK)
        ]

        self.pile = Pile(400, 100, CARD_WIDTH, CARD_HEIGHT, (255, 255, 0))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for card in self.cards:
                    if card.rect.collidepoint(event.pos):
                        card.start_dragging(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                for card in self.cards:
                    if card.dragging:
                        card.stop_dragging()
                        if self.pile.rect.collidepoint(event.pos) and not self.pile.card:
                            self.pile.place_card(card)

    def run(self):
        while True:
            self.handle_events()
            for card in self.cards:
                if card.dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    new_x = mouse_x - card.offset_x
                    new_y = mouse_y - card.offset_y
                    card.rect.topleft = (new_x, new_y)

            self.screen.fill(WHITE)
            self.pile.draw(self.screen)
            for card in self.cards:
                card.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)
