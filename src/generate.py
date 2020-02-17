'''Generator produces fractal frames'''
import time
import random
import logging
from uuid import uuid4
import numpy as np

import utils
from frame import Frame

FRAME_SIZE = 1280
NUM_PARAMETERS = 3
ITERATIONS = int(3e1)
POINTS = int(1e6)
ESCAPE_RADIUS = 2.0
RANGE = 2.0
RATIO = FRAME_SIZE / (2 * RANGE)


class Generator():
    '''Generator class to produce frames'''

    def __init__(self, params, xform, xform_rate=1.0):
        self.gen_id = uuid4()
        self.params = params
        self.xform = xform
        self.xform_rate = xform_rate

        self.frames = []

        assert utils.is_square(self.xform)
        assert len(self.params) == len(self.xform)


    def step(self):
        '''Steps the generating function according to the rate and xform'''
        frame = Frame(FRAME_SIZE)

        for _ in range(POINTS):
            path = []
            found = False
            cur_pos = 0
            seed_pos = None

            while not found:
                # TODO: Filter seeds that are in approximation of mandelbrot set
                #   cardiod: c = e^iθ / 2 − e^2iθ / 4
                #   main disk: c = e^iθ / 4 - 1

                seed_pos = complex(
                    random.uniform(-RANGE, RANGE), random.uniform(-RANGE, RANGE)
                )

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
                            frame.mod_density(x_pos,  y_pos, 1)
                            frame.mod_density(x_pos, -y_pos, 1)

                    break

        max_count = np.amax(frame.density)
        assert max_count > 0
        frame.density_norm = frame.density / max_count

        self.params = np.dot(self.xform_rate * self.xform, self.params)

        return frame


    def calc_frames(self, n_frames):
        '''Apply transform to params and generate next n frames'''
        print(f"calc {utils.trunc(str(self.gen_id))} ", end='', flush=True)

        for i in range(1, n_frames + 1):
            self.frames.append(self.step())
            print(f"{i} ", end='', flush=True)

        print()


    def log_frames(self):
        '''Log information about current frameset'''
        time_str = time.strftime("%Y%m%d-%H%M%S")
        name = f"{self.gen_id}_{time_str}"

        logging.basicConfig(filename=f"{name}.", level=logging.INFO)

        for frame in self.frames:
            logging.info("%s", str(frame))

