import sys, os, random, math
import pygame
from pygame.locals import *
import numpy as np
import scipy
from colorTrack import Tracker
from threading import Thread


class Model(object):
	'''The model class will contain functions of interactions between the different classes,
	how the different Creatures and Schools interact with wach other and respond to outside 
	stimuli.'''

	def __init__(self, screen_size, tracker, creatureNum = 5, forceConstant = 100):
		self.creature_list = []
		color = pygame.Color('green')
		self.creatureNum = creatureNum
		self.tracker = tracker
		self.screen_size = screen_size


		for i in xrange(creatureNum):
			vx = random.randint(0,1)
			vy = random.randint(0,1)
			self.creature_list.append(Creature(i*30+300, i*30+300, vx, vy, color))
		self.forceConstant = forceConstant
		self.school = School()
		#self.mouse_pos = Controller.mouse_pos

	def forces(self, creature1, creature2):
		'''the distance vectore between the two fish. Vector from creature1 to creature 2'''
		xdist = creature1.x - creature2.x
		ydist = creature1.y - creature2.y
		displacement = math.sqrt(xdist**2 + ydist**2)


		if displacement == 0:                #cannot divide by zero
			displacement = 0.0001
		force = creature1.mass * creature2.mass / (displacement **2)

		#attraction force zone
		xForce = (xdist/displacement)*force
		yForce = (ydist/displacement)*force

		#orientation zone
		if displacement < max([creature1.repulsion_r, creature2.repulsion_r]) and displacement > min([creature1.orientation_r, creature2.orientation_r]):
			#averages the velocities of the creatures so that they move in the same direction
			xForce = (creature1.vx + creature2.vx)/2
			yForce = (creature1.vy + creature2.vy)/2


		#repulsion force zone
		if displacement < max([creature1.orientation_r, creature2.orientation_r]):
			#force reverses if goes below this range
			xForce *= -1
			yForce *= -1

		#update the velocities
		creature1.vx -= int(xForce)
		creature1.vy -= int(yForce)

		creature2.vx += int(xForce)
		creature2.vy += int(yForce)


	def school_force(self, creature1, school):
		#the school has a center which the fish follow

		xdist = creature1.x - school.x
		ydist = creature1.y - school.y
		displacement = math.sqrt(xdist**2 + ydist**2)
		if displacement == 0:
			displacement == 0.0001

		force = creature1.mass * school.mass/ (displacement**2)
		xForce = (xdist/displacement)*force
		yForce = (ydist/displacement)*force

		creature1.vx -= int(xForce)
		creature1.vy -= int(yForce)



	def tracker_force(self, creature):
	#The force between the tracked object and a fishy

		xlocation = self.tracker.center[0]  
		ylocation = self.tracker.center[1]

		xdist = creature.x - xlocation
		ydist = creature.y - ylocation
		displacement = math.sqrt(xdist**2 + ydist**2)


		if xdist == 0 or ydist == 0:                #cannot divide by zero
			xdist = 0.0001
			ydist = 0.0001
		xForce = creature.mass  / ((xdist) * 10000)
		yForce = creature.mass  / ((ydist) * 10000)


		creature.vx += int(xForce)
		creature.vy += int(yForce)

	def __str__(self):
		pass


	def update(self):
		for creature1 in self.creature_list:
			#self.school_force(creature1, self.school)
			for creature2 in self.creature_list:
				if not creature1 is creature2:
					self.forces(creature1, creature2)
			if creature1.x <= 0 or creature1.x >= self.screen_size[0]:
				creature1.vx *= -1
			if creature1.y <= 0 or creature1.y >= self.screen_size[1]:
				creature1.vy *= -1

			self.tracker_force(creature1)

		for creature in self.creature_list:
			print creature
			creature.update()
		print self.school
		self.school.update



class School(object):
	def __init__(self, x = 1920/2, y = 1080/2, vx = 0, vy = 0, r = 100):
		'''A school is made up of many creatures. Each of the creatures both attract and 
		repel the other creatures in their school.'''
		self.x, self.y, self.r = x, y, r
		self.vx, self.vy = vx, vy
		self.mass = 100
		self.boundary = 2 * math.pi * r**2  #current boundary of the school is a circle. I don't think this should be a very strict boundary
		creature_positions = []
		#self.creature_list = model.creature_list

	def update(self):
		self.move()

	def move(self):
		self.x += vx
		self.y += vy

	def __str__(self):
		return 'school position {}, {}'.format(self.x, self.y)


class Creature(pygame.sprite.Sprite):
	def __init__(self, x, y, vx, vy, color, mass = 5, r = 20):
		'''Creatures are currently represented by dots. Each creature belongs to a school. 
		A creature can attract and repel other creatures of a school. There are different 
		radii and magnitudes for attraction, repulsion, and orientation.'''
		self.x, self.y, self.mass, self.r = x, y, mass, r
		self.vx, self.vy = vx, vy
		self.color = color

		self.attraction_r = self.r + 200  #numbers for these are not final and will most likely be changed
		self.orientation_r = self.r + 150
		self.repulsion_r = self.r + 5
		self.attraction_weight = 1.5   #weights will be used in calculating angular direction
		self.repulsion_weight = 0.7
		#self.rect = pygame.Rect(x-r/math.sqrt(2), y-r/math.sqrt(2), 2*r/math.sqrt(2), 2*r/math.sqrt(2))

		pygame.sprite.Sprite.__init__(self)
	# def accelerate(self, force, force_angle):
	# 	self.vx += force*math.cos(force_angle)
	# 	self.vy += force*math.sin(force_angle)

	def update(self):
		self.move()
		#self.rect.centerx, self.rect.centery = self.x, self.y

	def move(self):
		if self.vx > 5:
			self.x += 5
		if self.vy > 5:
			self.y += 5
		else:
			self.x += self.vx
			self.y += self.vy

	def __str__(self):
		return 'creature position {},{}, {}, {}'.format(self.x, self.y, self.vx, self.vy)



class View(object):
	'''The View class is the visual representation of the model.'''
	def __init__(self, screen_size, model):
		# set screen size to bigger display--allow more space for school to move
		self.screen = pygame.display.set_mode((1920,1080))

		# need to blit two different versions of the background image
		self.back1 = pygame.image.load('back.png')
		self.back2 = pygame.image.load('back.png')

		# initial positions of two images are either 0 or width of first image
		self.back1_x = 0
		self.back2_x = self.back1.get_width()

	def update(self, model):
		# display images to screen
		self.screen.blit(self.back1, (self.back1_x,0))
		self.screen.blit(self.back2, (self.back2_x,0))

		# add school to image
		for creature in model.creature_list:
			pygame.draw.circle(self.screen, pygame.Color('red'), (creature.x, creature.y), creature.attraction_r)
			pygame.draw.circle(self.screen, pygame.Color('blue'), (creature.x, creature.y), creature.orientation_r) 
			pygame.draw.circle(self.screen, creature.color, (creature.x, creature.y), creature.r)
		
		pygame.display.update()

		# update image positions to create "animated" feel
		self.back1_x -= 1
		self.back2_x -= 1

		# allows images to stream continuously
		if self.back1_x == -1 * self.back1.get_width():
			self.back1_x = self.back2_x + self.back2.get_width()
		if self.back2_x == -1 * self.back2.get_width():
			self.back2_x = self.back1_x + self.back1.get_width()


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
	"""Runs our game loop and our tracking loop"""

	pygame.init()

	# initializing the clock to limit the rate our code runs at
	clock = pygame.time.Clock()

	# What the user can see
	screen_size = (1920, 1080) #pygame.display.list_modes()[0]

	# boundaries that the creatures have to be within
	world_size = (2120, 1280)
	
	# initializes the color tracker
	tracka = Tracker()

	# initialize our model
	model = Model(screen_size, tracka)
	
	# this manages how we see things
	view = View(screen_size, model)

	# The game loop is in a seperate funciton so we can thread
	def runLoop():
		running = True
		while running:
			model.update()
			view.update(model)
			clock.tick(20)
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()

	t1 = Thread(target = tracka.track)
	t2 = Thread(target = runLoop)

	t1.start()
	t2.start()

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
