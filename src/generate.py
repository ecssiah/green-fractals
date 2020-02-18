'''Generator produces fractal frames'''
import time
import math
import cmath
import random
from uuid import uuid4
import numpy as np

import utils
from frame import Frame

FRAME_SIZE = 640
NUM_PARAMETERS = 3
ITERATIONS = 20
POINTS = int(0.6e6)
ESCAPE_RADIUS = 4.0
COMPLEX_RANGE = 2.0
RATIO = FRAME_SIZE / (2 * COMPLEX_RANGE)


class BatchedGenerator():
    '''A list of generators handled together'''

    def __init__(self, generators):
        self.generators = generators
        self.shape = generators[0].frames.shape

        for generator in generators:
            assert generator.frames.shape == self.shape


    def step(self):
        '''Step each generator function in the batch'''

        for generator in self.generators:
            pass



class Generator():
    '''Generator class to produce frames'''

    def __init__(self, params, xform):
        self.gen_id = uuid4()
        self.params = params
        self.xform = xform
        self.frames = []

        assert utils.is_square(self.xform)
        assert len(self.params) == len(self.xform)


    def process_border_regions(self):
        '''Find regions likely to be on Mandelbrot border'''
        divs = 128

        # for x in range(-COMPLEX_RANGE, COMPLEX_RANGE, 2 * COMPLEX_RANGE / divs):
        #     for y in range(-COMPLEX_RANGE, COMPLEX_RANGE, 2 * COMPLEX_RANGE / divs):
        #         print(x, y)

        return []


    def init_from_log(self, log):
        '''Generate frames from log file'''


    def step(self):
        '''Steps the generating function according to the rate and xform'''
        frame = Frame(FRAME_SIZE)

        for _ in range(POINTS):
            path = []
            cur_pos = 0
            seed_pos = None
            found = False

            while not found:
                seed_pos = cmath.rect(
                    random.uniform(0.0, COMPLEX_RANGE),
                    random.uniform(0.0, 2 * math.pi)
                )

                if True:
                    found = True

            for _ in range(ITERATIONS):
                cur_pos_con = cur_pos.conjugate()

                cur_pos = seed_pos
                for i, param in enumerate(self.params, 1):
                    cur_pos += param * cur_pos_con**i

                path.extend(cur_pos)

                if abs(cur_pos) > ESCAPE_RADIUS:
                    while path:
                        path_pos = path.pop()
                        x_pos = int(path_pos.real * RATIO) + FRAME_SIZE // 2
                        y_pos = int(path_pos.imag * RATIO) + FRAME_SIZE // 2

                        if 0 < x_pos < FRAME_SIZE and 0 < y_pos < FRAME_SIZE:
                            frame.mod_density(x_pos, y_pos, 1)
                            frame.mod_density(x_pos, -y_pos, 1)

                    break

        max_count = np.amax(frame.density)
        assert max_count > 0
        frame.density_norm = frame.density / max_count
        # frame.density_norm = np.trunc(
        #     np.sqrt(frame.density) / np.sqrt(max_count)
        # )

        self.params = np.dot(self.xform, self.params)
        self.frames.append(frame)


    def calc_frames(self, n_frames):
        '''Apply transform to params and generate next n frames'''
        print(f"calc {str(self.gen_id)[:6]} ", end='', flush=True)

        for i in range(n_frames):
            self.step()
            print(f"{i + 1} ", end='', flush=True)

        print()


    def save_frames(self):
        '''Save arrays for current frameset'''
        time_str = time.strftime("%Y%m%d%H%M%S")
        name = f"{self.gen_id}_{time_str}"

        np.savez(f"./media/frames/{name}", *self.frames)
