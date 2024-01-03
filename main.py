import pygame
import sys

from card import Card

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 71, 96
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def main():
    # screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Solitaire")

    clock = pygame.time.Clock()

    dragging = False
    offset_x, offset_y = 0, 0

    # card
    my_card = Card(100, 100, CARD_WIDTH, CARD_HEIGHT, BLACK)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if my_card.rect.collidepoint(event.pos):
                    dragging = True
                    offset_x = event.pos[0] - my_card.rect.x
                    offset_y = event.pos[1] - my_card.rect.y
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

        if dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            new_x = mouse_x - offset_x
            new_y = mouse_y - offset_y
            my_card.rect.topleft = (new_x, new_y)

        screen.fill(WHITE)
        my_card.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)


if __name__ == "__main__":
    main()
