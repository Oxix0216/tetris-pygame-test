import random
import pygame
from settings import SHAPES, COLORS, COLS, ROWS

BLOCK_SIZE = 30
NEXT_PIECES_X = COLS + 2  # Adjust X position for next pieces
HOLD_PIECE_X = COLS + 2  # Adjust X position for hold piece
NEXT_PIECES_Y = 2  # Starting Y position for next pieces
HOLD_PIECE_Y = 2  # Starting Y position for the hold piece

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape  # shape should be a list of rows, where each row is a list of 0 or 1
        self.color = COLORS[SHAPES.index(shape)]  # color based on the shape index
        self.rotation = 0  # rotation state

    def get_shape(self):
        return self.shape[self.rotation % len(self.shape)]  # Support rotation

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)


class Grid:
    def __init__(self):
        self.grid = [[(0, 0, 0) for _ in range(COLS)] for _ in range(ROWS)]  # Initialize a grid with black cells

    def add_piece(self, piece):
        for x, y in self.convert_shape(piece):
            if 0 <= y < ROWS and 0 <= x < COLS:
                self.grid[y][x] = piece.color

    def convert_shape(self, piece):
        positions = []
        shape = piece.get_shape()  # Get the current shape based on rotation
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:  # Only consider non-zero cells in the shape
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
        score = len(full_rows) * 100  # Award 100 points per row cleared
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
        self.next_pieces = [self.get_new_piece() for _ in range(5)]  # List to store the next 5 pieces
        self.game_over = False
        self.score = 0
        self.fall_time = 0
        self.fall_speed = 0.5  # seconds
        self.move_timer = 0
        self.move_delay = 0.2  # Time in seconds between piece moves
        self.rotation_timer = 0
        self.rotation_delay = 0.2  # Time in seconds between rotations
        self.dropping = False  # New flag to track if the piece is being dropped instantly
        self.space_pressed = False  # New flag to detect if spacebar is being pressed
        self.held_piece = None  # Hold piece for future use

    def get_new_piece(self):
        return Piece(COLS // 2 - 2, 0, random.choice(SHAPES))

    def update_game(self, dt):
        """Update the game state by moving the piece down and handling input."""
        if self.game_over:
            return
        self.fall_time += dt
        if not self.dropping:  # Don't fall automatically if we're in drop mode
            if self.fall_time >= self.fall_speed:
                self.fall_time = 0
                self.move_piece(0, 1)  # Move the piece down
        self.handle_input(dt)

    def move_piece(self, dx, dy):
        """Move the piece and check if it's valid."""        
        self.current_piece.x += dx
        self.current_piece.y += dy
        if not self.grid.valid_space(self.current_piece):
            self.current_piece.x -= dx
            self.current_piece.y -= dy
            if dy > 0:  # If piece reaches the bottom
                self.grid.add_piece(self.current_piece)
                # Clear full rows and update score
                cleared_rows_score = self.grid.clear_rows()
                self.score += cleared_rows_score  # Update the score
                self.current_piece = self.next_pieces.pop(0)  # Get the next piece from the list
                self.next_pieces.append(self.get_new_piece())  # Add a new piece to the end of the list
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

        # Handle spacebar press for instant drop
        if keys[pygame.K_SPACE]:
            if not self.space_pressed:  # Only drop once if space wasn't previously pressed
                self.space_pressed = True
                self.dropping = True
                # Move the current piece down until it can't move anymore
                while self.grid.valid_space(self.current_piece):
                    self.current_piece.y += 1
                self.current_piece.y -= 1  # Correct position, one step back after invalid space
                self.grid.add_piece(self.current_piece)  # Add piece to grid
                cleared_rows_score = self.grid.clear_rows()  # Clear any full rows
                self.score += cleared_rows_score  # Update the score after clearing rows
                # Set the current piece to the next piece without affecting the next shape
                self.current_piece = self.next_pieces.pop(0)  # Get the next piece from the list
                self.next_pieces.append(self.get_new_piece())  # Add a new piece to the list
                if not self.grid.valid_space(self.current_piece):
                    self.game_over = True  # End game if no valid space for the new piece
                self.dropping = False  # Reset the dropping state

        elif not keys[pygame.K_SPACE]:  # Reset space_pressed when space is released
            self.space_pressed = False

        # Handle hold piece
        if keys[pygame.K_c] and not self.game_over:
            if self.held_piece is None:
                self.held_piece = self.current_piece
                self.current_piece = self.next_pieces.pop(0)
                self.next_pieces.append(self.get_new_piece())
            else:
                self.current_piece, self.held_piece = self.held_piece, self.current_piece

        # Update timers
        self.move_timer += dt
        self.rotation_timer += dt

    def draw(self, surface):
        """Draw the game grid and the current piece."""
        self.grid.draw(surface)
        
        # Draw current piece
        for x, y in self.grid.convert_shape(self.current_piece):
            if y >= 0:  # Only draw if the piece is not below the screen
                pygame.draw.rect(surface, self.current_piece.color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Draw ghost piece (rotated correctly)
        ghost_piece = Piece(self.current_piece.x, self.current_piece.y, self.current_piece.shape)
        ghost_piece.rotation = self.current_piece.rotation  # Sync the rotation of the ghost piece
        # Move ghost piece down until it hits a collision
        while self.grid.valid_space(ghost_piece):
            ghost_piece.y += 1
        ghost_piece.y -= 1  # Correct position, one step back after invalid space

        # Draw ghost piece in a lighter gray
        for x, y in self.grid.convert_shape(ghost_piece):
            if y >= 0:
                pygame.draw.rect(surface, (50, 50, 50), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 2)

        # Draw the score
        font = pygame.font.SysFont('Arial', 30)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        surface.blit(score_text, (10, 10))  # Draw score at the top-left of the screen

        # Draw the next 5 pieces in smaller boxes to the right of the grid
        for i, piece in enumerate(self.next_pieces):
            shape = piece.get_shape()
            for j, row in enumerate(shape):
                for k, cell in enumerate(row):
                    if cell:  # Only draw non-empty cells
                        pygame.draw.rect(surface, piece.color,
                                         ((NEXT_PIECES_X + k) * BLOCK_SIZE, (NEXT_PIECES_Y + i * 4 + j) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Draw the hold piece
        if self.held_piece:
            shape = self.held_piece.get_shape()
            for j, row in enumerate(shape):
                for k, cell in enumerate(row):
                    if cell:  # Only draw non-empty cells
                        pygame.draw.rect(surface, self.held_piece.color,
                                         (HOLD_PIECE_X * BLOCK_SIZE, (HOLD_PIECE_Y + j) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # If game over, display the "Game Over" screen
        if self.game_over:
            font = pygame.font.SysFont('Arial', 50)
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 3))
            surface.blit(game_over_text, text_rect)

            restart_text = font.render("Press R to Restart", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
            surface.blit(restart_text, restart_rect)

        pygame.display.update()
