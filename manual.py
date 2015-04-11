from gamestate import Response, GameState
import sys
import pygame

pygame.init()
#surface = pygame.display.set_mode([1000, 1000])

r = Response()
state = GameState()

(width, height) = (100, 100)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Manual Control')
running = True
count = 0;


rotate_left = False
rotate_right = False
while running:
    state.read()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                rotate_left = (event.type == pygame.KEYDOWN)
            elif event.key == pygame.K_RIGHT:
                rotate_right = (event.type == pygame.KEYDOWN)
            elif event.key == pygame.K_UP:
                r.set_thrust(event.type == pygame.KEYDOWN)
            elif event.key == pygame.K_SPACE:
                r.set_fire(event.type == pygame.KEYDOWN)
    if(rotate_left):
        r.set_ccw()
    elif(rotate_right):
        r.set_cw()
    else:
        r.set_no_turn()

    pygame.display.flip()
    r.send()
