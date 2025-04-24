import pygame
from tetris import TetrisGame
from settings import BLOCK_SIZE, COLS, ROWS
import time  # Import time module to control the popup duration

# Initialize pygame
pygame.init()

# Set the width and height of the screen based on the grid size and block size
screen = pygame.display.set_mode((COLS * BLOCK_SIZE, ROWS * BLOCK_SIZE))
pygame.display.set_caption('Tetris')

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Function to show popup message
def show_popup(surface):
    font = pygame.font.SysFont("Arial", 40)
    text = font.render("Developed by Siso", True, (255, 255, 255))  # White text
    text_rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))

    # Display the text for 3 seconds
    surface.fill((0, 0, 0))  # Clear the screen with black background
    surface.blit(text, text_rect)
    pygame.display.flip()

    time.sleep(3)  # Wait for 3 seconds before starting the game

def main():
    game = TetrisGame()  # Create a Tetris game instance
    
    # Show the popup message before starting the game
    show_popup(screen)
    
    running = True
    while running:
        dt = clock.get_time() / 1000.0  # Calculate the delta time in seconds
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle restarting the game with the 'R' key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.game_over:
                    game = TetrisGame()  # Restart the game
        
        # Update the game state
        game.update_game(dt)
        
        # Fill the screen with black before drawing the new frame
        screen.fill((0, 0, 0))
        
        # Draw the game state
        game.draw(screen)
        
        # Update the display
        pygame.display.flip()
        
        # Run at 24 FPS (frames per second)
        clock.tick(24)

    pygame.quit()

if __name__ == '__main__':
    main()
