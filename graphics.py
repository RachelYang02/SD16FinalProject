import pygame
from pygame.locals import *
import time
import random
import numpy as np
from numpy import * 

# TO DO 
# + scaling in make_cart for polar conversion after calcuations
# + don't forget to scale back down 


class Matrix(object):
    #does something
    def __init__(self, screen_size, initial_vals, direction = True):
        self.coordinates = initial_vals # our house for all of our positions
        self.screen_size = screen_size
        self.direction = direction
        self.trans = np.zeros((self.coordinates.size/2,2)) - 0.002

    def vibration(self): 
        if self.direction == True:
        	self.trans += 0.004
        	self.coordinates = np.add(self.coordinates,self.trans)
        	self.direction = False
        else:
        	self.trans -= 0.004
        	self.coordinates = np.add(self.coordinates,self.trans)
        	self.direction = True



         # translate primary matrix


class View(object):

    def __init__(self, screen_size, matrix, pngs):
       
        self.screen = pygame.display.set_mode(screen_size)
        self.screen.fill(pygame.Color('black'))
        self.pngs = pngs
        self.matrix = matrix 
        self.screen_size = screen_size
        pygame.display.update() 

    def draw(self):
        self.screen.fill((20,20,20))
        for i in xrange(0,self.matrix.coordinates.size/2):
            x = self.matrix.coordinates[i,0] * self.screen_size[0]
            y = self.matrix.coordinates[i,1] * self.screen_size[1]
            self.screen.blit(self.pngs[0],(x,y))
        pygame.display.update()



def main(): 
    png_0 = pygame.image.load('triangle.png')
    pngs = [png_0]

    pygame.init()
    clock = pygame.time.Clock() 
    screen_size = (1920, 1080)

    frame_rate = 60

    node_density = 50

    # Here the initial matrix of nodes is created
    initial_matrix = np.random.rand(node_density,2) # * 2 - 1 
  
    matrix = Matrix(screen_size, initial_matrix)
    view = View(screen_size, matrix, pngs)


    while True:
        
        
        matrix.vibration()
        view.draw()
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return None



if __name__ == '__main__': main() 
