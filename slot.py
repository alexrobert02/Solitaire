import pygame

from card import Card


class Slot:
    """
    A slot object in a card game.
    Attributes
    ----------
    rect : pygame.Rect
        Pygame rect object representing the slot's position and size.
    color : tuple
        Tuple (R, G, B) representing the color of the slot in RGB format.
    pile : list
        List of cards in the slot.
    border_width : int
        Width of the slot's border.
    original_height : int
        Original height of the slot.
    """
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple, border_width: int):
        """
        Initialize a Slot object.
        :param x: X-coordinate of the slot's top-left corner.
        :param y: Y-coordinate of the slot's top-left corner.
        :param width: Width of the slot.
        :param height: Height of the slot.
        :param color: Tuple (R, G, B) representing the color of the slot in RGB format.
        :param border_width: Width of the slot's border.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.pile = []
        self.border_width = border_width
        self.original_height = height

    def draw(self, screen: pygame.Surface):
        """
        Draw the slot with its cards on the specified Pygame screen by placing the cards one below the other.
        :param screen: Pygame screen to draw the slot on.
        """
        pygame.draw.rect(screen, self.color, self.rect, self.border_width)
        for i, card in enumerate(self.pile):
            card.rect.topleft = (self.rect.left, self.rect.top + i * 20)

    def draw_stock(self, screen: pygame.Surface):
        """
        Draw the slot as a stock pile on the specified Pygame screen by placing the cards one on top of each other.
        :param screen: Pygame screen to draw the stock pile on.
        """
        pygame.draw.rect(screen, self.color, self.rect, self.border_width)
        for i, card in enumerate(self.pile):
            card.rect.topleft = (self.rect.left, self.rect.top)

    def place_card(self, card: Card):
        """
        Place a card on the slot.
        :param card: Card object to be placed on the slot.
        """
        self.pile.append(card)
        card.rect.topleft = self.rect.topleft
        card.set_original_position(self.rect.topleft)

    def remove_card(self, card: Card):
        """
        Remove a card from the slot.
        :param card: Card object to be removed from the slot.
        """
        self.pile.remove(card)

    def remove_pile(self, pile: list):
        """
        Remove a pile of cards from the slot.
        :param pile: List of Card objects representing the pile to be removed.
        """
        for i, card in enumerate(pile):
            card.stop_dragging()
            self.pile.remove(card)
            if len(self.pile) != 0 and self.rect.height < self.original_height:
                self.rect.height -= 20

    def place_pile(self, pile: list):
        """
        Place a pile of cards on the slot.
        :param pile: List of Card objects representing the pile to be placed.
        """
        for i, card in enumerate(pile):
            if card.dragging:
                card.stop_dragging()
            card.rect.topleft = (self.rect.left, self.rect.top)
            if len(self.pile) != 0:
                self.rect.height += 20
            self.pile.append(card)

    def get_draggable_pile(self, card: Card):
        """
        Get the subset of the pile that can be dragged starting from the specified card.
        :param card: Card object to determine the draggable pile.
        :return: List of Card objects representing the draggable pile.
        """
        if self.pile is not None:
            return self.pile[self.pile.index(card):]
        return card

    def start_dragging(self, pos: tuple, card: Card):
        """
        Start dragging the specified card and the associated draggable pile.
        :param pos: Tuple containing the starting position of the drag.
        :param card: Card object to be dragged.
        """
        draggable_pile = self.get_draggable_pile(card)
        for card in draggable_pile:
            new_x = pos[0]
            new_y = pos[1]
            new_pos = (new_x, new_y)
            card.start_dragging(new_pos)

    def get_top_card(self) -> Card:
        """
        Get the top card on the slot.
        :return: Card object representing the top card on the slot.
        """
        return self.pile[-1]

    def is_empty(self):
        """
        Check if the slot is empty.
        :return: true if the slot is empty, false otherwise.
        """
        return len(self.pile) == 0
