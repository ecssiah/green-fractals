'''A square snapshot of a density map called a frame'''
import numpy as np


class Frame():
    '''A density map'''

    def __init__(self, dim):
        self.dim = dim
        self.density = np.zeros((dim, dim), dtype=int)
        self.density_norm = np.zeros((dim, dim))


    def __str__(self):
        return f"{self.density}\n{self.density_norm}\n"


    def __len__(self):
        return self.dim


    def mod_density(self, x_pos, y_pos, inc):
        '''Increment the density at x_pos, y_pos'''
        self.density[x_pos, y_pos] += inc
