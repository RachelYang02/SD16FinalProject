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
        self.node_matrix() 

    def node_matrix(self):  
        # self.nodes = numpy.random.rand(self.density,2) * 2 - 1
        self.nodes = initial_matrix

        return self.nodes 

    def __str__(self): 
        return 'nodes: {}'.format(self.nodes)

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
        self.density = density
        self.screen_size = screen_size
        pygame.display.update() 

    def draw(self):
        circle_png = pygame.image.load('circle.png')
        self.screen.blit(circle_png,(900,900))
        self.screen.fill((20, 20, 20))
        for i in range(0,self.density): # index through each item of the array
            node = self.matrix.nodes[i]
            node_x = node[0] * self.screen_size[0]
            node_y = node[1] * self.screen_size[1]
            self.screen.blit(circle_png,(node_x, node_y)), # each item is a set of coordinates->place circle 
        print self.matrix.nodes

        pygame.display.update() 
        

def main(): 

    pygame.init()
    clock = pygame.time.Clock() 
    screen_size = (1920, 1800)

    frame_rate = 60
    screen = pygame.display.set_mode(screen_size)

    node_denisty = 10

    # Here the initial matrix of nodes is created
    initial_matrix = numpy.random.rand(node_denisty,2)
    global initial_matrix

    model = Model(screen_size)
    matrix = Matrix(node_denisty)
    view = View(node_denisty, screen_size, model, matrix)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        matrix.update()
        model.update()
        view.draw()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__': main() 
