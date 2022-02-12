import pygame
from constants import *


piece_names = ["K", "Q", "B", "N", "R", "P"]
san_file_num_map = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7
}
san_rank_map = {
    '1': 7,
    '2': 6,
    '3': 5,
    '4': 4,
    '5': 3,
    '6': 2,
    '7': 1,
    '8': 0,
}


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
            if i <= 5:
                name = name.upper()
            elif i > 5:
                name = name.lower()
            self.pieces[name] = scaled

    def _draw_squares(self, surface: pygame.Surface):
        for square in self.squares:
            pygame.draw.rect(surface, square.color, square.rect)

    def _draw_pieces(self, surface):
        for rank in self.board:
            for piece in rank:
                if piece is not None:
                    surface.blit(self.pieces[piece.symbol], (piece.left, piece.top))

    def draw(self, surface: pygame.Surface):
        self._draw_squares(surface)
        self._draw_pieces(surface)

    def set_board_fen(self, fen: str):
        rank = 0
        file = 0
        for char in fen:
            if char == "/":
                rank = rank + 1
                file = 0
                continue
            elif char.isdigit():
                file = file + int(char)
                continue
            elif char.isalpha():
                left = file * 80
                top = rank * 80
                self.board[rank][file] = Piece(char, left, top)
            file = file + 1

    def move_piece_from_to(self, src: str, dest: str):
        if len(src) == 0 or len(dest) == 0:
            raise Exception("missing src or dest location")

        srcFile = san_file_num_map[src[0]]
        srcRank = int(src[1])
        destFile = san_file_num_map[dest[0]]
        destRank = int(dest[1])

        print(f"moving piece from {srcFile},{srcRank} to {destFile},{destRank}")

        # print(f"src: {self.board[srcRank][srcFile]}")
        # print(f"dest: {self.board[destRank][destFile]}")
        # print(self.board)

        self.board[destRank][destFile] = self.board[srcRank][srcFile]
        self.board[srcRank][srcFile] = None
