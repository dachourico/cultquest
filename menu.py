#menu goes here to get into the game

import pygame

def run_menu(screen, clock):
    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 50

    #Button
    start_button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
    start_button_rect.center = screen.get_rect().center

    # Title text
    title_font = pygame.font.Font(None, 96)
    title_surface = title_font.render("CULT QUEST", True, (255,255,255))
    title_rect = title_surface.get_rect(center=(screen.get_width() // 2, start_button_rect.top - 60))
    
    #Button Text
    font = pygame.font.Font(None, 40)
    text_surface = font.render("START", True, (255,255,255))
    text_rect = text_surface.get_rect(center=start_button_rect.center)
    

    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return "PLAYING"
        
        screen.fill((50, 50, 50))
        pygame.draw.rect(screen, (0,200,0), start_button_rect)
        screen.blit(text_surface, text_rect)
        screen.blit(title_surface, title_rect)

        pygame.display.flip()
        clock.tick(60)
    return "QUIT"