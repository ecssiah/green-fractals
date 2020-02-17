import numpy as np


class Frame():
    '''A square snapshot of a Green's fractal'''

    def __init__(self, dim):
        self.dim = dim
        self.density = np.zeros((dim, 1))
        self.rel_density = np.zeros((dim, 1))

        print(self.density)
        print(self.rel_density)