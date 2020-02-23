'''Generator produces fractal frames'''
import time
import math
import cmath
import random
from uuid import uuid4
import numpy as np

import utils
from frame import Frame

FRAME_SIZE = 1280
NUM_PARAMETERS = 3
ITERATIONS = 100
POINTS = int(0.5e5)
ESCAPE_RADIUS = 2.0
COMPLEX_RANGE = 2.0
RATIO = FRAME_SIZE / (2 * COMPLEX_RANGE)
REGIONS_DIM = 16


class Generator():
    '''Generator class to produce frames'''

    def __init__(self, params, xform):
        self.gen_id = uuid4()
        self.params = params
        self.xform = xform
        self.frames = []

        self.regions = np.zeros((REGIONS_DIM, REGIONS_DIM), dtype=int)
        self.process_border_regions()

        assert utils.is_square(self.xform)
        assert len(self.params) == len(self.xform)


    def process_border_regions(self):
        '''Find regions likely to be on Mandelbrot border'''
        spacing = COMPLEX_RANGE / REGIONS_DIM
        escape_map = np.zeros((REGIONS_DIM + 1, REGIONS_DIM + 1), dtype=int)

        for x_pos in range(REGIONS_DIM + 1):
            for y_pos in range(REGIONS_DIM + 1):
                seed_pos = complex(
                    spacing * x_pos - COMPLEX_RANGE / 2,
                    spacing * y_pos - COMPLEX_RANGE / 2,
                )
                cur_pos = seed_pos

                for _ in range(ITERATIONS):
                    pos_conj = cur_pos.conjugate()
                    cur_pos = seed_pos

                    for idx, param in enumerate(self.params, 1):
                        cur_pos += param * pos_conj ** idx

                    if abs(cur_pos) > ESCAPE_RADIUS:
                        escape_map[x_pos, y_pos] = 1
                        break

        num_border_regions = 0

        for x_pos in range(REGIONS_DIM):
            for y_pos in range(REGIONS_DIM):
                region_sum = (
                    escape_map[x_pos, y_pos] +
                    escape_map[x_pos + 1, y_pos] +
                    escape_map[x_pos, y_pos + 1] +
                    escape_map[x_pos + 1, y_pos + 1]
                )

                if 0 < region_sum < 4:
                    num_border_regions += 1
                    self.regions[x_pos, y_pos] = 1

        print(num_border_regions)
        print(self.regions)


    def init_from_log(self, log):
        '''Generate frames from log file'''


    def is_border(self, pos):
        '''Rejects ineffective seed points'''
        half_width = COMPLEX_RANGE / 2
        conversion_factor = REGIONS_DIM / COMPLEX_RANGE

        x_pos = math.trunc(conversion_factor * pos.real + half_width)
        y_pos = math.trunc(conversion_factor * pos.imag + half_width)

        print(x_pos, y_pos)

        return self.regions[x_pos, y_pos] == 1


    def choose_seed(self):
        '''Choose effective seed points'''
        is_border_pos = False
        while not is_border_pos:
            seed_pos = cmath.rect(
                random.uniform(0.0, COMPLEX_RANGE),
                random.uniform(0.0, 2 * math.pi)
            )

            is_border_pos = self.is_border(seed_pos)

        return seed_pos


    def calc_escapes(self, seed_pos, frame):
        '''Iterates a seed_pos looking for escape'''
        path = []
        cur_pos = seed_pos

        for _ in range(ITERATIONS):
            pos_conj = cur_pos.conjugate()
            cur_pos = seed_pos

            for idx, param in enumerate(self.params, 1):
                cur_pos += param * pos_conj ** idx

            if abs(cur_pos) > ESCAPE_RADIUS:
                while path:
                    path_pos = path.pop()
                    x_pos = int(path_pos.real * RATIO) + FRAME_SIZE // 2
                    y_pos = int(path_pos.imag * RATIO) + FRAME_SIZE // 2

                    if 0 < x_pos < FRAME_SIZE and 0 < y_pos < FRAME_SIZE:
                        frame.mod_density(x_pos, y_pos, 1)
                        frame.mod_density(x_pos, -y_pos, 1)

                break


    def norm_density(self, frame):
        '''Normalizes the density map'''
        max_count = np.amax(frame.density)
        assert max_count > 0

        frame.density_norm = frame.density / max_count
        self.frames.append(frame)


    def step(self):
        '''Steps the generating function according to the rate and xform'''
        frame = Frame(FRAME_SIZE)

        for _ in range(POINTS):
            seed_pos = self.choose_seed()
            self.calc_escapes(seed_pos, frame)

        self.norm_density(frame)
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
