import random
import pygame
from settings import SHAPES, COLORS, COLS, ROWS

BLOCK_SIZE = 30
NEXT_PIECES_X = COLS + 2  
HOLD_PIECE_X = COLS + 2 
NEXT_PIECES_Y = 2  
HOLD_PIECE_Y = 2  

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape 
        self.color = COLORS[SHAPES.index(shape)] 
        self.rotation = 0  

    def get_shape(self):
        return self.shape[self.rotation % len(self.shape)]  

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)


class Grid:
    def __init__(self):
        self.grid = [[(0, 0, 0) for _ in range(COLS)] for _ in range(ROWS)]  

    def add_piece(self, piece):
        for x, y in self.convert_shape(piece):
            if 0 <= y < ROWS and 0 <= x < COLS:
                self.grid[y][x] = piece.color

    def convert_shape(self, piece):
        positions = []
        shape = piece.get_shape()  
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:  
                    positions.append((piece.x + j, piece.y + i))
        return positions

    def valid_space(self, piece):
        for x, y in self.convert_shape(piece):
            if y >= ROWS or x < 0 or x >= COLS or self.grid[y][x] != (0, 0, 0):
                return False
        return True

    def clear_rows(self):
        """Clear full rows and shift others down, return score based on cleared rows."""
        full_rows = [i for i, row in enumerate(self.grid) if (0, 0, 0) not in row]
        score = len(full_rows) * 100 
        for row_index in full_rows:
            self.grid.pop(row_index)
            self.grid.insert(0, [(0, 0, 0) for _ in range(COLS)])
        return score

    def draw(self, surface):
        """Draw the grid with the current pieces."""
        for y in range(ROWS):
            for x in range(COLS):
                pygame.draw.rect(surface, self.grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


class TetrisGame:
    def __init__(self):
        self.grid = Grid()
        self.current_piece = self.get_new_piece()
        self.next_pieces = [self.get_new_piece() for _ in range(5)]
        self.game_over = False
        self.score = 0
        self.fall_time = 0
        self.fall_speed = 0.5
        self.move_timer = 0
        self.move_delay = 0.2 
        self.rotation_timer = 0
        self.rotation_delay = 0.2  
        self.dropping = False  
        self.space_pressed = False 
        self.held_piece = None  

    def get_new_piece(self):
        return Piece(COLS // 2 - 2, 0, random.choice(SHAPES))

    def update_game(self, dt):
        """Update the game state by moving the piece down and handling input."""
        if self.game_over:
            return
        self.fall_time += dt
        if not self.dropping:  
            if self.fall_time >= self.fall_speed:
                self.fall_time = 0
                self.move_piece(0, 1)
        self.handle_input(dt)

    def move_piece(self, dx, dy):
        """Move the piece and check if it's valid."""        
        self.current_piece.x += dx
        self.current_piece.y += dy
        if not self.grid.valid_space(self.current_piece):
            self.current_piece.x -= dx
            self.current_piece.y -= dy
            if dy > 0:  
                self.grid.add_piece(self.current_piece)

                cleared_rows_score = self.grid.clear_rows()
                self.score += cleared_rows_score  
                self.current_piece = self.next_pieces.pop(0)  
                self.next_pieces.append(self.get_new_piece())  
                if not self.grid.valid_space(self.current_piece):
                    self.game_over = True

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        if self.move_timer >= self.move_delay:
            if keys[pygame.K_LEFT]:
                self.move_piece(-1, 0)
                self.move_timer = 0
            elif keys[pygame.K_RIGHT]:
                self.move_piece(1, 0)
                self.move_timer = 0
        if keys[pygame.K_DOWN]:
            self.move_piece(0, 1)
        if keys[pygame.K_UP] and self.rotation_timer >= self.rotation_delay:
            self.current_piece.rotate()
            if not self.grid.valid_space(self.current_piece):
                self.current_piece.rotation -= 1
            self.rotation_timer = 0


        if keys[pygame.K_SPACE]:
            if not self.space_pressed: 
                self.space_pressed = True
                self.dropping = True

                while self.grid.valid_space(self.current_piece):
                    self.current_piece.y += 1
                self.current_piece.y -= 1  
                self.grid.add_piece(self.current_piece)  
                cleared_rows_score = self.grid.clear_rows()  
                self.score += cleared_rows_score 

                self.current_piece = self.next_pieces.pop(0) 
                self.next_pieces.append(self.get_new_piece()) 
                if not self.grid.valid_space(self.current_piece):
                    self.game_over = True  
                self.dropping = False  

        elif not keys[pygame.K_SPACE]:  
            self.space_pressed = False

        if keys[pygame.K_c] and not self.game_over:
            if self.held_piece is None:
                self.held_piece = self.current_piece
                self.current_piece = self.next_pieces.pop(0)
                self.next_pieces.append(self.get_new_piece())
            else:
                self.current_piece, self.held_piece = self.held_piece, self.current_piece

        self.move_timer += dt
        self.rotation_timer += dt

    def draw(self, surface):
        """Draw the game grid and the current piece."""
        self.grid.draw(surface)
        
        for x, y in self.grid.convert_shape(self.current_piece):
            if y >= 0:
                pygame.draw.rect(surface, self.current_piece.color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        ghost_piece = Piece(self.current_piece.x, self.current_piece.y, self.current_piece.shape)
        ghost_piece.rotation = self.current_piece.rotation  

        while self.grid.valid_space(ghost_piece):
            ghost_piece.y += 1
        ghost_piece.y -= 1  

        for x, y in self.grid.convert_shape(ghost_piece):
            if y >= 0:
                pygame.draw.rect(surface, (50, 50, 50), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 2)

        font = pygame.font.SysFont('Arial', 30)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        surface.blit(score_text, (10, 10)) 

        for i, piece in enumerate(self.next_pieces):
            shape = piece.get_shape()
            for j, row in enumerate(shape):
                for k, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(surface, piece.color,
                                         ((NEXT_PIECES_X + k) * BLOCK_SIZE, (NEXT_PIECES_Y + i * 4 + j) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        if self.held_piece:
            shape = self.held_piece.get_shape()
            for j, row in enumerate(shape):
                for k, cell in enumerate(row):
                    if cell: 
                        pygame.draw.rect(surface, self.held_piece.color,
                                         (HOLD_PIECE_X * BLOCK_SIZE, (HOLD_PIECE_Y + j) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


        if self.game_over:
            font = pygame.font.SysFont('Arial', 50)
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 3))
            surface.blit(game_over_text, text_rect)

            restart_text = font.render("Press R to Restart", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
            surface.blit(restart_text, restart_rect)

        pygame.display.update()
