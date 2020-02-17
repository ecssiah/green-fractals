'''Generator produces fractal frames'''
import random
import numpy as np

from frame import Frame

FRAME_SIZE = 1280

NUM_PARAMETERS = 3
ITERATIONS = int(1e2)
POINTS = int(1e2)
ESCAPE_RADIUS = 3.0
REAL_RANGE, COMP_RANGE = 4.0, 4.0
REAL_RATIO, COMP_RATIO = FRAME_SIZE / REAL_RANGE, FRAME_SIZE / COMP_RANGE


class Generator():
    '''Generator class to produce frames'''

    def __init__(self, params, xform, xform_rate=1.0):
        self.params = params
        self.xform = xform
        self.xform_rate = xform_rate

        self.frames = []

        self.num_params = len(params[0])

        assert len(self.xform) == len(self.xform[0])
        assert self.num_params == len(self.xform)


    def step(self):
        frame = Frame(FRAME_SIZE)

        for _ in range(POINTS):
            z = 0
            path = []
            seed_point = complex(
                random.uniform(-COMP_RANGE, COMP_RANGE),
                random.uniform(-COMP_RANGE, COMP_RANGE)
            )

            for _ in range(ITERATIONS):
                w = z.conjugate()

                if abs(z) > ESCAPE_RADIUS:
                    while path:
                        x = int(path.pop() * REAL_RATIO) + FRAME_SIZE // 2
                        y = int(path.pop() * COMP_RATIO) + FRAME_SIZE // 2

                        if 0 < x < FRAME_SIZE and 0 < y < FRAME_SIZE:
                            frame.density[x][y] += 1

            self.params = np.dot(self.xform_rate * self.xform, self.params)

        return frame


    def next(self, n=1):
        '''Apply transform to params and generate next n frames'''

        for i in range(n):
            self.frames.append(self.step())

        print(self.frames)







