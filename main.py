import pygame
from constants import *
from menu import *
from game_play import *
from options import *

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("CultQuest")
    print("Attempting to run menu")


    current_game_state = run_menu(screen, clock)
    print("Starting CultQuest with pygame version: 3.12")
    print("Screen width: 1280")
    print("Screen height: 720")
    while True:
        if current_game_state == "PLAYING":
            current_game_state = run_game(screen, clock)
        elif current_game_state == "QUIT":
            pygame.quit()
            return
        elif current_game_state == "OPTIONS":
            current_game_state = run_options(screen, clock)

            
    
    

if __name__ == "__main__":
    main()