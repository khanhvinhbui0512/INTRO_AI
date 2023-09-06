from tkinter import Y

import pygame
pygame.init()
screen_width = 1000
screen_height = 500
display = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Bloxorz")

TILE_COLOR = (199,208,207)
BLACK = (0,0,0)
BLOCK_COLOR = (165, 42, 42)

def draw_block(map_x, map_y, block_state):
    pygame.draw.rect(display, BLOCK_COLOR, (map_x+5, map_y+5, 39, 39))

level = [
    [1,1,1,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,1,1,9,1,1],
    [0,0,0,0,0,0,1,1,1,0]
]

def draw_map(startX = 100,startY = 50):
    x,y = startX,startY
    i = 1
    for row in level:
        for tile in row:
            if (tile == 1):
                pygame.draw.rect(display,TILE_COLOR,(x,y,50,50))
                pygame.draw.line(display,BLACK,(x+50,y),(x+50,y+50),5)
                pygame.draw.line(display,BLACK,(x,y+50),(x+50,y+50),5)
            x += 50
        x = startX
        y += 50    

block_x = 1
block_y = 1

while(True):
    for e in pygame.event.get():
        if (e.type == pygame.KEYDOWN):
            if (e.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
            if (e.key == pygame.K_LEFT):
                print("LEFT")
            if (e.key == pygame.K_RIGHT):
                print("RIGHT")
            if (e.key == pygame.K_UP):
                print("UP")
            if (e.key == pygame.K_DOWN):
                print("DOWN")
        if (e.type == pygame.QUIT):
            pygame.quit()
            quit() 
    display.fill((193,39,1)) #fill screen
    draw_map()
    draw_block(100,100,"block_state")
    pygame.display.update() #update screen