import pygame
from pygame.locals import *
import time
import random
import numpy as np
from numpy import * 
import sys

# TO DO 
# + Making volume control expansion 
# + Vanishing radius for expansion?
# + Make more png's for small radii? 

# Current Plan: 
# Circles eminate from center thoughout volume durration 
# Once volume drops below the threshold the circles stop being formed 
# and the ones that are currently in mostion expand and fade away 
# Rotate triangles in center 
# Vibration to be visible (opacities behind cicles)


class Matrix(object):
    #does something
    def __init__(self, screen_size, position_matrix, direction = True):
        self.coordinates = position_matrix # our house for all of our positions
        self.x_matrix = position_matrix[:,[0]] # this extracts the 1st column of the inital matrix (x values)
        self.y_matrix = position_matrix[:,[1]] # this extracts the 2nd column of the inital matrix (y values)
        self.screen_size = screen_size
        self.direction = direction
        self.r = np.sqrt(self.x_matrix**2 + self.y_matrix**2) 
        self.theta = np.arctan2(self.y_matrix,self.x_matrix)
        # self.trans = np.zeros((self.coordinates.size/2,2)) - 0.002
        self.trans = (np.random.rand(self.coordinates.size/2,2) * 2 - 1 ) * 1000
        
    def make_cart(self,r,theta):
        self.x_matrix = r * np.cos(theta)
        self.y_matrix = r * np.sin(theta)
        self.coordinates = np.concatenate((self.x_matrix,self.y_matrix), axis=1)
        return self.coordinates

    def expansion(self):
        self.r += .07
        self.coordinates = self.make_cart(self.r,self.theta)

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
            for div in xrange(1,12):
                scale = 240/div
                x = self.matrix.coordinates[i,0] * scale + self.screen_size[0]/2 
                y = self.matrix.coordinates[i,1] * scale + self.screen_size[1]/2 
                self.screen.blit(self.pngs[0],(x,y))

        pygame.display.update()

def main(): 
    png_0 = pygame.image.load('circle.png')
    pngs = [png_0]

    pygame.init()
    clock = pygame.time.Clock() 
    screen_size = (1920, 1080)

    frame_rate = 90

    node_density = 50

    # Here the initial matrix of nodes is created
    initial_matrix = np.array([1, 0])

    for i in range(1, node_density):
        theta = i * 2 * math.pi / node_density
        x = math.cos(theta)
        y = math.sin(theta)
        a = np.array([x,y])
        initial_matrix = np.append(initial_matrix, a)

    initial_matrix = np.resize(initial_matrix, (node_density,2))

    matrix = Matrix(screen_size, initial_matrix)
    view = View(screen_size, matrix, pngs)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        # and if statement dependant on volume that calls expansion 
        matrix.expansion() 
        matrix.vibration()
        matrix.expansion() 
        view.draw()
        clock.tick(frame_rate)

    pygame.quit()
    
if __name__ == '__main__': main() 
