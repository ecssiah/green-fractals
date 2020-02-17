import numpy as np
from generate import Generator


def basic_example():
    '''Produces an example Green's fractal animation'''
    params = np.array([[1, 0, 0]])
    rot_angles = np.array([1e-3, 1e-3, 0.0])
    yaw = np.array([
        [ np.cos(rot_angles[0]), -np.sin(rot_angles[0]), 0],
        [ np.sin(rot_angles[0]),  np.cos(rot_angles[0]), 0],
        [ 0                    ,  0                    , 1]
    ])
    pitch = np.array([
        [ np.cos(rot_angles[1]),  0, np.sin(rot_angles[1])],
        [ 0                    ,  1, 0                    ],
        [-np.sin(rot_angles[1]),  0, np.cos(rot_angles[1])]
    ])
    roll = np.array([
        [ 1, 0                    ,  0                    ],
        [ 0, np.cos(rot_angles[2]), -np.sin(rot_angles[2])],
        [ 0, np.sin(rot_angles[2]),  np.cos(rot_angles[2])]
    ])

    xform = np.dot(yaw, np.dot(pitch, roll))

    print("params: ", params)
    print("xform: ", xform)

    generator = Generator(params, xform)
    generator.next(4)


if __name__ == '__main__':
    basic_example()
