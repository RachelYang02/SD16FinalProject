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
    
    def __init__(self, screen_size, position_matrix, theta_matrix_CW, theta_matrix_CCW, direction = True):

        # For Points 
        self.coordinates = position_matrix # our house for all of our positions
        self.x_matrix = position_matrix[:,[0]] # this extracts the 1st column of the inital matrix (x values)
        self.y_matrix = position_matrix[:,[1]] # this extracts the 2nd column of the inital matrix (y values)
        self.screen_size = screen_size
        self.direction = direction
        self.r = np.sqrt(self.x_matrix**2 + self.y_matrix**2) 
        self.theta = np.arctan2(self.y_matrix,self.x_matrix)
        self.trans = (np.random.rand(self.coordinates.size/2,2) * 2 - 1 ) * 1000  # self.trans = np.zeros((self.coordinates.size/2,2)) - 0.002

        # For Triangles
        self.radius = [100,100,100]
        self.theta_matrix_CW = theta_matrix_CW
        self.theta_matrix_CCW = theta_matrix_CCW
        self.theta_matrix_CW_inner = theta_matrix_CW
        self.theta_matrix_CCW_inner = theta_matrix_CCW
        self.theta_matrix_CW_innermost = theta_matrix_CW
        self.theta_matrix_CCW_innermost = theta_matrix_CCW

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

    def rotation(self): 
        # Outer Triangles 
        rotation_speed = 3
        self.theta_matrix_CW = np.add(self.theta_matrix_CW, np.pi*rotation_speed/180) # add to every corner of triangle
        self.theta_matrix_CCW = np.add(self.theta_matrix_CCW, -np.pi*rotation_speed/180) # subtract from every corner of triangle
        
        # Inner Triangles 
        faster = 6
        self.theta_matrix_CW_inner  = np.add(self.theta_matrix_CW_inner,   np.pi*(rotation_speed+faster)/180) # add to every corner of triangle
        self.theta_matrix_CCW_inner = np.add(self.theta_matrix_CCW_inner, -np.pi*(rotation_speed+faster)/180) # subtract from every corner of triangle

        # Innermost Triangles 
        fastest = 9
        self.theta_matrix_CW_innermost  = np.add(self.theta_matrix_CW_innermost,   np.pi*(rotation_speed+fastest)/180) # add to every corner of triangle
        self.theta_matrix_CCW_innermost = np.add(self.theta_matrix_CCW_innermost, -np.pi*(rotation_speed+fastest)/180) # subtract from every corner of triangle

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

        center_x = self.screen_size[0]/2
        center_y = self.screen_size[1]/2

        # This makes multiple circles that expand outwards
        for i in xrange(0,self.matrix.coordinates.size/2):
            for div in range(1,12):
                scale = 600/div
                x = self.matrix.coordinates[i,0] * scale + center_x 
                y = self.matrix.coordinates[i,1] * scale + center_y 
                self.screen.blit(self.pngs[0],(x,y))

        print self.matrix.theta_matrix_CW
        # This rotates three triangles CW
        # BIG
        xs0 = (self.matrix.radius * np.cos(self.matrix.theta_matrix_CW)) + center_x  
        ys0 = (self.matrix.radius * np.sin(self.matrix.theta_matrix_CW)) + center_y 
        # MEDIUM
        xs2 = ((np.add(self.matrix.radius,-50)) * np.cos(np.add(self.matrix.theta_matrix_CW_inner,np.pi/3))) + center_x  
        ys2 = ((np.add(self.matrix.radius,-50)) * np.sin(np.add(self.matrix.theta_matrix_CW_inner,np.pi/3))) + center_y 
        # SMALL
        xs4 = ((np.add(self.matrix.radius,-75)) * np.cos(np.add(self.matrix.theta_matrix_CW_innermost,np.pi*2/3))) + center_x  
        ys4 = ((np.add(self.matrix.radius,-75)) * np.sin(np.add(self.matrix.theta_matrix_CW_innermost,np.pi*2/3))) + center_y 
        
        # This rotates three triangles CCW
        # BIG
        xs1 = (self.matrix.radius * np.cos(self.matrix.theta_matrix_CCW)) + center_x  
        ys1 = (self.matrix.radius * np.sin(self.matrix.theta_matrix_CCW)) + center_y 
        # MEDIUM
        xs3 = ((np.add(self.matrix.radius,-50)) * np.cos(np.add(self.matrix.theta_matrix_CCW_inner,np.pi/3))) + center_x  
        ys3 = ((np.add(self.matrix.radius,-50)) * np.sin(np.add(self.matrix.theta_matrix_CCW_inner,np.pi/3))) + center_y 
        # SMALL 
        xs5 = ((np.add(self.matrix.radius,-75)) * np.cos(np.add(self.matrix.theta_matrix_CCW_inner,np.pi*2/3))) + center_x  
        ys5 = ((np.add(self.matrix.radius,-75)) * np.sin(np.add(self.matrix.theta_matrix_CCW_inner,np.pi*2/3))) + center_y 
 
        points_list0 = [xs0[0],ys0[0]],[xs0[1],ys0[1]],[xs0[2],ys0[2]]
        points_list1 = [xs1[0],ys1[0]],[xs1[1],ys1[1]],[xs1[2],ys1[2]]
        points_list2 = [xs2[0],ys2[0]],[xs2[1],ys2[1]],[xs2[2],ys2[2]]
        points_list3 = [xs3[0],ys3[0]],[xs3[1],ys3[1]],[xs3[2],ys3[2]]
        points_list4 = [xs4[0],ys4[0]],[xs4[1],ys4[1]],[xs4[2],ys4[2]]
        points_list5 = [xs5[0],ys5[0]],[xs5[1],ys5[1]],[xs5[2],ys5[2]]

        pygame.gfxdraw.aapolygon(self.screen,points_list0,(100,15,100)) 
        pygame.gfxdraw.aapolygon(self.screen,points_list1,(100,15,100))
        pygame.gfxdraw.aapolygon(self.screen,points_list2,(100,15,100)) 
        pygame.gfxdraw.aapolygon(self.screen,points_list3,(100,15,100))
        pygame.gfxdraw.aapolygon(self.screen,points_list4,(100,15,100))
        pygame.gfxdraw.aapolygon(self.screen,points_list5,(100,15,100))


        pygame.display.update()

def main(): 
    # png_0 = pygame.image.load('circle.png')
    png_1 = pygame.image.load('circle1.png')
    png_2 = pygame.image.load('triangles.png')
    pngs = [png_1,png_2]

    pygame.init()
    clock = pygame.time.Clock() 
    screen_size = (1920, 1080)

    frame_rate = 100

    node_density = 50

    # Here the initial matrix of nodes is created
    initial_matrix = np.array([1, 0])

    # Here the initial matrix for the triangles is created 
    # Six triangles total, 3 CW, 3CCW 
    initial_theta_matrix_CW = np.array([0, np.pi*2/3, np.pi*4/3]) #,[np.pi/3, np.pi, 5*np.pi/3]])
    initial_theta_matrix_CCW = np.array([np.pi, np.pi/3, np.pi*5/3]) 

    for i in range(1, node_density):
        theta = i * 2 * math.pi / node_density
        x = math.cos(theta)
        y = math.sin(theta)
        a = np.array([x,y])
        initial_matrix = np.append(initial_matrix, a)

    initial_matrix = np.resize(initial_matrix, (node_density,2))

    matrix = Matrix(screen_size, initial_matrix, initial_theta_matrix_CW, initial_theta_matrix_CCW)
    view = View(screen_size, matrix, pngs)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        # and if statement dependant on volume that calls expansion 
        matrix.expansion() 
        matrix.rotation() 
        matrix.vibration()
        matrix.expansion() 
        view.draw()
        clock.tick(frame_rate)

    pygame.quit()
    
if __name__ == '__main__': main() 
