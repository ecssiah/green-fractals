'''A square snapshot of a density map called a frame'''
import numpy as np

from constants import ITERATIONS, FRAME_SIZE, ESCAPE_RADIUS, RATIO


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


    def calc_norm(self):
        '''Normalizes the frame data'''
        max_count = np.amax(self.density)
        assert max_count > 0

        self.density_norm = self.density / max_count


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
                    x_pos = int(path_pos.real * RATIO) + FRAME_SIZE // 2
                    y_pos = int(path_pos.imag * RATIO) + FRAME_SIZE // 2

                    if 0 < x_pos < FRAME_SIZE and 0 < y_pos < FRAME_SIZE:
                        self.density[x_pos, y_pos] += 1
                        self.density[x_pos, -y_pos] += 1

                break
