import pygame


class Slot:
    def __init__(self, x, y, width, height, color, border_width):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.pile = []
        self.border_width = border_width
        self.original_height = height

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, self.border_width)
        for i, card in enumerate(self.pile):
            card.rect.topleft = (self.rect.left, self.rect.top + i * 20)

    def draw_stock(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, self.border_width)
        for i, card in enumerate(self.pile):
            card.rect.topleft = (self.rect.left, self.rect.top)

    def place_card(self, card):
        print("card is placed on a pile")
        self.pile.append(card)
        card.rect.topleft = self.rect.topleft
        card.set_original_position(self.rect.topleft)

    def remove_card(self, card):
        self.pile.remove(card)

    def remove_pile(self, pile):
        print("pile is removed")
        for i, card in enumerate(pile):
            card.stop_dragging()
            print("height removed")
            self.pile.remove(card)
            if len(self.pile) != 0 and self.rect.height < self.original_height:
                self.rect.height -= 20

    def place_pile(self, pile):
        print("pile is placed")
        for i, card in enumerate(pile):
            card.stop_dragging()
            card.rect.topleft = (self.rect.left, self.rect.top)
            card.slot = self
            print("height added")
            if len(self.pile) != 0:
                self.rect.height += 20
            self.pile.append(card)

    def get_draggable_pile(self, card):
        if self.pile is not None:
            return self.pile[self.pile.index(card):]
        return card

    def start_dragging(self, pos, card):
        draggable_pile = self.get_draggable_pile(card)
        for card in draggable_pile:
            new_x = pos[0]
            new_y = pos[1]
            new_pos = (new_x, new_y)
            card.start_dragging(new_pos)
