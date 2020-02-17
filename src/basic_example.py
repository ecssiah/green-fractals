import numpy as np
from generate import Generator


def rotate_xform(alpha, beta, gamma):
    '''Returns an array representing a rotation by three Euler angles'''
    yaw = np.array([
        [np.cos(alpha), -np.sin(alpha), 0],
        [np.sin(alpha),  np.cos(alpha), 0],
        [0            ,  0            , 1]
    ])
    pitch = np.array([
        [ np.cos(beta), 0, np.sin(beta)],
        [ 0           , 1, 0           ],
        [-np.sin(beta), 0, np.cos(beta)]
    ])
    roll = np.array([
        [1, 0            ,  0            ],
        [0, np.cos(gamma), -np.sin(gamma)],
        [0, np.sin(gamma),  np.cos(gamma)]
    ])

    return np.dot(yaw, np.dot(pitch, roll))


def basic_example():
    '''Produces an example Green's fractal animation'''
    params = np.array([[1.0, 1.0, 1.0]]).T
    xform = rotate_xform(2 * np.pi / 128, 2 * np.pi / 128, 0)

    generator = Generator(params, xform)
    generator.calc_frames(1)
    generator.generate_images()


if __name__ == '__main__':
    basic_example()
