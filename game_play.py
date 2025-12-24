# game loop goes here to be called in main.py

import os
import pygame

PLAYER_SIZE = 64
PLAYER_SPEED = 260  # pixels per second

DEBUG_DRAW_COLLIDERS = False



def run_game(screen, clock):
    
    bg_path = os.path.join(os.path.dirname(__file__), "assets", "home_bg.png")
    background = pygame.image.load(bg_path).convert()  # use convert_alpha() if it has transparency
    background = pygame.transform.scale(background, screen.get_size())

    # --- world setup ---
    player_rect = pygame.Rect(0,0, PLAYER_SIZE, PLAYER_SIZE)
    player_rect.center = screen.get_rect().center


    

    while True:
        dt = clock.tick(60) / 1000.0  # seconds since last frame

        # --- events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"  # or return "QUIT" if you prefer

        # --- input (continuous) ---
        keys = pygame.key.get_pressed()
        vx = vy = 0.0

        if keys[pygame.K_a] or keys[pygame.K_a]:
            vx = -PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_d]:
            vx = PLAYER_SPEED
        if keys[pygame.K_w] or keys[pygame.K_w]:
            vy = -PLAYER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_s]:
            vy = PLAYER_SPEED

        # prevent faster diagonal movement
        if vx != 0 and vy != 0:
            vx *= 0.7071
            vy *= 0.7071

# --- APPLY MOVEMENT HERE ---
        player_rect.x += int(vx * dt)
        player_rect.y += int(vy * dt)
        # --- draw ---
        screen.blit(background, (0,0))

        



        # draw player
        pygame.draw.rect(screen, (50, 180, 255), player_rect)

        pygame.display.flip()

