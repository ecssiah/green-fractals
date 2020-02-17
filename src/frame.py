import numpy as np


class Frame():
    '''A square snapshot of a density map'''

    def __init__(self, dim):
        self.dim = dim
        self.density = np.zeros((dim, dim), dtype=int)
        self.density_norm = np.zeros((dim, dim))


    def mod_density(self, x, y, inc):
        '''Increment the density at x, y'''
        self.density[x, y] += inc


    def __str__(self):
        return f"{self.density}\n{self.density_norm}\n"