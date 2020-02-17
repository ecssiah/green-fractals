'''Generator produces fractal frames'''
import random
from uuid import uuid4
import numpy as np
from PIL import Image

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
        self.id = uuid4()
        self.params = params
        self.xform = xform
        self.xform_rate = xform_rate

        self.frames = []

        assert len(self.xform) == len(self.xform[0])
        assert len(self.params) == len(self.xform)


    def step(self):
        '''Steps the generating function according to the rate and xform'''
        frame = Frame(FRAME_SIZE)

        for _ in range(POINTS):
            z = 0
            path = []
            found = False
            seed_point = None

            while not found:
                # TODO: Filter seeds that are in approximation of mandelbrot set
                #   cardiod: c = e^iθ / 2 − e^2iθ / 4
                #   main disk: c = e^iθ / 4 - 1

                seed_point = complex(
                    random.uniform(-RANGE, RANGE), random.uniform(-RANGE, RANGE)
                )

                # outside_main_disk = (1/4) < abs(seed_point - complex(-1, 0))

                # if outside_main_disk:
                found = True

            for _ in range(ITERATIONS):
                w = z.conjugate()
                z = seed_point

                for i, p in enumerate(self.params, 1):
                    z += p * w**i

                path.extend(z)

                if abs(z) > ESCAPE_RADIUS:
                    while path:
                        z_test = path.pop()
                        x = int(z_test.real * RATIO) + FRAME_SIZE // 2
                        y = int(z_test.imag * RATIO) + FRAME_SIZE // 2

                        if 0 < x < FRAME_SIZE and 0 < y < FRAME_SIZE:
                            frame.inc_density(x, y, 1)
                            # frame.density[x, y] += 1

                    break

        max_count = np.amax(frame.density)

        assert max_count > 0

        frame.density_norm = frame.density / max_count

        self.params = np.dot(self.xform_rate * self.xform, self.params)

        return frame


    def calc_frames(self, n_frames):
        '''Apply transform to params and generate next n frames'''
        print(f"{self.id}:", end='', flush=True)

        for i in range(n_frames):
            self.frames.append(self.step())
            print(f" {i}", end='', flush=True)

        print()
