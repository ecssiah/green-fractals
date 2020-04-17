'''A square snapshot of a density map called a frame'''
import numpy as np

from constants import (
    POINTS,
    ITERATIONS,
    FRAME_SIZE,
    ESCAPE_RADIUS,
)


class Viewport():
    '''A rectangular region representing a view'''
    def __init__(self, x, y, d):
        self.x = x
        self.y = y
        self.d = d


class Frame():
    '''A density map'''

    def __init__(self, dim):
        self.dim = dim
        self.viewport = Viewport(0.0, -0.7, 1.4)
        self.density = np.zeros((dim, dim), dtype=int)
        self.density_norm = np.zeros((dim, dim))


    def __str__(self):
        return f"{self.density}\n{self.density_norm}\n"


    def __len__(self):
        return self.dim


    def normalize(self):
        '''Normalizes the frame data'''
        max_count = np.amax(self.density)
        assert max_count > 0

        self.density_norm = self.density / max_count


    def to_screen_coords(self, c):
        '''Transforms a complex number to screen space tuple'''
        conversion_factor = FRAME_SIZE / self.viewport.d

        return (
            int(conversion_factor * (c.imag - self.viewport.x + self.viewport.d / 2)),
            int(conversion_factor * (c.real - self.viewport.y + self.viewport.d / 2))
        )


    def step(self, seeds, params):
        '''Step the generating function for each point'''
        for i in range(POINTS):
            self.calc_path(seeds[i], params)


    def calc_path(self, seed_pos, params):
        '''Iterates a seed_pos looking for escape paths'''
        path = []
        cur_pos = seed_pos

        for _ in range(ITERATIONS):
            path.append(cur_pos)
            pos_conj = cur_pos.conjugate()
            cur_pos = seed_pos

            for i in range(len(params)):
                cur_pos += params[i, 0] * pos_conj**(i+2)

            if abs(cur_pos) > ESCAPE_RADIUS:
                while path:
                    path_pos = path.pop()
                    top = path_pos.real <= self.viewport.y + self.viewport.d / 2
                    bottom = path_pos.real >= self.viewport.y - self.viewport.d / 2

                    if top and bottom:
                        left1 = path_pos.imag >= self.viewport.x - self.viewport.d / 2
                        right1 = path_pos.imag <= self.viewport.x + self.viewport.d / 2

                        if left1 and right1:
                            pos1 = self.to_screen_coords(path_pos)
                            self.density[pos1[0], pos1[1]] += 1


                        left2 = -path_pos.imag >= self.viewport.x - self.viewport.d / 2
                        right2 = -path_pos.imag <= self.viewport.x + self.viewport.d / 2

                        if left2 and right2:
                            pos2 = self.to_screen_coords(path_pos.conjugate())
                            self.density[pos2[0], pos2[1]] += 1

                break
