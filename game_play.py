# game loop goes here to be called in main.py

import os
import pygame

PLAYER_SIZE = 32
PLAYER_SPEED = 220  # pixels per second

DEBUG_DRAW_COLLIDERS = True



def run_game(screen, clock):
    
    bg_path = os.path.join(os.path.dirname(__file__), "assets", "house.webp")
    background = pygame.image.load(bg_path).convert()  # use convert_alpha() if it has transparency
    background = pygame.transform.scale(background, screen.get_size())

    # --- world setup ---
    player_rect = pygame.Rect(0,0, PLAYER_SIZE, PLAYER_SIZE)
    player_rect.center = screen.get_rect().center

    # Example colliders (walls). Later these come from your tilemap.
    walls = [
        pygame.Rect(300, 150, 200, 40),
        pygame.Rect(200, 350, 40, 200),
        pygame.Rect(50, 500, 700, 30),
    ]

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

        # --- move + collide (axis-separated) ---
        player_rect.x += int(vx * dt)
        for wall in walls:
            if player_rect.colliderect(wall):
                if vx > 0:  # moving right
                    player_rect.right = wall.left
                elif vx < 0:  # moving left
                    player_rect.left = wall.right

        player_rect.y += int(vy * dt)
        for wall in walls:
            if player_rect.colliderect(wall):
                if vy > 0:  # moving down
                    player_rect.bottom = wall.top
                elif vy < 0:  # moving up
                    player_rect.top = wall.bottom

        # --- draw ---
        screen.blit(background, (0,0))

        if DEBUG_DRAW_COLLIDERS:
            for wall in walls:
                pygame.draw.rect(screen, (120,120,120), wall, 2)

        # draw walls
        for wall in walls:
            pygame.draw.rect(screen, (120, 120, 120), wall, 2)
            walls = [
                pygame.Rect(0, 0, 1280, 40),        # top wall
                pygame.Rect(0, 0, 40, 720),         # left wall
                pygame.Rect(0, 680, 1280, 40),      # bottom wall
                pygame.Rect(1240, 0, 40, 720),      # right wall

                pygame.Rect(870, 70, 222, 220),     # fireplace
                pygame.Rect(520, 210, 248, 130),    # table
                pygame.Rect(980, 420, 260, 220),    # bed
                pygame.Rect(75, 190, 211, 160), #tv
                ]


        

        # draw player
        pygame.draw.rect(screen, (50, 180, 255), player_rect)

        pygame.display.flip()

