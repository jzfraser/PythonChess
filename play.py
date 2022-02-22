import sys, pygame
import game as g
from constants import *


def main():
    pygame.init()

    width = height = SQUARE_LENGTH * 8
    size = (width, height)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    game = g.Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.handle_leftclick_down(event)
            elif (
                event.type == pygame.MOUSEMOTION
                and game.uiBoard.active_square is not None
            ):
                game.handle_mouse_motion(event)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                game.handle_leftclick_up(event)
        screen.fill(WHITE)
        game.uiBoard.draw(screen, list(game.gameBoard.legal_moves))

        pygame.display.update()

        clock.tick(FPS)

        if game.gameBoard.outcome() is not None:
            outcome = game.gameBoard.outcome()
            if outcome.winner is not None:
                winner = COLOR_MAP[outcome.winner]
                print(f"{winner} won by {str(outcome.termination.name)}!")
            else:
                print(f"The match was a draw!")
            print()
            print(outcome.result())
            again = input("Play again? (y/n)")
            if again == "y":
                game.uiBoard._empty_board()
                game.uiBoard.set_board_fen(STARTING_FEN)
                game.gameBoard.reset()
                print("Board reset. Enjoy!")
                continue
            elif again == "n":
                sys.exit()
            else:
                print("Invalid input, exiting")
                sys.exit()


if __name__ == "__main__":
    main()
