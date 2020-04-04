'''Module containing a series of general utilities'''
import numpy as np


def is_square(mat):
    '''Returns True if m is a square matrix'''
    rows = len(mat)
    for row in mat:
        if len(row) != rows:
            return False
    return True


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

    return yaw @ pitch @ roll
    # return np.dot(yaw, np.dot(pitch, roll))
