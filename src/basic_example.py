import math
import numpy as np

import image
import utils
import generate


def basic_example():
    '''Produces an example Green's fractal animation'''
    params1 = np.array([[1.0, 0.8, 0.4]]).T
    params2 = np.array([[0.4, 1.0, 0.8]]).T
    params3 = np.array([[0.8, 0.4, 1.0]]).T

    divs = 128

    xform1 = utils.rotate_xform(
        2 * math.pi / divs,
        2 * math.pi / divs,
        2 * math.pi / divs,
    )
    xform2 = utils.rotate_xform(
        2 * math.pi / divs,
        2 * math.pi / divs,
        2 * math.pi / divs,
    )
    xform3 = utils.rotate_xform(
        2 * math.pi / divs,
        2 * math.pi / divs,
        2 * math.pi / divs,
    )

    num_frames = 8

    generator1 = generate.Generator(params1, xform1)
    generator1.calc_frames(num_frames)
    generator1.save_frames()
    image.mono_images(generator1)

    generator2 = generate.Generator(params2, xform2)
    generator2.calc_frames(num_frames)
    generator2.save_frames()
    image.mono_images(generator2)

    generator3 = generate.Generator(params3, xform3)
    generator3.calc_frames(num_frames)
    generator3.save_frames()
    image.mono_images(generator3)

    image.color_images(generator1, generator2, generator3)


if __name__ == '__main__':
    basic_example()
