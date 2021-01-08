# Conway's A Game of Life
# Oliver Sulyok

from sys import exit
import pygame
import random
import math
import numpy as np


#####################################################################
#####                          TO DO                            #####
#####                   Add Spcaeships!                         #####
#####   Add options to choose your own size/displacement        #####
#####        Add option to draw your own pattern                #####
#####           Add option to choose your own colors            #####
#####################################################################

# Screen definitions and starting postions for some shapes
x_size = 150
y_size = 120
cell_size = 7
x_start = 3
y_start = 3

# Color definitions
color_about_to_die = (179, 179, 255)
color_alive = (255, 255, 255)
color_background = (0, 0, 0)
color_grid = (30, 30, 60)

# Definitions for random shape
m_range = x_size - 2*x_start
n_range = y_size - 2*y_start


# Update states. It follow Conway's rules for game
def update(surface, current, size):
    next_generation = np.zeros((current.shape[0], current.shape[1]))

    for row, col in np.ndindex(current.shape):
        # Calculates number of alive states around particular cell
        number_alive = np.sum(current[row-1:row+2, col-1:col+2]) - current[row, col]

        # Add definitions for rules. 
        if current[row, col] == 1 and number_alive < 2 or number_alive > 3:
            colr = color_about_to_die # Turns cell into dying color.
        # Add comment about states    
        elif (current[row, col] == 1 and 2 <= number_alive <= 3) or (current[row, col] == 0 and number_alive == 3):
            next_generation[row, col] = 1
            colr = color_alive

        colr = colr if current[row, col] == 1 else color_background
        pygame.draw.rect(surface, colr, (col*size, row*size, size-1, size-1))
    
    return next_generation

def glider_cannon(dimx, dimy):
    # The pattern of the glider cannon
    cells = np.zeros((dimy, dimx))
    pattern = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
                        [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]);
    pos = (x_start,y_start)
    cells[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern
    return cells

def blinker(dimx, dimy):
    # The pattern of the blinker
    cells = np.zeros((dimy, dimx))
    pattern = np.array([[0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]);
    pos = (20, 35)
    cells[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern
    return cells

def random_cells(dimx, dimy):
    cells = np.zeros((dimy, dimx))
    pattern = np.random.randint(2, size=(n_range, m_range))
    pos = (x_start, y_start)
    cells[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern
    return cells


def main(dimx, dimy, cellsize):
    pygame.init()
    surface = pygame.display.set_mode((dimx * cellsize, dimy * cellsize))
    pygame.display.set_caption("A Game of Life")

    cells = random_cells(dimx, dimy)
    
    #
    #   Write options for choosing which mode to display using PyGame
    #
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        surface.fill(color_grid)
        cells = update(surface, cells, cellsize)
        pygame.display.update()

if __name__ == "__main__":
    main(x_size, y_size, cell_size)