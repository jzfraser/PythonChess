import sys, pygame, chess
import ui
from constants import SQUARE_LENGTH, WHITE


def main():
    pygame.init()

    width = height = SQUARE_LENGTH * 8
    size = (width, height)
    screen = pygame.display.set_mode(size)

    uiBoard = ui.Board()
    gameBoard = chess.Board()
    uiBoard.set_board_fen(gameBoard.board_fen())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(WHITE)
        uiBoard.draw(screen)

        pygame.display.update()
        if gameBoard.outcome() is not None:
            break

    print(gameBoard.outcome())


if __name__ == "__main__":
    main()
