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

    starting_fen = gameBoard.board_fen()
    uiBoard.set_board_fen(starting_fen)

    clock = pygame.time.Clock()

    outcome = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for square in uiBoard.squares:
                    if square.rect.collidepoint(event.pos):
                        if uiBoard.active_square is not None:
                            if square is uiBoard.active_square:
                                color = (
                                    square.piece.symbol.isupper()
                                )  # true if white, false if black
                                if color != gameBoard.turn:
                                    break
                                uiBoard.active_square.piece.dragging = True
                                mouse_left, mouse_top = event.pos
                                uiBoard.active_square.set_piece_offsets(
                                    mouse_left, mouse_top
                                )
                                continue
                            move = chess.Move.from_uci(
                                uiBoard.active_square.name + square.name
                            )
                            if move in gameBoard.legal_moves:
                                uiBoard.move_piece_from_to(
                                    uiBoard.active_square.name, square.name
                                )
                                gameBoard.push(move)
                                square.reset_piece_pos()
                                uiBoard.active_square = None
                        if square.piece is not None:
                            if uiBoard.active_square == square:
                                uiBoard.active_square = None
                            else:
                                color = (
                                    square.piece.symbol.isupper()
                                )  # true if white, false if black
                                if color != gameBoard.turn:
                                    break
                                uiBoard.active_square = square
                                uiBoard.active_square.piece.dragging = True
                                mouse_left, mouse_top = event.pos
                                uiBoard.active_square.set_piece_offsets(
                                    mouse_left, mouse_top
                                )
                        else:
                            uiBoard.active_square = None
            elif event.type == pygame.MOUSEMOTION and uiBoard.active_square is not None:
                if uiBoard.active_square.piece.dragging:
                    piece = uiBoard.active_square.piece
                    mouse_left, mouse_top = event.pos
                    piece.left = piece.offset_left + mouse_left
                    piece.top = piece.offset_top + mouse_top
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if uiBoard.active_square is not None:
                    for square in uiBoard.squares:
                        if square.rect.collidepoint(event.pos):
                            if uiBoard.active_square.name == square.name:
                                uiBoard.active_square.reset_piece_pos()
                                break
                            move = chess.Move.from_uci(
                                uiBoard.active_square.name + square.name
                            )
                            if move in gameBoard.legal_moves:
                                uiBoard.active_square.reset_piece_pos()
                                uiBoard.move_piece_from_to(
                                    uiBoard.active_square.name, square.name
                                )
                                gameBoard.push(move)
                                square.reset_piece_pos()
                                uiBoard.active_square = None
                                break
                            else:
                                uiBoard.active_square.reset_piece_pos()

        screen.fill(WHITE)
        uiBoard.draw(screen, list(gameBoard.legal_moves))

        pygame.display.update()

        clock.tick(FPS)

        if gameBoard.outcome() is not None:
            outcome = gameBoard.outcome()
            if outcome.winner is not None:
                winner = COLOR_MAP[outcome.winner]
                print(f"{winner} won by {str(outcome.termination.name)}!")
            else:
                print(f"The match was a draw!")
            print()
            print(outcome.result())
            again = input("Play again? (y/n)")
            if again == "y":
                uiBoard._empty_board()
                uiBoard.set_board_fen(starting_fen)
                gameBoard.reset()
                print("Board reset. Enjoy!")
                continue
            elif again == "n":
                sys.exit()
            else:
                print("Invalid input, exiting")
                sys.exit()


if __name__ == "__main__":
    main()
