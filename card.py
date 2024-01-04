import pygame


class Card:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.original_position = (x, y)
        self.color = color
        self.dragging = False
        self.offset_x, self.offset_y = 0, 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

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
