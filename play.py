import sys, pygame
import chess
import board
from constants import SQUARE_LENGTH, WHITE


def main():
    pygame.init()

    width = height = SQUARE_LENGTH * 8
    size = (width, height)
    screen = pygame.display.set_mode(size)

    ui = board.Board()
    gameBoard = chess.Board()
    ui.set_board_from_fen(gameBoard.board_fen())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(WHITE)
        ui.draw(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
