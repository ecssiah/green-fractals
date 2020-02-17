'''Generator produces fractal frames'''
import numpy as np

ITERATIONS = 1e6
CHANNELS = 3
NUM_PARAMETERS = 3
FRAME_SIZE = 1280
COMPLEX_RANGE = (4.0, 4.0)


class Generator():
    '''Generator class to produce frames'''

    def __init__(
        self,
        seed_params=np.zeros((NUM_PARAMETERS, CHANNELS)),
        xform=np.identity(NUM_PARAMETERS),
        xform_rate=1.0,
    ):
        self.seed_params = seed_params
        self.xform = xform
        self.xform_rate = xform_rate

        assert len(self.seed_params) == len(self.xform) == len(self.xform[0])

        print("seed_params: ", self.seed_params)
        print("xform: ", self.xform)
        print("xform_rate: ", self.xform_rate)


    def step(self):
        self.seed_params = np.dot(self.xform_rate * self.xform, self.seed_params)



    def next(self, n=1):
        '''Apply transform to params and generate next n frames'''
        for ch in range(CHANNELS):
            for i in range(n):
                self.step()
                print(self.seed_params)







