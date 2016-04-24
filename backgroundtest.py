import pygame
import sys
import pygame.sprite as sprite

theClock = pygame.time.Clock()

background = pygame.image.load('back2.png')

background_size = background.get_size()
background_rect = background.get_rect()
screen = pygame.display.set_mode(background_size)
w,h = background_size
x = 0
y = 0

x1 = -w
y1 = 0

running = True

while running:
    screen.blit(background,background_rect)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    x1 += 100
    x += 100
    screen.blit(background,(x,y))
    screen.blit(background,(x1,y1))
    if x > w:
        x = -w
    if x1 > w:
        x1 = -w
    pygame.display.flip()
    pygame.display.update()
