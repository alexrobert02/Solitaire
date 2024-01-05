import pygame


class Slot:
    def __init__(self, x, y, width, height, color, border_width):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.cards = []
        self.border_width = border_width

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, self.border_width)
        for i, card in enumerate(self.cards):
            card.rect.topleft = (self.rect.left, self.rect.top + i * 20)

    def place_card(self, card):
        print("card is placed on a pile")
        self.cards.append(card)
        card.rect.topleft = self.rect.topleft
        card.set_original_position(self.rect.topleft)

    def remove_card(self):
        print("card is removed from a pile")
        if self.cards:
            self.cards.pop()

    def place(self, cards):

        for i, card in enumerate(cards):
            print(i)
            card.rect.topleft = (self.rect.left, self.rect.top)
            card.slot = self

            self.cards.append(card)

    def get_draggable_pile(self, card):
        if self.cards is not None:
            return self.cards[self.cards.index(card):]
        return card

    def start_dragging(self, pos, card):
        draggable_pile = self.get_draggable_pile(card)
        for card in draggable_pile:
            new_x = pos[0]
            new_y = pos[1]
            new_pos = (new_x, new_y)
            card.start_dragging(new_pos)
