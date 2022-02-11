import pygame
from constants import SQUARE_LENGTH, WHITE, BLACK


piece_names = ["KING","QUEEN","BISHOP","KNIGHT","ROOK","PAWN"]


class Square:
    def __init__(self, left, top, length, color):
            self.left = left
            self.top = top
            self.length = length
            self.rect = pygame.Rect(left, top, self.length, self.length)

            self.color = color


class Piece:
    def __init__(self, color, name, left, top):
        self.name = name
        self.color = color
        self.left = left
        self.top = top


class Board:
    def __init__(self):
        self.squares = []
        self.pieces = {}
        self.board = [[None for j in range(8)] for i in range(8)]
        self.pieces_png = pygame.image.load('./images/Pieces.png').convert_alpha()
        self._create_squares()
        self._load_piece_images()

    def _create_squares(self):
        for rank in range(8):
            for file in range(8):
                left = file * SQUARE_LENGTH
                top = rank * SQUARE_LENGTH

                color = BLACK
                if ((file % 2 != 0) and (rank % 2 != 0)) or (file % 2 == 0) and (rank % 2 == 0):
                    color = WHITE
                s = Square(left, top, SQUARE_LENGTH, color)
                self.squares.append(s)
    
    def _load_piece_images(self):
        for i in range(12):
            left = (i % 6) * 333
            top = 0
            if i > 5:
                top = 334

            cropped = self.pieces_png.subsurface((left, top, 334, 334))
            scaled = pygame.transform.scale(cropped, (80, 80))

            name = piece_names[i % 6]
            color = 'w'
            if i > 5:
                color = 'b'
            self.pieces[color + name] = scaled
    
    def _draw_squares(self, surface):
        pass

    def _draw_pieces(self, surface):
        pass
    
    def draw(self, surface):
        for square in self.squares:
            pygame.draw.rect(surface, square.color, square.rect)
        for rank in self.board:
            for piece in rank:
                if piece is not None:
                    surface.blit(self.pieces[piece.color + piece.name], (piece.left, piece.top))
    
    def init_board(self):
        for file in range(8):
            left = file * 80
            wTop = 80 * 6
            bTop = 80
            self.board[1][file] = Piece('w', "PAWN", left, wTop)
            self.board[6][file] = Piece('b', "PAWN", left, bTop)

        wTop = 80 * 7
        bTop = 0
        self.board[0][0] = Piece('w', "ROOK", 0, wTop)
        self.board[0][1] = Piece('w', "KNIGHT", 80, wTop)
        self.board[0][2] = Piece('w', "BISHOP", 160, wTop)
        self.board[0][3] = Piece('w', "QUEEN", 240, wTop)
        self.board[0][4] = Piece('w', "KING", 320, wTop)
        self.board[0][5] = Piece('w', "BISHOP", 400, wTop)
        self.board[0][6] = Piece('w', "KNIGHT", 480, wTop)
        self.board[0][7] = Piece('w', "ROOK", 560, wTop)
        self.board[7][0] = Piece('b', "ROOK", 0, bTop)
        self.board[7][1] = Piece('b', "KNIGHT", 80, bTop)
        self.board[7][2] = Piece('b', "BISHOP", 160, bTop)
        self.board[7][3] = Piece('b', "QUEEN", 240, bTop)
        self.board[7][4] = Piece('b', "KING", 320, bTop)
        self.board[7][5] = Piece('b', "BISHOP", 400, bTop)
        self.board[7][6] = Piece('b', "KNIGHT", 480, bTop)
        self.board[7][7] = Piece('b', "ROOK", 560, bTop)
