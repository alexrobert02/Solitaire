import pygame


class Card:
    def __init__(self, x, y, width, height, suite, rank):
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
        screen.blit(self.back_image, self.rect)

    def draw_front(self, screen):
        screen.blit(self.image, self.rect)

    def start_dragging(self, mouse_pos):
        self.dragging = True
        self.offset_x = mouse_pos[0] - self.rect.x
        self.offset_y = mouse_pos[1] - self.rect.y

    def stop_dragging(self):
        if self.dragging:
            self.dragging = False
            self.rect.topleft = self.original_position

    def set_original_position(self, new_position):
        self.original_position = new_position
