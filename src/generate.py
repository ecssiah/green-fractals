'''Generator produces fractal frames'''
import random
import numpy as np

FRAME_SIZE = 1280

NUM_PARAMETERS = 3
ITERATIONS = 1e2
POINTS = 1e2
ESCAPE_RADIUS = 3.0
REAL_RANGE, COMP_RANGE = (4.0, 4.0), (4.0, 4.0)
REAL_RATIO, IMAG_RATIO = FRAME_SIZE / REAL_RANGE, FRAME_SIZE / COMP_RANGE


class Generator():
    '''Generator class to produce frames'''

    def __init__(
        self,
        params=np.zeros((NUM_PARAMETERS, 1)),
        xform=np.identity(NUM_PARAMETERS),
        xform_rate=1.0,
    ):
        self.params = params
        self.xform = xform
        self.xform_rate = xform_rate

        self.frames = []

        assert len(self.params) == len(self.xform) == len(self.xform[0])

        print("params: ", self.params)
        print("xform: ", self.xform)
        print("xform_rate: ", self.xform_rate)


    def step(self):
        frame = Frame(FRAME_SIZE)

        for _ in range(POINTS):
            z = 0
            path = []
            seed_point = complex(
                random.uniform(-COMP_RANGE[0], COMP_RANGE[0]),
                random.uniform(-COMP_RANGE[1], COMP_RANGE[1])
            )

            for _ in range(ITERATIONS):
                w = z.conjugate()

                if abs(z) > ESCAPE_RADIUS:
                    while path:
                        x = int(path.pop() * REAL_RATIO) + FRAME_SIZE[0] // 2
                        y = int(path.pop() * COMP_RATIO) + FRAME_SIZE[1] // 2

                        if 0 < x FRAME_SIZE[0] and 0 < y < FRAME_SIZE[1]:
                            frame.density[x][y] += 1




        self.params = np.dot(self.xform_rate * self.xform, self.params)


    def next(self, n=1):
        '''Apply transform to params and generate next n frames'''

        for i in range(n):
            self.frames.push(self.step())







