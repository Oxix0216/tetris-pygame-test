# grid.py
from settings import COLS, ROWS, BLOCK_SIZE
import pygame

class Grid:
    def __init__(self):

        self.grid = [[(0, 0, 0) for _ in range(COLS)] for _ in range(ROWS)]

    def add_piece(self, piece):
        """Add the piece to the grid."""
        for x, y in self.convert_shape(piece):
            if 0 <= y < ROWS and 0 <= x < COLS:
                self.grid[y][x] = piece.color

    def convert_shape(self, piece):
        """Convert the shape of the piece into grid positions."""
        positions = []
        shape = piece.shape 

        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    positions.append((piece.x + j, piece.y + i)) 
        return positions

    def valid_space(self, piece):
        """Check if the piece is in a valid position on the grid."""
        for x, y in self.convert_shape(piece):

            if y >= ROWS or x < 0 or x >= COLS or self.grid[y][x] != (0, 0, 0):
                return False 
        return True

    def clear_rows(self):
        """Clear full rows and shift the grid down."""
        for i, row in enumerate(self.grid):
            if (0, 0, 0) not in row:  
                self.grid.pop(i)
                self.grid.insert(0, [(0, 0, 0) for _ in range(COLS)])

    def draw(self, surface):
        """Draw the grid."""
        for y in range(ROWS):
            for x in range(COLS):
                pygame.draw.rect(surface, self.grid[y][x], 
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
