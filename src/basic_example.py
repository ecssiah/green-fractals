import math
import numpy as np

import image
import utils
import generate


def basic_example():
    '''Produces an example Green's fractal animation'''
    params1 = np.array([[0.6, 1.0, 0.6]]).T
    params2 = np.array([[0.0, 1.0, 1.0]]).T
    params3 = np.array([[1.0, 0.0, 1.0]]).T

    divs = 128
    num_frames = divs + 1
    angle = 2 * math.pi / divs

    xform1 = utils.rotate_xform(-angle, angle, angle)
    xform2 = utils.rotate_xform(angle, -angle, angle)
    xform3 = utils.rotate_xform(angle, angle, -angle)

    generator1 = generate.Generator(params1, xform1)
    generator1.calc_frames(num_frames)
    image.mono_images(generator1)

    generator2 = generate.Generator(params2, xform2)
    generator2.calc_frames(num_frames)
    image.mono_images(generator2)

    generator3 = generate.Generator(params3, xform3)
    generator3.calc_frames(num_frames)
    image.mono_images(generator3)

    image.color_images(generator1, generator2, generator3)


if __name__ == '__main__':
    basic_example()
