import pygame
from pygame.locals import *
import time
import random
import math
import numpy 
from numpy import * 

class Matrix(object): 

    def __init__(self, density):
        color = pygame.Color('white')
        self.nodes = [] 
        self.density = density

    def update(self): 
        print self.nodes
        self.nodes.update

    def node_matrix(self):  
        self.nodes = numpy.random.rand(self.density,2) * 2 - 1

        return self.nodes 

    def __str__(self): 
        nodes = numpy.random.rand(self.density,2) * 2 - 1
        return 'nodes: {}'.format(nodes)

class Model(object):

    def __init__(self, screen):
        color = pygame.Color('white')
        self.screen = screen

    def update(self):
        pass  

class View(object):

    def __init__(self, density, screen_size, model, matrix):
        self.screen = pygame.display.set_mode(screen_size)
        self.screen.fill(pygame.Color('black'))
        self.matrix = matrix 
        pygame.display.update() 

    def draw(self, density, model):
        circle_png = pygame.image.load('circle.png')
        ''' THE ISSUE IS THAT THE MATRIX IS NOT RETURNING AN ARRAY TO MY DRAW FUNCTION '''
        # for x in numpy.nditer(matrix): # index through each item of the array
        #     self.screen.blit(circle_png,(x.T)), # each item is a set of coordinates->place circle 
        self.screen.fill((20, 20, 20))
        pygame.display.update() 
        

def main(): 

    pygame.init()
    clock = pygame.time.Clock() 
    screen_size = (1920, 1800)

    frame_rate = 60
    screen = pygame.display.set_mode(screen_size)

    node_denisty = 10
    model = Model(screen_size)
    matrix = Matrix(node_denisty)
    view = View(node_denisty, screen_size, model, matrix)
    

    print matrix 

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        model.update()
        view.draw(node_denisty, model)
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__': main() 
