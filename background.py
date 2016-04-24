import pygame
from pygame.locals import *
import time
import random
from pygame import gfxdraw


class Point(object): 
    """ creating point class, to determine location of all our stuff 
    """
    def __init__(self, screen_size, x, y):
        self.x = x
        self.y = y

    def pos(self):
        return self.x, self.y

    def update(self):


class Nodes(object):
	def __init__(self,screen_size): 
		self.screen_y = screen_size[1]
		self.screen_x = screen_size[0]
		self.node_list_x = [] 
		self.node_list_y = []

	def matrix(self): 
		self.screen_x/100
		

class View(object): 
	def __init__(self, screen_size, model):
		# set screen size to bigger display--allow more space for school to move
		self.screen = pygame.display.set_mode((1920,1080))
		# fill screen as black
		self.screen.fill(pygame.Color('black'))

	def update(self, model): 
		self.screen.fill(pygame.Color('black'))





if __name__ == '__main__':

    try:
        pygame.quit()
    except:
        pass

    pygame.init()
    frame_rate = 25
    screen_size = (1920, 1800)
    background = pygame.display.set_mode(screen_size)


    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event, model)

        model.update()
        view.draw(model)
        time.sleep(1/frame_rate)

    pygame.quit()