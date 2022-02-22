import pygame
from constants import *


class Square:
    def __init__(self, left, top, length, color, index):
        self.left = left
        self.top = top
        self.length = length
        self.rect = pygame.Rect(left, top, self.length, self.length)
        self.color = color
        self.piece: Piece = None
        self.index = index
        self.name = self._get_name()

    def _get_name(self):
        names = list(SQUARE_NAME_NUM_MAP.keys())
        vals = list(SQUARE_NAME_NUM_MAP.values())
        return names[vals.index(self.index)]

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
                + str(self.name)
            )
        else:
            square += (
                "#"
                + " "
                + str(self.left)
                + " "
                + str(self.top)
                + " "
                + str(self.index)
                + " "
                + str(self.name)
            )
        return square

    def reset_piece_pos(self):
        if self.piece is not None:
            self.piece.left = self.left
            self.piece.top = self.top
            self.piece.offset_left = 0
            self.piece.offset_top = 0
            self.piece.dragging = False

    def set_piece_offsets(self, left, top):
        if self.piece is not None:
            self.piece.offset_left = self.left - left
            self.piece.offset_top = self.top - top


class Piece:
    def __init__(self, symbol, left, top):
        self.symbol = symbol
        self.dragging = False
        self.left = left
        self.top = top
        self.offset_left = 0
        self.offset_top = 0

    def __str__(self):
        return self.symbol


class Board:
    def __init__(self) -> None:
        self.squares = []
        self.pieces = {}
        self._create_squares()
        self._load_piece_images()
        self.active_square: Square = None

    def __str__(self) -> str:
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

    def _square_to_coords(self, square: int) -> tuple:
        left = (square & 7) * 80
        top = (square >> 3) * 80
        return (left, top)

    def _parse_square_name(self, square_index: str) -> int:
        return SQUARE_NAME_NUM_MAP[square_index]

    def _get_square_center(self, square: Square) -> tuple:
        return (square.left + 40, square.top + 40)

    def _empty_board(self) -> None:
        for square in self.squares:
            if square is not None:
                square.piece = None

    def _create_squares(self) -> None:
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

    # load chess piece image from png containing all of them in one place
    # images will be cropped to  333x334px on a subsurface then scaled down
    # to 80x80px to fit on a square
    def _load_piece_images(self) -> None:
        pieces_png = pygame.image.load("./images/Pieces.png").convert_alpha()
        for i in range(12):
            left = (i % 6) * 333  # left coord of crop area
            top = 0  # top coord of corp area
            if i > 5:
                top = 334

            cropped = pieces_png.subsurface((left, top, 334, 334))
            scaled = pygame.transform.smoothscale(cropped, (80, 80))

            name = PIECE_NAMES[i % 6]
            if i <= 5:
                name = name.upper()
            elif i > 5:
                name = name.lower()
            self.pieces[name] = scaled

    def _draw_squares(self, surface: pygame.Surface) -> None:
        for square in self.squares:
            pygame.draw.rect(surface, square.color, square.rect)

    def _draw_pieces(self, surface) -> None:
        for square in self.squares:
            if square.piece is not None:
                if not square.piece.dragging:
                    surface.blit(
                        self.pieces[square.piece.symbol],
                        (square.left, square.top),
                    )
                else:
                    surface.blit(
                        self.pieces[square.piece.symbol],
                        (square.piece.left, square.piece.top),
                    )

    # draw a circle on any square that is a legal move for the
    # piece on the current active square of the board
    def _draw_moves(self, surface: pygame.Surface, legalMoves) -> None:
        active = self.active_square
        if active is not None:
            for move in legalMoves:
                from_square = move.from_square
                to_square = move.to_square
                if from_square == active.index:
                    destSquare = self.squares[to_square]
                    destSquareCenter = self._get_square_center(destSquare)
                    pygame.draw.circle(surface, PURPLE, destSquareCenter, 10)

    def draw(self, surface: pygame.Surface, legalMoves) -> None:
        self._draw_squares(surface)
        self._draw_pieces(surface)
        self._draw_moves(surface, legalMoves)

    # set pieces on the board based on a FEN string
    def set_board_fen(self, fen: str) -> None:
        self._empty_board()
        fen_ranks = fen.split("/")
        fen_ranks.reverse()
        square_index = 0
        for rank in fen_ranks:
            for symbol in rank:
                if symbol.isalpha():
                    left = self.squares[square_index].left
                    top = self.squares[square_index].top
                    self.squares[square_index].piece = Piece(symbol, left, top)
                    square_index += 1
                else:
                    square_index += int(symbol)

    def move_from_to(self, src: str, dest: str) -> None:
        if len(src) == 0 or len(dest) == 0:
            raise Exception("missing src or dest location")

        src_square_index = self._parse_square_name(src)
        dest_square_index = self._parse_square_name(dest)

        src_piece = self.squares[src_square_index].piece
        if src_piece is not None:
            self.squares[dest_square_index].piece = src_piece
            self.squares[dest_square_index].piece.left = self.squares[
                dest_square_index
            ].left
            self.squares[dest_square_index].piece.top = self.squares[
                dest_square_index
            ].top
            self.squares[src_square_index].piece = None

    def kingside_castle(self, src, dest) -> None:
        color = (
            self.active_square.piece.symbol.isupper()
        )  # true if white, false if black
        rook_src = None
        rook_dest = None
        if color:
            rook_src = self.squares[7].name
            rook_dest = "f1"
        else:
            rook_src = self.squares[63].name
            rook_dest = "f8"
        self.move_from_to(src, dest)
        self.move_from_to(rook_src, rook_dest)

    def queenside_castle(self, src, dest) -> None:
        color = (
            self.active_square.piece.symbol.isupper()
        )  # true if white, false if black
        rook_src = None
        rook_dest = None
        if color:
            rook_src = self.squares[0].name
            rook_dest = "d1"
        else:
            rook_src = self.squares[56].name
            rook_dest = "d8"
        self.move_from_to(src, dest)
        self.move_from_to(rook_src, rook_dest)

    def en_passant(self, src, dest):
        pass
