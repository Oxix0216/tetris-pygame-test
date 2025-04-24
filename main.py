import pygame
from tetris import TetrisGame
from settings import BLOCK_SIZE, COLS, ROWS
import time  # Import time module to control the popup duration

pygame.init()

screen = pygame.display.set_mode((COLS * BLOCK_SIZE, ROWS * BLOCK_SIZE))
pygame.display.set_caption('Tetris')

clock = pygame.time.Clock()

def show_popup(surface):
    font = pygame.font.SysFont("Arial", 40)
    text = font.render("Developed by Siso", True, (255, 255, 255))  # White text
    text_rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))

    surface.fill((0, 0, 0))
    surface.blit(text, text_rect)
    pygame.display.flip()

    time.sleep(3)

def main():
    game = TetrisGame()
    
    show_popup(screen)
    
    running = True
    while running:
        dt = clock.get_time() / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.game_over:
                    game = TetrisGame()  # Restart the game
        
        game.update_game(dt)
        
        screen.fill((0, 0, 0))
        
        game.draw(screen)
        
        pygame.display.flip()
        
        clock.tick(24)

    pygame.quit()

if __name__ == '__main__':
    main()
