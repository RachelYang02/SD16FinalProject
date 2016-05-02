import sys, os, random, math
import pygame
from pygame.locals import *
import time



class Model(object):
	'''The model class will contain functions of interactions between the different classes,
	how the different Creatures and Schools interact with wach other and respond to outside 
	stimuli.'''
	def __init__(self, screen_size):
		color = pygame.Color('green')
		self.creature1 = Creature(100, 100, 5, 5, color)
		self.creature2 = Creature(500, 100, 5, 5, color)
		#self.mouse_pos = Controller.mouse_pos

	def forces(self, creature1, creature2):
		pass
		dx, dy = creature1.x - creature2.x, creature1.y - creature2.y
		distance = math.sqrt(dx**2 + dy**2)
		force = creature1.mass*creature2.mass/(distance**2)
		# force_x = 
		# force_y = 

	def update(self):
		self.creature1.update()
		self.creature2.update()

class School(object):
	def __init__(self, x, y, vx, vy, r):
		'''A school is made up of many creatures. Each of the creatures both attract and 
		repel the other creatures in their school.'''
		self.x, self.y, self.r = x, y, r
		self.vx, self.vy = vx, vy
		self.boundary = 2 * math.pi * r**2  #current boundary of the school is a circle. I don't think this should be a very strict boundary
		creature_positions = []
		self.creature_list = []


	def update(self):
		pass


class Creature(object):
	def __init__(self, x, y, vx, vy, color, mass = 20, r = 20):
		'''Creatures are currently represented by dots. Each creature belongs to a school. 
		A creature can attract and repel other creatures of a school. There are different 
		radii and magnitudes for attraction, repulsion, and orientation.'''
		self.x, self.y, self.mass, self.r = x, y, mass, r
		self.vx, self.vy = vx, vy
		self.color = color

		self.attraction_r = self.r + 10  #numbers for these are not final and will most likely be changed
		self.orientation_r = self.r + 8
		self.repulsion_r = self.r + 6
		self.attraction_weight = 1.5   #weights will be used in calculating angular direction
		self.repulsion_weight = 0.7
		#self.rect = pygame.Rect(x-r/math.sqrt(2), y-r/math.sqrt(2), 2*r/math.sqrt(2), 2*r/math.sqrt(2))

	def accelerate(self, force, force_angle):
		self.vx += force*math.cos(force_angle)
		self.vy += force*math.sin(force_angle)

	def update(self):
		self.move()
		#self.rect.centerx, self.rect.centery = self.x, self.y

	def move(self):
		self.x += self.vx
		self.y += self.vy

	def __str__(self):
		return 'creature position {},{}'.format(self.x, self.y)


class View(object):
	'''The View class is the visual representation of the model.'''
	def __init__(self, screen_size, model):
		self.screen = pygame.display.set_mode(screen_size)
		self.screen.fill(pygame.Color('blue')) 
		pygame.draw.circle(self.screen, model.creature1.color, (model.creature1.x, model.creature1.y), model.creature1.r)
		pygame.draw.circle(self.screen, model.creature2.color, (model.creature2.x, model.creature2.y), model.creature2.r)

		pygame.display.update()

	def update(self, model):
		self.screen.fill(pygame.Color('blue'))
		pygame.draw.circle(self.screen, model.creature1.color, (model.creature1.x, model.creature1.y), model.creature1.r)
		pygame.draw.circle(self.screen, model.creature2.color, (model.creature2.x, model.creature2.y), model.creature2.r)
		pygame.display.update()


class Controller(object):
	'''The Controller class is a stand-in for the Audio/Video classes.''' 
	def __init__(self):
		mouse_pos = pygame.mouse.get_pos()

	def update(self, events, model):
		mouse_pos = pygame.mouse.get_pos()
		mouse_posx = mouse_pos[0]
		mouse_posy = mouse_pos[1]

class Audio(object):
	'''Audio will first be implemented with pressing keys. 
	It will then be changed to make the model update due to the sound input.
	'''
	def __init__(self):
		pass

class Video(object):
	def __init__(self):
		pass


def main():
	pygame.init()
	clock = pygame.time.Clock()
	screen_size = (640, 480) #pygame.display.list_modes()[0]
	model = Model(screen_size)
	controller = Controller()
	view = View(screen_size, model)
	running = True
	i = 0
	while running:
		model.update()
		view.update(model)
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		i += 1
		time.sleep(10000)

if __name__ == '__main__': main()


"""
Things to work on:
+We need to add in:
	+multiple creatures
	+forces between the creatures
	+make school classes/interactions
+Make the fish more complex:
	+make them into multiple circles (from large circle for head to increasingly smaller tail circles)
	+find a way to make the circles move together/look fishy-like in movement 
	+find nice-looking fish colors/transparencies
	+make shapes more complicated instead of circles 
+It would be cool to have a background that looks like shimmery water.
+Integrate across collected data and visual representation
	+Develop the Audio/Video classes for the inputted data
	+Make creatures respond to these inputs
	+Input more types of data for creatures to respond to

"""