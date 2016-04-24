import pygame, sys
from pygame.locals import *
 
pygame.init()
 
screen = pygame.display.set_mode((1920, 1080))
 
clock = pygame.time.Clock()
 
bgOne = pygame.image.load('back.png')
bgTwo = pygame.image.load('back1.png')
 
bgOne_x = 0
bgTwo_x = bgOne.get_width()
 
while True:
 
    screen.blit(bgOne, (bgOne_x, 0))
    screen.blit(bgTwo, (bgTwo_x, 0))
 
    pygame.display.update()
 
    bgOne_x -= 1
    bgTwo_x -= 1
 
    if bgOne_x == -1 * bgOne.get_width():
        bgOne_x = bgTwo_x + bgTwo.get_width()
    if bgTwo_x == -1 * bgTwo.get_width():
        bgTwo_x = bgOne_x + bgOne.get_width()
 
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            sys.exit()

