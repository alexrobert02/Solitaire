import pygame


class Card:
    def __init__(self, x, y, width, height, suite, rank):
        """
        Initialize a Card object.

        Parameters:
        - x: X-coordinate of the card's top-left corner.
        - y: Y-coordinate of the card's top-left corner.
        - width: Width of the card.
        - height: Height of the card.
        - suite: Suite of the card.
        - rank: Rank of the card.

        Attributes:
        - rect : Pygame.Rect object representing the card's position and size.
        - original_position: Tuple representing the original (x, y) position of the card.
        - image: Image of the card's face.
        - back_image: Image of the card's back.
        - dragging: Flag indicating whether the card is being dragged
        - offset_x: X-offset of the mouse position from the card's rect when dragging.
        - offset_y: Y-offset of the mouse position from the card's rect when dragging.
        - suite: Suite of the card
        - rank: Rank of the card
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.original_position = (x, y)
        self.image = pygame.image.load(f'images/{rank.name.lower()}_of_{suite.name.lower()}.png')
        self.image = pygame.transform.smoothscale(self.image, (width, height))
        self.back_image = pygame.image.load("images/back_card.png")
        self.back_image = pygame.transform.smoothscale(self.back_image, (width, height))
        self.dragging = False
        self.offset_x, self.offset_y = 0, 0
        self.suite = suite
        self.rank = rank
        self.face_up = False

    def draw(self, screen):
        """
        Draw the card's back image on the specified Pygame screen.

        Parameters:
        - screen: Pygame screen to draw the card on.

        Returns:
            None
        """
        screen.blit(self.back_image, self.rect)

    def draw_front(self, screen):
        """
        Draw the card's front image on the specified Pygame screen.

        Parameters:
        - screen: Pygame screen to draw the card on.

        Returns:
            None
        """
        screen.blit(self.image, self.rect)

    def start_dragging(self, mouse_pos):
        """
        Start dragging the card.

        Parameters:
        - mouse_pos: Tuple containing the current mouse position.

        Returns:
            None
        """
        self.dragging = True
        self.offset_x = mouse_pos[0] - self.rect.x
        self.offset_y = mouse_pos[1] - self.rect.y

    def stop_dragging(self):
        """
        Stop dragging the card and reset its position.

        Returns:
            None
        """
        if self.dragging:
            self.dragging = False
            self.rect.topleft = self.original_position

    def set_original_position(self, new_position):
        """
        Set the original position of the card.

        Parameters:
        - new_position: Tuple containing the new position.

        Returns:
            None
        """
        self.original_position = new_position

    def turn_face_up(self, screen):
        """
        Turn the card face up and draw its front image on the specified Pygame screen.

        Parameters:
        - screen: Pygame screen to draw the card on.

        Returns:
            None
        """
        self.face_up = True
        self.draw_front(screen)

    def turn_face_down(self, screen):
        """
        Turn the card face down and draw its back image on the specified Pygame screen.

        Parameters:
        - screen: Pygame screen to draw the card on.

        Returns:
            None
        """
        self.face_up = False
        self.draw(screen)
