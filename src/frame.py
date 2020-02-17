import numpy as np


class Frame():
    '''A square snapshot of a Green's fractal'''

    def __init__(self, dim):
        self.dim = dim
        self.density = np.zeros((dim, dim), dtype=int)
        self.density_norm = np.zeros((dim, dim))


    def inc_density(self, x, y, inc):
        '''Increment the density value at x, y'''
        self.density[x, y] += inc


    def __str__(self):
        return f"density:\n{self.density}\nnorm:\n{self.density_norm}"