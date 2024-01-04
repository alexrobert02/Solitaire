import pygame

class Pile:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.card = None

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.card:
            self.card.draw(screen)

    def place_card(self, card):
        print("card is placed on a pile")
        self.card = card
        self.card.rect.topleft = self.rect.topleft
        self.card.set_original_position(self.rect.topleft)
