'''Generator produces fractal frames'''
import time
import math
import cmath
import random
from uuid import uuid4
import numpy as np

import utils
import image
from frame import Frame

FRAME_SIZE = 1024
ITERATIONS = 600
POINTS = 100_000
ESCAPE_RADIUS = 2
COMPLEX_RANGE = 2.0
RATIO = FRAME_SIZE / (2 * COMPLEX_RANGE)
REGIONS_DIM = 20
PRODUCE_IMAGES = True

class Viewport():
    '''A rectangular region representing a view'''
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Border():
    '''A granular representation of a fractal border'''
    def __init__(self, params):
        self.params = params
        self.regions = self.init_regions()


    def produce_seed(self):
        '''Returns a seed from one of the border regions'''
        seed = None

        while True:
            seed = cmath.rect(
                random.uniform(0, COMPLEX_RANGE),
                random.uniform(0, 2 * math.pi)
            )

            if self.is_border(seed):
                break

        return seed


    def is_border(self, pos):
        '''Rejects ineffective seed points'''
        half_width = COMPLEX_RANGE / 2
        conversion_factor = REGIONS_DIM / COMPLEX_RANGE

        x_pos = math.floor(conversion_factor * (pos.real + half_width))
        y_pos = math.floor(conversion_factor * (pos.imag + half_width))

        if 0 <= x_pos < REGIONS_DIM and 0 <= y_pos < REGIONS_DIM:
            return self.regions[x_pos, y_pos] == 1

        return False


    def init_regions(self):
        '''Find regions likely to be on Mandelbrot border'''
        regions = np.zeros((REGIONS_DIM, REGIONS_DIM), dtype=int)

        spacing = COMPLEX_RANGE / REGIONS_DIM
        escape_map = np.zeros((REGIONS_DIM + 1, REGIONS_DIM + 1), dtype=int)

        for x_pos in range(REGIONS_DIM + 1):
            for y_pos in range(REGIONS_DIM + 1):
                cur_pos = seed_pos = complex(
                    spacing * x_pos - COMPLEX_RANGE / 2,
                    spacing * y_pos - COMPLEX_RANGE / 2,
                )

                for _ in range(ITERATIONS):
                    pos_conj = cur_pos.conjugate()
                    cur_pos = seed_pos

                    for i in range(len(self.params)):
                        cur_pos += self.params[i, 0] * pos_conj**(i+2)

                    if abs(cur_pos) > ESCAPE_RADIUS:
                        if 0 <= x_pos < REGIONS_DIM and 0 <= y_pos < REGIONS_DIM:
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
                    regions[x_pos, y_pos] = 1

        return regions


    def update_params(self, params):
        '''Calculates new regions based on params input'''
        self.params = params
        self.init_regions()


class Generator():
    '''Generator class to produce frames'''

    def __init__(self, init_params, xform, num_frames=12):
        self.gen_id = uuid4()
        self.xform = xform
        self.num_frames = num_frames
        self.init_params = init_params
        self.viewport = Viewport(0, 0, 1.6, 1.6)

        assert utils.is_square(self.xform)
        assert len(self.init_params) == len(self.xform)

        self.params = self.generate_params()
        self.seeds = self.generate_seeds()

        self.frames = []


    def init_from_log(self, log):
        '''Generate frames from log file'''


    def generate_params(self):
        '''Calculate params using xform for all frames'''
        params = [self.init_params]

        for i in range(1, self.num_frames):
            params.append(self.xform @ params[i - 1])

        return params


    def generate_seeds(self):
        '''Find suitable complex numbers to serve as seeds'''
        seeds = []

        for frame_num in range(self.num_frames):
            border = Border(self.params[frame_num])
            seeds.append([])

            for _ in range(POINTS):
                seeds[frame_num].append(border.produce_seed())

        return seeds


    def calc_escapes(self, frame_num, seed_pos, frame):
        '''Iterates a seed_pos looking for escape'''
        path = []
        cur_pos = seed_pos

        for _ in range(ITERATIONS):
            path.append(cur_pos)
            pos_conj = cur_pos.conjugate()
            cur_pos = seed_pos

            for i in range(len(self.params[frame_num])):
                cur_pos += self.params[frame_num][i, 0] * pos_conj**(i+2)

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


    def step(self, frame_num):
        '''Steps the generating function according to the rate and xform'''
        frame = Frame(FRAME_SIZE)

        for i in range(POINTS):
            self.calc_escapes(frame_num, self.seeds[frame_num][i], frame)

        self.norm_density(frame)

        if PRODUCE_IMAGES:
            self.process_image(frame)


    def calc_frames(self, num_frames):
        '''Apply transform to params and generate next n frames'''
        print(f"calc {str(self.gen_id)[:6]} ", end='', flush=True)

        for frame_num in range(num_frames):
            self.step(frame_num)
            print(f"{frame_num + 1} ", end='', flush=True)

        print()


    def process_image(self, frame):
        '''Save the given frame to an image on the disk'''
        img = image.frame2image(frame)

        name = f"{self.gen_id}_frame_{len(self.frames):04}"
        img.save(f"./media/imgs/{name}.png")


    def save_frames(self):
        '''Save arrays for current frameset'''
        time_str = time.strftime("%Y%m%d%H%M%S")
        name = f"{self.gen_id}_{time_str}"

        # Not saving numpy arrays, saving Frames
        np.savez(f"./media/frames/{name}", *self.frames)

        # np.savez(f"./media/frames/{name}_density", )
