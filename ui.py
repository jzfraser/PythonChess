import pygame
from constants import *


class Square:
    def __init__(self, left, top, length, color, index):
        self.left = left
        self.top = top
        self.length = length
        self.rect = pygame.Rect(left, top, self.length, self.length)
        self.color = color
        self.piece = None
        self.index = index

    def __str__(self):
        square = ""
        if self.piece is not None:
            square += (
                self.piece.symbol
                + " "
                + str(self.left)
                + " "
                + str(self.top)
                + " "
                + str(self.index)
                + " "
                + str(self.piece.active)
                + " "
                + str(self.rect.left)
                + " "
                + str(self.rect.top)
            )
        else:
            square += (
                "empty"
                + " "
                + str(self.left)
                + " "
                + str(self.top)
                + " "
                + str(self.index)
                + " "
                + str(self.rect.left)
                + " "
                + str(self.rect.top)
            )
        return square


class Piece:
    def __init__(self, symbol, left, top):
        self.symbol = symbol

    def __str__(self):
        return self.symbol


class Board:
    def __init__(self):
        self.squares = []
        self.pieces = {}
        self.pieces_png = pygame.image.load("./images/Pieces.png").convert_alpha()
        self._create_squares()
        self._load_piece_images()
        self.active_piece = None

    def __str__(self):
        boardString = ""
        numEmpty = 0
        for rank in self.board:
            for piece in rank:
                if piece is None:
                    numEmpty = numEmpty + 1
                    continue
                boardString = boardString + str(piece)
            if numEmpty > 0:
                boardString = boardString + str(numEmpty)
            boardString = boardString + "/"
            numEmpty = 0
        return boardString

    def _square_to_coords(self, square: int):
        left = (square & 7) * 80
        top = (square >> 3) * 80
        return (left, top)

    def _parse_square_name(self, square: str):
        return SQUARE_NAME_NUM_MAP(square)

    def _get_square_center(self, square: Square) -> tuple:
        return (square.left + 40, square.top + 40)

    def _empty_board(self):
        for square in self.squares:
            if square is not None:
                square.piece = None

    def _create_squares(self):
        index = 0
        for rank in range(7, -1, -1):
            for file in range(8):
                left = file * SQUARE_LENGTH
                top = rank * SQUARE_LENGTH
                color = BLACK

                if (
                    (file % 2 != 0)
                    and (rank % 2 != 0)
                    or (file % 2 == 0)
                    and (rank % 2 == 0)
                ):
                    color = WHITE

                s = Square(left, top, SQUARE_LENGTH, color, index)
                self.squares.append(s)
                index += 1

    # values used in this method seem random but are based on properties of the png containing the piece images
    def _load_piece_images(self):
        for i in range(12):
            left = (i % 6) * 333
            top = 0
            if i > 5:
                top = 334

            cropped = self.pieces_png.subsurface((left, top, 334, 334))
            scaled = pygame.transform.smoothscale(cropped, (80, 80))

            name = PIECE_NAMES[i % 6]
            if i <= 5:
                name = name.upper()
            elif i > 5:
                name = name.lower()
            self.pieces[name] = scaled

    def _draw_squares(self, surface: pygame.Surface):
        for square in self.squares:
            pygame.draw.rect(surface, square.color, square.rect)

    def _draw_pieces(self, surface):
        for square in self.squares:
            if square.piece is not None:
                surface.blit(
                    self.pieces[square.piece.symbol],
                    (square.left, square.top),
                )

    def _draw_moves(self, surface: pygame.Surface, legalMoves):
        active = self.active_piece
        if active is not None:
            for move in legalMoves:
                from_square = move.from_square
                to_square = move.to_square
                # print(move)
                # print(from_square, to_square)
                # print(active.index)
                if from_square == active.index:
                    # print(from_square, to_square)
                    destSquare = self.squares[to_square]
                    destSquareCenter = self._get_square_center(destSquare)
                    # print(active.left, active.top)
                    # print(destSquare.left, destSquare.top)
                    # print(destSquareCenter)
                    pygame.draw.circle(surface, [30, 144, 255], destSquareCenter, 10)

    def draw(self, surface: pygame.Surface, legalMoves):
        self._draw_squares(surface)
        self._draw_pieces(surface)
        self._draw_moves(surface, legalMoves)

    def set_board_fen(self, fen: str):
        self._empty_board()
        fen_ranks = fen.split("/")
        fen_ranks.reverse()
        square_index = 0
        for rank in fen_ranks:
            for symbol in rank:
                if symbol.isalpha():
                    left, top = self._square_to_coords(square_index)
                    self.squares[square_index].piece = Piece(symbol, left, top)
                    square_index += 1
                else:
                    square_index += int(symbol)

    def move_piece_from_to(self, src: str, dest: str):
        if len(src) == 0 or len(dest) == 0:
            raise Exception("missing src or dest location")

        srcSquare = self._parse_square_name(src)
        destSquare = self._parse_square_name(dest)
        srcPiece = self.squares[srcSquare].piece
        top, left = self._square_to_coords(srcSquare)

        srcPiece.top = top
        srcPiece.left = left

        self.squares[destSquare].piece = srcPiece
        self.squares[srcSquare].piece = None
