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
ITERATIONS = 40
POINTS = int(0.4e6)
ESCAPE_RADIUS = 2.2
COMPLEX_RANGE = 2.0
RATIO = FRAME_SIZE / (2 * COMPLEX_RANGE)
REGIONS_DIM = 128


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

        self.regions = np.zeros((REGIONS_DIM, REGIONS_DIM), dtype=int)
        self.process_border_regions()

        self.path = []
        self.cur_pos = complex(0, 0)
        self.seed_pos = complex(0, 0)

        assert utils.is_square(self.xform)
        assert len(self.params) == len(self.xform)


    def process_border_regions(self):
        '''Find regions likely to be on Mandelbrot border'''
        spacing = COMPLEX_RANGE / REGIONS_DIM
        escape_map = np.zeros((REGIONS_DIM + 1, REGIONS_DIM + 1), dtype=int)

        for x_pos in range(REGIONS_DIM + 1):
            for y_pos in range(REGIONS_DIM + 1):
                cur_pos = complex(
                    x_pos * spacing - COMPLEX_RANGE / 2,
                    y_pos * spacing - COMPLEX_RANGE / 2,
                )

                for _ in range(ITERATIONS):
                    cur_pos_conj = cur_pos.conjugate()
                    next_pos = cur_pos

                    for idx, param in enumerate(self.params, 1):
                        next_pos += param * cur_pos_conj**idx

                    cur_pos = next_pos

                    if abs(cur_pos) > ESCAPE_RADIUS:
                        escape_map[x_pos, y_pos] = 1
                        break

        for x_pos in range(REGIONS_DIM):
            for y_pos in range(REGIONS_DIM):
                region_sum = (
                    escape_map[x_pos, y_pos] +
                    escape_map[x_pos + 1, y_pos] +
                    escape_map[x_pos, y_pos + 1] +
                    escape_map[x_pos + 1, y_pos + 1]
                )

                if 0 < region_sum < 4:
                    self.regions[x_pos, y_pos] = 1


    def init_from_log(self, log):
        '''Generate frames from log file'''


    def is_border(self, pos):
        '''Rejects ineffective seed points'''
        half_width = COMPLEX_RANGE / 2
        conversion_factor = REGIONS_DIM / COMPLEX_RANGE

        prev_x = conversion_factor * pos.real
        prev_y = conversion_factor * pos.imag

        print(prev_x, prev_y)

        x_pos = math.floor(prev_x + half_width)
        y_pos = math.floor(prev_y + half_width)

        print("orig", pos)
        print("chgd", x_pos, y_pos)

        return self.regions[x_pos, y_pos] == 1


    def iterate_pos(self, pos):
        '''Performs one iteration of the generator function'''
        pos_conj = pos.conjugate()
        next_pos = self.seed_pos

        for idx, param in enumerate(self.params, 1):
            next_pos += param * pos_conj ** idx

        return next_pos


    def step(self):
        '''Steps the generating function according to the rate and xform'''
        frame = Frame(FRAME_SIZE)

        for _ in range(POINTS):
            self.path = []

            is_border_pos = False
            while not is_border_pos:
                self.seed_pos = cmath.rect(
                    random.uniform(0.0, COMPLEX_RANGE),
                    random.uniform(0.0, 2 * math.pi)
                )

                is_border_pos = self.is_border(self.seed_pos)

            for _ in range(ITERATIONS):
                self.cur_pos = self.iterate_pos(self.cur_pos)

                if abs(self.cur_pos) > ESCAPE_RADIUS:
                    while self.path:
                        path_pos = self.path.pop()
                        x_pos = int(path_pos.real * RATIO) + FRAME_SIZE // 2
                        y_pos = int(path_pos.imag * RATIO) + FRAME_SIZE // 2

                        if 0 < x_pos < FRAME_SIZE and 0 < y_pos < FRAME_SIZE:
                            frame.mod_density(x_pos, y_pos, 1)
                            frame.mod_density(x_pos, -y_pos, 1)

                    break

        max_count = np.amax(frame.density)
        assert max_count > 0

        frame.density_norm = frame.density / max_count
        self.frames.append(frame)

        self.params = np.dot(self.xform, self.params)


    def calc_frames(self, n_frames):
        '''Apply transform to params and generate next n frames'''
        print(f"calc {str(self.gen_id)[:6]} ", end='', flush=True)

        for idx in range(n_frames):
            self.step()
            print(f"{idx + 1} ", end='', flush=True)

        print()


    def save_frames(self):
        '''Save arrays for current frameset'''
        time_str = time.strftime("%Y%m%d%H%M%S")
        name = f"{self.gen_id}_{time_str}"

        # Not saving numpy arrays, saving Frames
        np.savez(f"./media/frames/{name}", *self.frames)

        # np.savez(f"./media/frames/{name}_density", )
