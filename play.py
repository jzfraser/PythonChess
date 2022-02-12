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
    uiBoard.set_board_from_fen(gameBoard.board_fen())

    first_move = True

    while gameBoard.outcome() is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if first_move:
            gameBoard.push_san("e4")
            uiBoard.set_board_from_fen(gameBoard.board_fen())
            first_move = False

        screen.fill(WHITE)
        uiBoard.draw(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
