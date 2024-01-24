import pygame

from suite import Suite
from rank import Rank


class Card:
    """
    A Card object in a card game.
    Attributes
    ----------
        rect : pygame.Rect
            Pygame.Rect object representing the card's position and size.
        original_position: tuple
            Tuple representing the original (x, y) position of the card.
        image: pygame.Surface
            Pygame.Surface object representing the image of the card's face.
        back_image: pygame.Surface
            Pygame.Surface object representing the image of the card's back.
        dragging: bool
            Flag indicating whether the card is being dragged
        offset_x: int
            X-offset of the mouse position from the card's rect when dragging.
        offset_y: int
            Y-offset of the mouse position from the card's rect when dragging.
        suite: Suite
            Suite of the card
        rank: Rank
            Rank of the card
    """
    def __init__(self, x: int, y: int, width: int, height: int, suite: Suite, rank: Rank):
        """
        Initialize a Card object.
        :param x: X-coordinate of the card's top-left corner.
        :param y: Y-coordinate of the card's top-left corner.
        :param width: Width of the card.
        :param height: Height of the card.
        :param suite: Suite of the card.
        :param rank: Rank of the card.
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

    def draw(self, screen: pygame.Surface):
        """
        Draw the card's back image on the specified Pygame screen.
        :param screen: Pygame screen to draw the card on.
        """
        screen.blit(self.back_image, self.rect)

    def draw_front(self, screen: pygame.Surface):
        """
        Draw the card's front image on the specified Pygame screen.
        :param screen: Pygame screen to draw the card on.
        """
        screen.blit(self.image, self.rect)

    def start_dragging(self, mouse_pos: tuple):
        """
        Start dragging the card.
        :param mouse_pos: Tuple containing the current mouse position.
        """
        self.dragging = True
        self.offset_x = mouse_pos[0] - self.rect.x
        self.offset_y = mouse_pos[1] - self.rect.y

    def stop_dragging(self):
        """
        Stop dragging the card and reset its position.
        """
        if self.dragging:
            self.dragging = False
            self.rect.topleft = self.original_position

    def set_original_position(self, new_position: tuple):
        """
        Set the original position of the card.
        :param new_position: Tuple containing the new position.
        """
        self.original_position = new_position

    def turn_face_up(self, screen: pygame.Surface):
        """
        Turn the card face up and draw its front image on the specified Pygame screen.
        :param screen: Pygame screen to draw the card on.
        """
        self.face_up = True
        self.draw_front(screen)

    def turn_face_down(self, screen: pygame.Surface):
        """
        Turn the card face down and draw its back image on the specified Pygame screen.
        :param screen: Pygame screen to draw the card on.
        """
        self.face_up = False
        self.draw(screen)
