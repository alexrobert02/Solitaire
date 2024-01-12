import pygame


class Slot:
    def __init__(self, x, y, width, height, color, border_width):
        """
        Initialize a Slot object.

        Parameters:
        - x: X-coordinate of the slot's top-left corner.
        - y: Y-coordinate of the slot's top-left corner.
        - width: Width of the slot.
        - height: Height of the slot.
        - color: Tuple (R, G, B) representing the color of the slot in RGB format.
        - border_width: Width of the slot's border.

        Attributes:
        - rect : Pygame.Rect object representing the slot's position and size.
        - color : Tuple (R, G, B) representing the color of the slot in RGB format.
        - pile: List of the cards in the slot.
        - border_width: Width of the slot's border.
        - original_height: Original height of the slot.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.pile = []
        self.border_width = border_width
        self.original_height = height

    def draw(self, screen):
        """
        Draw the slot with its cards on the specified Pygame screen by placing the cards one below the other.

        Parameters:
        - screen: Pygame screen to draw the slot on.

        Returns:
            None
        """
        pygame.draw.rect(screen, self.color, self.rect, self.border_width)
        for i, card in enumerate(self.pile):
            card.rect.topleft = (self.rect.left, self.rect.top + i * 20)

    def draw_stock(self, screen):
        """
        Draw the slot as a stock pile on the specified Pygame screen by placing the cards one on top of each other.

        Parameters:
        - screen: Pygame screen to draw the stock pile on.

        Returns:
            None
        """
        pygame.draw.rect(screen, self.color, self.rect, self.border_width)
        for i, card in enumerate(self.pile):
            card.rect.topleft = (self.rect.left, self.rect.top)

    def place_card(self, card):
        """
        Place a card on the slot.

        Parameters:
        - card: Card object to be placed on the slot.

        Returns:
            None
        """
        self.pile.append(card)
        card.rect.topleft = self.rect.topleft
        card.set_original_position(self.rect.topleft)

    def remove_card(self, card):
        """
        Remove a card from the slot.

        Parameters:
        - card: Card object to be removed from the slot.

        Returns:
            None
        """
        self.pile.remove(card)

    def remove_pile(self, pile):
        """
        Remove a pile of cards from the slot.

        Parameters:
        - pile: List of Card objects representing the pile to be removed.

        Returns:
            None
        """
        for i, card in enumerate(pile):
            card.stop_dragging()
            self.pile.remove(card)
            if len(self.pile) != 0 and self.rect.height < self.original_height:
                self.rect.height -= 20

    def place_pile(self, pile):
        """
        Place a pile of cards on the slot.

        Parameters:
        - pile: List of Card objects representing the pile to be placed.

        Returns:
            None
        """
        for i, card in enumerate(pile):
            if card.dragging:
                card.stop_dragging()
            card.rect.topleft = (self.rect.left, self.rect.top)
            if len(self.pile) != 0:
                self.rect.height += 20
            self.pile.append(card)

    def get_draggable_pile(self, card):
        """
        Get the subset of the pile that can be dragged starting from the specified card.

        Parameters:
        - card: Card object to determine the draggable pile.

        Returns:
        - List of Card objects representing the draggable pile.
        """
        if self.pile is not None:
            return self.pile[self.pile.index(card):]
        return card

    def start_dragging(self, pos, card):
        """
        Start dragging the specified card and the associated draggable pile.

        Parameters:
        - pos: Tuple containing the starting position of the drag.
        - card: Card object to be dragged.

        Returns:
            None
        """
        draggable_pile = self.get_draggable_pile(card)
        for card in draggable_pile:
            new_x = pos[0]
            new_y = pos[1]
            new_pos = (new_x, new_y)
            card.start_dragging(new_pos)

    def get_top_card(self):
        """
        Get the top card on the slot.

        Returns:
        - Card object representing the top card on the slot.
        """
        return self.pile[-1]

    def is_empty(self):
        """
        Check if the slot is empty.

        Returns:
        - True if the slot is empty, False otherwise.
        """
        return len(self.pile) == 0
