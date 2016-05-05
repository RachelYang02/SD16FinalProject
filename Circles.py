import pygame
from pygame.locals import *
from pygame import gfxdraw
import time
import random
import numpy as np
from numpy import * 
import sys

# TO DO 
# + Make rotation speed relative to something? 
# + Consolodate all of the Triangle code into loops and indexable arrays 

# Current Plan: 
# Circles eminate from center thoughout volume durration 
# Once volume drops below the threshold the circles stop being formed 
# and the ones that are currently in mostion expand and fade away 
# Rotate triangles in center 
# Vibration to be visible (opacities behind cicles)

class Matrix(object):
    ''' Matrix controls all transformations to the two main matricies 
        These matricies are where all graphical movement is defined 
        Postition Matrix is the master matrix that controls all the points in all the rings. 
        Theta Matrix is the master matrix that controls all the angles of all the nested rotating triangles ''' 

    def __init__(self, screen_size, position_matrix, theta_matrix, direction=True):

        # For Points 
        self.coordinates = position_matrix # our house for all of our positions
        self.x_matrix = position_matrix[:,[0]] # this extracts the 1st column of the inital matrix (x values)
        self.y_matrix = position_matrix[:,[1]] # this extracts the 2nd column of the inital matrix (y values)
        self.screen_size = screen_size
        self.direction = direction
        self.r = np.sqrt(self.x_matrix**2 + self.y_matrix**2) 
        self.theta = np.arctan2(self.y_matrix,self.x_matrix)

        # For Triangles
        self.radius = [100,100,100]
        self.theta_CW = theta_matrix[0]
        self.theta_CCW = theta_matrix[1]
        self.theta_CW_inner = theta_matrix[0]
        self.theta_CCW_inner = theta_matrix[1]
        self.theta_CW_innermost = theta_matrix[0]
        self.theta_CCW_innermost = theta_matrix[1]

    def make_cart(self,r,theta):
        ''' Converts r & theta to cart. coord. 
            Returns coordinates to expansion'''  
        self.x_matrix = r * np.cos(theta)
        self.y_matrix = r * np.sin(theta)
        self.coordinates = np.concatenate((self.x_matrix,self.y_matrix), axis=1)
        return self.coordinates

    def expansion(self, loud=True):
        ''' Expands the rings dependent on volume,
            does calc in polar coord (changes r)
            calls make_cart to convert polar to cart
            cart coord for view.draw''' 
        r_step = 0.1 # how quickly the rings expand outwards 

        if loud == False:
            self.r -= r_step * 5 # if Not Loud contract
        else:
            self.r += r_step # else assume Loud and expand 

        self.coordinates = self.make_cart(self.r,self.theta)

    def rotation(self): 
        ''' The triangles are defined in polar cood. Adding radians to the theta 
            of each triangle rotates them at differing speeds.
            The master Theta Matrix is duplicated and transformed into a matrix 
            of r & theta for each nested triangle '''  
        # Outer Triangles 
        rotation_speed = 3
        self.theta_CW = np.add(self.theta_CW, np.pi*rotation_speed/180) # add to every corner of triangle > CLOCKWISE
        self.theta_CCW = np.add(self.theta_CCW, -np.pi*rotation_speed/180) # subtract from every corner of triangle > COUNTER CLOCKWISE
        
        # Inner Triangles 
        faster = 6
        self.theta_CW_inner  = np.add(self.theta_CW_inner,   np.pi*(rotation_speed+faster)/180) 
        self.theta_CCW_inner = np.add(self.theta_CCW_inner, -np.pi*(rotation_speed+faster)/180)
        
        # Innermost Triangles 
        fastest = 9
        self.theta_CW_innermost  = np.add(self.theta_CW_innermost,   np.pi*(rotation_speed+fastest)/180) 
        self.theta_CCW_innermost = np.add(self.theta_CCW_innermost, -np.pi*(rotation_speed+fastest)/180) 

class View(object):
    ''' View loops through with master Position Matrix to create multiple rings
        Number of rings dependent on volume input
        View converts Triangle Matrix to cart coord and scales/offsets the nested triangles
        View.draw calculates and puts everything on screen ''' 

    def __init__(self, screen_size, matrix, index=0, loud=True): 
       
        self.screen = pygame.display.set_mode(screen_size)
        self.screen.fill(pygame.Color('black'))
        self.matrix = matrix 
        self.screen_size = screen_size
        self.index = index
        self.loud = loud 
        pygame.display.update() 

    def draw(self, loud):
        ''' Draw is where the final transformations of the matricies 
            are done before drawing onto screen ''' 
        self.screen.fill((20,20,20))

        center_x = self.screen_size[0]/2
        center_y = self.screen_size[1]/2
        
        if self.loud == True:
            self.index += 1
        else:
            self.index = 0

        # This makes multiple rings that expand outwards
        for i in xrange(0,self.matrix.coordinates.size/2):
            for div in range(1,12):
                scale = 600/div
                x = self.matrix.coordinates[i,0] * scale + center_x 
                y = self.matrix.coordinates[i,1] * scale + center_y 
                pygame.gfxdraw.filled_circle(self.screen,int(x),int(y),1,(70,70,70))

            # This causes expansion and contration 
            if self.index > 0:
                for div in xrange(1,self.index):
                    if self.index % 20:
                        index = self.index/20
                    index = self.index/20
                    scale = index * 240/(div)

                    # need to find radius to determine at what distance we should vanish the dots
                    x = self.matrix.coordinates[i,0] * scale  
                    x_shift = x + self.screen_size[0]/2 
                    y = self.matrix.coordinates[i,1] * scale
                    y_shift = y + self.screen_size[1]/2 

                    radius = math.sqrt(x**2 + y**2)
                    if radius > 500:
                        continue
                    pygame.gfxdraw.filled_circle(self.screen,int(x_shift),int(y_shift),1,(70,70,70))

            else:
                continue

        # This makes the Black Hole 
        pygame.gfxdraw.filled_circle(self.screen,center_x,center_y,100,(20,20,20))

        # This makes multiple nested triangles that rotate 
        # This rotates three triangles CW
        # BIG
        xs0 = (self.matrix.radius * np.cos(self.matrix.theta_CW)) + center_x  # converting from polar to cart coord and moving to center of screen
        ys0 = (self.matrix.radius * np.sin(self.matrix.theta_CW)) + center_y 
        # MEDIUM
        xs1 = ((np.add(self.matrix.radius,-50)) * np.cos(np.add(self.matrix.theta_CW_inner,np.pi/3))) + center_x  # converting to cart, scaling to 50%, and offseting theta from outer triangle by pi/3 
        ys1 = ((np.add(self.matrix.radius,-50)) * np.sin(np.add(self.matrix.theta_CW_inner,np.pi/3))) + center_y 
        # SMALL
        xs2 = ((np.add(self.matrix.radius,-75)) * np.cos(np.add(self.matrix.theta_CW_innermost,np.pi*2/3))) + center_x  # converting, scaling to 25%, and offseting by 2pi/3 
        ys2 = ((np.add(self.matrix.radius,-75)) * np.sin(np.add(self.matrix.theta_CW_innermost,np.pi*2/3))) + center_y 
        
        # This rotates three triangles CCW
        # BIG
        xs3 = (self.matrix.radius * np.cos(self.matrix.theta_CCW)) + center_x  
        ys3 = (self.matrix.radius * np.sin(self.matrix.theta_CCW)) + center_y 
        # MEDIUM
        xs4 = ((np.add(self.matrix.radius,-50)) * np.cos(np.add(self.matrix.theta_CCW_inner,np.pi/3))) + center_x  
        ys4 = ((np.add(self.matrix.radius,-50)) * np.sin(np.add(self.matrix.theta_CCW_inner,np.pi/3))) + center_y 
        # SMALL 
        xs5 = ((np.add(self.matrix.radius,-75)) * np.cos(np.add(self.matrix.theta_CCW_inner,np.pi*2/3))) + center_x  
        ys5 = ((np.add(self.matrix.radius,-75)) * np.sin(np.add(self.matrix.theta_CCW_inner,np.pi*2/3))) + center_y 
        
        points_list = [[xs0,ys0],[xs1,ys1],[xs2,ys2],[xs3,ys3],[xs4,ys4],[xs5,ys5]]
        
        # This draws all the nested triangles 
        for points in points_list: 
            xs = points[0]
            ys = points[1]
            points = [xs[0],ys[0]],[xs[1],ys[1]],[xs[2],ys[2]]
            pygame.gfxdraw.aapolygon(self.screen,points,(100,15,100))

        pygame.display.update()
        return self.index

def main(): 
    pygame.init()
    clock = pygame.time.Clock() 
    screen_size = (1920, 1080)

    frame_rate = 60

    node_density = 50

    # Here the initial matrix of nodes is created
    initial_matrix = np.array([1, 0])

    # Here the initial matrix for the triangles is created [CW, CCW]
    initial_theta_matrix = np.array([[0, np.pi*2/3, np.pi*4/3],[np.pi, np.pi/3, np.pi*5/3]]) 

    for i in range(1, node_density):
        theta = i * 2 * math.pi / node_density
        x = math.cos(theta)
        y = math.sin(theta)
        a = np.array([x,y])
        initial_matrix = np.append(initial_matrix, a)

    initial_matrix = np.resize(initial_matrix, (node_density,2))

    matrix = Matrix(screen_size, initial_matrix, initial_theta_matrix)
    view = View(screen_size, matrix) 

    running = True

    while running:
         #if volume > some number
            #loud = True
            #matrix.expansion(loud = True)
            #view.draw()
        #else:
        #matrix.expansion()
        #matrix.expansion(loud = False)
        #matrix.vibration()
        #view.draw()

        index = view.draw(loud = True)
        if index > 120:
            # print index
            matrix.rotation() 
            matrix.expansion(loud = False)
            view.draw(loud = False)
        else:
            matrix.rotation() 
            matrix.expansion()
            view.draw(loud = True)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # and if statement dependant on volume that calls expansion 
        # matrix.expansion() 
        # matrix.rotation() 
        # # matrix.vibration()
        # # matrix.expansion() 
        # view.draw()
        
        clock.tick(frame_rate)

    pygame.quit()
    
if __name__ == '__main__': main() 
