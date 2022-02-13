import sys, pygame, chess
import ui
from constants import *


def main():
    pygame.init()

    width = height = SQUARE_LENGTH * 8
    size = (width, height)
    screen = pygame.display.set_mode(size)

    uiBoard = ui.Board()
    gameBoard = chess.Board()
    uiBoard.set_board_fen(gameBoard.board_fen())

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for square in uiBoard.squares:
                    if square.rect.collidepoint(event.pos):
                        if square.piece is not None:
                            if uiBoard.active_piece == square:
                                uiBoard.active_piece = None
                            else:
                                uiBoard.active_piece = square
                        else:
                            uiBoard.active_piece = None

        screen.fill(WHITE)
        uiBoard.draw(screen, list(gameBoard.legal_moves))

        pygame.display.update()
        if gameBoard.outcome() is not None:
            break
        clock.tick(FPS)

    print(gameBoard.outcome())


if __name__ == "__main__":
    main()
