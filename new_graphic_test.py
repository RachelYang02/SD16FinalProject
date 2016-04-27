import pygame
from pygame.locals import *
import time
from pygame import math 
import random
import math
import numpy as np
from numpy import * 

# TO DO 
# + scaling in make_cart for polar conversion after calcuations 

class Node(object): 
    ''' Node returns the cart coord that it feeds to View
        Node handles invidual points and their characteristics'''

    def __init__(self,x,y,png): 
        self.png = png
        self.x = x 
        self.y = y

class Matrix(object): 
    ''' Creates cart matrix to feed to Node. 
        Creates polar matrix to feed to Model. 
        Matrix keeps track of all node behavior''' 

    def __init__(self, density, screen_size, matrix, pngs):
        self.matrix = matrix # our house for all of our positions
        self.pngs = pngs # loading list of pngs for nodes 
        self.screen_size = screen_size
        self.xs = matrix[:,[0]] # This extracts the 1st column of the inital matrix (x values)
        self.ys = matrix[:,[1]] # This extracts the 2nd column of the inital matrix (y values)
        self.x = [] # init empty list for make_cart, used in make_n0de
        self.y = [] # init empty list for make_cart, used in make_node 
        self.r = [] # init polar coord array
        self.theta = [] # init polar coord array 
        self.density = density # how many nodes? 
        self.polarNodes = [] # list of polar nodes for calc in Model
        self.cartNodes = [] # list of cart nodes for draw in View 
        self.node_list = [] # list for nodes with png passed to Node

    def make_polar(self): 
        # CONVERT TO POLAR FOR CALC
        # r is 1st column, theta is 2nd 
        self.r = np.sqrt(self.xs**2 + self.ys**2) 
        self.theta = np.arctan2(self.ys,self.xs)
        self.polarNodes = np.concatenate((self.r, self.theta), axis=0)

    def make_cart(self):
        # CONVERT BACK TO CART FOR DRAW 
        # and shift/scale for top left (0,0) & screen size
        self.x = self.r * np.cos(self.theta)
        self.y = self.r * np.sin(self.theta)
        self.cartNodes = np.concatenate((self.x,self.y), axis=0)

    def make_node(self): 
        # Take in result from make_cart and call Node class making a list of nodes for Node 
        # that will then be given to blit to draw in View 
        for index in range(0,self.density): 
            # NEED LATER for update node = matrix.cartNodes[index]
            x = self.x[index] * (self.screen_size[0]) 
            y = self.y[index] * (self.screen_size[1]) 
            self.node_list.append(Node(x,y,self.pngs[0]))

    def update(self):
        # update will update in everthing in the order we want to update it in 
        # be sure that xs and ys are updated for cart and polar (should be find when Model give Matrix the new matrix)
        self.make_polar() 
        self.make_cart()
        self.make_node() 
    
    def __str__(self): 
        return 'matrix {} '.format(self.matrix)

class Model(object): 
    ''' Takes in the polar matrix (and other parameters) and does all the math. 
        Creates new matrix, feeds matrix to Matrix'''

    def __init__(self, density, matrix): 
        self.density = density 
        self.matrix = matrix.matrix
        self.transM = np.random.rand(self.density,2) # transformation matrix for vibration

    def radial_motion(self): 
        pass  

    def vibration(self): 
        self.matrix = np.add(self.matrix,self.transM)

    def update(self): 
        self.vibration()  

    def __str__(self): 
        return 'matrix {} T {}'.format(self.matrix, self.transM)

class View(object):
    ''' '''
    def __init__(self, density, screen_size, matrix):
        self.screen = pygame.display.set_mode(screen_size)
        self.screen.fill(pygame.Color('black'))
        self.matrix = matrix 
        self.nodes = self.matrix.node_list
        self.density = density
        self.screen_size = screen_size
        pygame.display.update() 

    def draw(self):
        
        self.screen.fill((20, 20, 20))
        for node in self.nodes: 
            self.screen.blit(node.png,(node.x, node.y)), # place node 
        pygame.display.update() 
        

def main(): 
    png_0 = pygame.image.load('triangle.png')
    pngs = [png_0]

    pygame.init()
    clock = pygame.time.Clock() 
    screen_size = (1000, 1000)

    frame_rate = 60
    screen = pygame.display.set_mode(screen_size)

    node_density = 50

    # Here the initial matrix of nodes is created
    initial_matrix = np.random.rand(node_density,2) * 2 - 1 
            # initial_matrix = np.random.random_integers(500,1000,size=(50,2))
  
    # node = Node(node_density, screen_size) 
    matrix = Matrix(node_density, screen_size, initial_matrix, pngs)
    view = View(node_density, screen_size, matrix)
    model = Model(node_density, matrix) 

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        matrix.update()
        # print matrix 
        model.update()
        # print model 
        view.draw()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__': main() 
