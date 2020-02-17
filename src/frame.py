import numpy as np


class Frame():
    '''A square snapshot of a Green's fractal'''

    def __init__(self, n):
        density = np.zeros((n, 1))
        rel_density = np.zeros((n, 1))

        print(density)
        print(rel_density)