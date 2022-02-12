import pygame
from constants import SQUARE_LENGTH, WHITE, BLACK


piece_names = ["K", "Q", "B", "N", "R", "P"]


class Square:
    def __init__(self, left, top, length, color):
        self.left = left
        self.top = top
        self.length = length
        self.rect = pygame.Rect(left, top, self.length, self.length)

        self.color = color


class Piece:
    def __init__(self, symbol, left, top):
        self.symbol = symbol
        self.left = left
        self.top = top


class Board:
    def __init__(self):
        self.squares = []
        self.pieces = {}
        self.board = [[None for j in range(8)] for i in range(8)]
        self.pieces_png = pygame.image.load("./images/Pieces.png").convert_alpha()
        self._create_squares()
        self._load_piece_images()

    def _empty_board(self):
        self.board = [[None for j in range(8)] for i in range(8)]

    def _create_squares(self):
        for rank in range(8):
            for file in range(8):
                left = file * SQUARE_LENGTH
                top = rank * SQUARE_LENGTH

                color = BLACK
                if (
                    ((file % 2 != 0) and (rank % 2 != 0))
                    or (file % 2 == 0)
                    and (rank % 2 == 0)
                ):
                    color = WHITE
                s = Square(left, top, SQUARE_LENGTH, color)
                self.squares.append(s)

    # values used in this method seem random but are based on properties of the png containing the piece images
    def _load_piece_images(self):
        for i in range(12):
            left = (i % 6) * 333
            top = 0
            if i > 5:
                top = 334

            cropped = self.pieces_png.subsurface((left, top, 334, 334))
            scaled = pygame.transform.smoothscale(cropped, (80, 80))

            name = piece_names[i % 6]
            if i > 5:
                name = name.lower()
            self.pieces[name] = scaled

    def _draw_squares(self, surface):
        for square in self.squares:
            pygame.draw.rect(surface, square.color, square.rect)

    def _draw_pieces(self, surface):
        for rank in self.board:
            for piece in rank:
                if piece is not None:
                    surface.blit(self.pieces[piece.symbol], (piece.left, piece.top))

    def set_board_from_fen(self, fen):
        self._empty_board()
        rank = 8
        file = 1
        for char in fen:
            if char == "/":
                rank = rank - 1
                file = 1
                continue
            elif char.isdigit():
                file = file + int(char)
                continue
            elif char.isalpha():
                left = (file - 1) * 80
                top = (rank - 1) * 80
                self.board[rank - 1][file - 1] = Piece(char, left, top)
            file = file + 1

    def draw(self, surface):
        self._draw_squares(surface)
        self._draw_pieces(surface)

    def init_board(self):
        for file in range(8):
            left = file * 80
            wTop = 80 * 6
            bTop = 80
            self.board[1][file] = Piece("P", left, wTop)
            self.board[6][file] = Piece("p", left, bTop)

        wTop = 80 * 7
        bTop = 0
        self.board[0][0] = Piece("R", 0, wTop)
        self.board[0][1] = Piece("N", 80, wTop)
        self.board[0][2] = Piece("B", 160, wTop)
        self.board[0][3] = Piece("Q", 240, wTop)
        self.board[0][4] = Piece("K", 320, wTop)
        self.board[0][5] = Piece("B", 400, wTop)
        self.board[0][6] = Piece("N", 480, wTop)
        self.board[0][7] = Piece("R", 560, wTop)
        self.board[7][0] = Piece("r", 0, bTop)
        self.board[7][1] = Piece("n", 80, bTop)
        self.board[7][2] = Piece("b", 160, bTop)
        self.board[7][3] = Piece("q", 240, bTop)
        self.board[7][4] = Piece("k", 320, bTop)
        self.board[7][5] = Piece("b", 400, bTop)
        self.board[7][6] = Piece("n", 480, bTop)
        self.board[7][7] = Piece("r", 560, bTop)
