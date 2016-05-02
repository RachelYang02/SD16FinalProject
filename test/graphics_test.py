import pygame
from pygame.locals import *
import time
import random
import numpy as np
from numpy import * 
from colorTrack import Tracker
from audio import Audio
from threading import Thread
import sys


# TO DO 
# + scaling in make_cart for polar conversion after calcuations
# + don't forget to scale back down 


class Matrix(object):
    #does something
    def __init__(self, screen_size, initial_vals, audio, direction = True):
        self.coordinates = initial_vals # our house for all of our positions
        self.screen_size = screen_size
        self.direction = direction
        self.audio = audio
        #self.trans = np.zeros((self.coordinates.size/2,2)) - 0.0002
        self.trans = np.zeros((self.coordinates.size/2,2)) - 0.002

    def remap_interval(self, val,
                       input_interval_start=0,                   
                       input_interval_end=30000,
                       output_interval_start=0,
                       output_interval_end=0.1):
        """ Given an input value in the interval [input_interval_start,
            input_interval_end], return an output value scaled to fall within
            the output interval [output_interval_start, output_interval_end].

            val: the value to remap
            input_interval_start: the start of the interval that contains all
                                  possible values for val
            input_interval_end: the end of the interval that contains all possible
                                values for val
            output_interval_start: the start of the interval that contains all
                                   possible output values
            output_inteval_end: the end of the interval that contains all possible
                                output values
            returns: the value remapped from the input to the output interval
        """
        # return output value scaled to output interval
        input_range = float(input_interval_end - input_interval_start)
        output_range = float(output_interval_end - output_interval_start)
        output_value = ((val - input_interval_start)/input_range) * (output_range) + output_interval_start
        return output_value

    def vibration(self): 
        if self.direction == True:
            remap = self.remap_interval(self.audio.currentVol)
            #print remap
            self.trans += remap

            self.coordinates = np.add(self.coordinates,self.trans)
        
            self.direction = False
        else:
            remap = self.remap_interval(self.audio.currentVol)

            self.trans -= remap
            
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
    screen_size = (1080, 2480)

    frame_rate = 60

    node_density = 50

    # Here the initial matrix of nodes is created
    initial_matrix = np.random.rand(node_density,2) # * 2 - 1 

    #tracka = Tracker()
    #t1 = Thread(target = tracka.track)

    listener = Audio()
    t2 = Thread(target = listener.collectAudio)
  
    matrix = Matrix(screen_size, initial_matrix, listener)
    view = View(screen_size, matrix, pngs)

    def runLoop():
        while True:
            
            
            matrix.vibration()
            view.draw()
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
    t3 = Thread(target = runLoop)


    #t1.start()
    t2.start()
    t3.start()


if __name__ == '__main__': main() 
