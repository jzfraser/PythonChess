import chess
import ui
from constants import *


class Game:
    def __init__(self):
        self.gameBoard: chess.Board = chess.Board()
        self.uiBoard: ui.Board = ui.Board()
        self.uiBoard.set_board_fen(STARTING_FEN)
        self.outcome = None
        self.odd_click = True

    def handle_leftclick_down(self, event):
        # loop over all squares
        for square in self.uiBoard.squares:
            # if mouse click position is within current square
            if square.rect.collidepoint(event.pos):
                # if active square already selected
                if self.uiBoard.active_square is not None:
                    # if current square is selected active square begin dragging
                    if square is self.uiBoard.active_square:
                        self.drag_piece_on_square(square, event.pos)
                        break
                    # else current square is different from active square
                    else:
                        # if move is legal then make move and reset active square
                        if not self.make_move(square):
                            if square.piece is not None:
                                self.drag_piece_on_square(square, event.pos)
                            else:
                                self.uiBoard.active_square = None
                            self.odd_click = not self.odd_click
                            break
                # else no active square
                else:
                    # if square has a piece start dragging it
                    if square.piece is not None:
                        # if game.uiBoard.active_square == square:
                        #     game.uiBoard.active_square = None
                        self.drag_piece_on_square(square, event.pos)
                    else:
                        if self.odd_click:
                            self.uiBoard.active_square = None
                            self.odd_click = False
                        else:
                            self.odd_click = True

    def handle_mouse_motion(self, event):
        if self.uiBoard.active_square.piece.dragging:
            piece = self.uiBoard.active_square.piece
            mouse_left, mouse_top = event.pos
            piece.left = piece.offset_left + mouse_left
            piece.top = piece.offset_top + mouse_top

    def handle_leftclick_up(self, event):
        # if an active square is selected
        if (
            self.uiBoard.active_square is not None
            and self.uiBoard.active_square.piece.dragging
        ):
            # check all squares
            for square in self.uiBoard.squares:
                # if mouse released over current square
                if square.rect.collidepoint(event.pos):
                    # if current square and active square are the same then drop the piece
                    if self.uiBoard.active_square == square:
                        self.uiBoard.active_square.reset_piece_pos()
                        if self.odd_click:
                            self.uiBoard.active_square = None
                            self.odd_click = False
                        else:
                            self.odd_click = True
                        break
                    # else if move from active to current fails
                    elif not self.make_move(square):
                        self.odd_click = not self.odd_click
                        break

    def make_move(self, dest_square) -> bool:
        # still need to handle en passant, and pawn promotion
        move = chess.Move.from_uci(self.uiBoard.active_square.name + dest_square.name)
        if move in self.gameBoard.legal_moves:
            src_square = self.uiBoard.active_square
            if self.gameBoard.is_en_passant(move):
                self.uiBoard.en_passant(src_square.name, dest_square.name)
            elif self.gameBoard.is_castling(move):
                if self.gameBoard.is_queenside_castling(move):
                    self.uiBoard.queenside_castle(src_square.name, dest_square.name)
                else:
                    self.uiBoard.kingside_castle(src_square.name, dest_square.name)
            else:
                self.uiBoard.move_from_to(src_square.name, dest_square.name)
            self.gameBoard.push(move)
            dest_square.reset_piece_pos()
            self.uiBoard.active_square = None
            # print(self.gameBoard)
            # print()
            return True
        else:
            # print(self.gameBoard)
            # print()
            self.uiBoard.active_square.reset_piece_pos()
            return False

    def drag_piece_on_square(self, square, pos):
        color = square.piece.symbol.isupper()  # true if white, false if black
        if color != self.gameBoard.turn:
            return
        self.uiBoard.active_square = square
        self.uiBoard.active_square.piece.dragging = True
        mouse_left, mouse_top = pos
        self.uiBoard.active_square.set_piece_offsets(mouse_left, mouse_top)
