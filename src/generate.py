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
from constants import (
    COMPLEX_RANGE,
    REGIONS_DIM,
    ITERATIONS,
    ESCAPE_RADIUS,
    RANDOM_SEED,
    POINTS,
    FRAME_SIZE,
)


class Border():
    '''A granular representation of a fractal border'''
    def __init__(self, params):
        self.params = params

        print(f"  calc border {params[0, 0]:.4f} {params[1, 0]:.4f} {params[2, 0]:.4f}")

        self.regions = self.init_regions()


    def produce_seed(self):
        '''Returns a seed from one of the border regions'''
        while True:
            seed = cmath.rect(
                random.uniform(0, COMPLEX_RANGE),
                random.uniform(0, 2 * math.pi)
            )

            if self.is_border(seed):
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


class Generator():
    '''Generator class to produce frames'''

    def __init__(self, init_params, xform, num_frames=12):
        random.seed(RANDOM_SEED)

        self.gen_id = str(uuid4())[:18]
        self.xform = xform
        self.num_frames = num_frames
        self.init_params = init_params

        assert utils.is_square(self.xform)
        assert len(self.init_params) == len(self.xform)

        print("calc params")
        self.params = self.gen_params()
        print("calc seeds")
        self.seeds = self.gen_seeds()
        print(f"calc frames {self.gen_id}")
        self.frames = self.gen_frames()


    def init_from_log(self, log):
        '''Generate frames from log file'''


    def gen_params(self):
        '''Calculate params using xform for all frames'''
        params = [self.init_params]

        for i in range(1, self.num_frames):
            params.append(self.xform @ params[i - 1])

        return params


    def gen_seeds(self):
        '''Find suitable complex numbers to serve as seeds'''
        seeds = []

        for frame_num in range(self.num_frames):
            border = Border(self.params[frame_num])
            seeds.append([])

            for _ in range(POINTS):
                seeds[frame_num].append(border.produce_seed())

        return seeds


    def produce_frame(self, frame_num):
        '''Steps the generating function according to the rate and xform'''
        frame = Frame(FRAME_SIZE)

        for i in range(POINTS):
            frame.calc_path(self.seeds[frame_num][i], self.params[frame_num])

        frame.normalize()

        return frame


    def gen_frames(self):
        '''Apply transform to params and generate next n frames'''
        frames = []

        for frame_num in range(self.num_frames):
            frame = self.produce_frame(frame_num)
            frames.append(frame)

            self.process_image(frame_num, frame)

            print(f"{frame_num + 1} ", end='', flush=True)

        print()

        return frames


    def process_image(self, frame_num, frame):
        '''Save the given frame to an image on the disk'''
        img = image.frame2image(frame)

        name = f"{self.gen_id}_frame_{frame_num:04}"
        img.save(f"./media/imgs/{name}.png")


    def save_frames(self):
        '''Save arrays for current frameset'''
        time_str = time.strftime("%Y%m%d%H%M%S")
        name = f"{self.gen_id}_{time_str}"

        np.savez(f"./media/frames/{name}", *self.frames)
