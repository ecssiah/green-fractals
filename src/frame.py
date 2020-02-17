import numpy as np


class Frame():
    '''A square snapshot of a density map'''

    def __init__(self, dim):
        self.dim = dim
        self.density = np.zeros((dim, dim), dtype=int)
        self.density_norm = np.zeros((dim, dim))


    def set_density(self, x, y, value):
        '''Set the density at x, y'''
        self.density[x, y] = value


    def mod_density(self, x, y, inc):
        '''Increment the density at x, y'''
        self.density[x, y] += inc


    def __str__(self):
        return f"density:\n{self.density}\nnorm:\n{self.density_norm}"