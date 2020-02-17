import numpy as np


class Frame():
    '''A square snapshot of a Green's fractal'''

    def __init__(self, dim):
        self.dim = dim
        self.density = np.zeros((dim, dim), dtype=int)
        self.density_norm = np.zeros((dim, dim))


    def __str__(self):
        return f"density: {self.density.shape} \nnorm: {self.density_norm.shape}"