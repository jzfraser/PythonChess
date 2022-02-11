import sys, pygame
import board
from constants import SQUARE_LENGTH, WHITE


def main():
    pygame.init()

    width = height = SQUARE_LENGTH * 8
    size = (width, height)
    screen = pygame.display.set_mode(size)

    gameBoard = board.Board()
    gameBoard.init_board()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(WHITE)
        gameBoard.draw(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
