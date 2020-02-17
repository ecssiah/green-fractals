import numpy as np

import image
import utils
import generate


def basic_example():
    '''Produces an example Green's fractal animation'''
    params1 = np.array([[1.0, 0.0, 0.0]]).T
    params2 = np.array([[1.0, 1.0, 0.0]]).T
    params3 = np.array([[1.0, 0.0, 1.0]]).T

    xform1 = utils.rotate_xform(
        2 * np.pi / 128,
        2 * np.pi / 128,
        2 * np.pi / 128,
    )
    xform2 = utils.rotate_xform(
        2 * np.pi / 128,
        2 * np.pi / 128,
        2 * np.pi / 128,
    )
    xform3 = utils.rotate_xform(
        2 * np.pi / 128,
        2 * np.pi / 128,
        2 * np.pi / 128,
    )

    generator1 = generate.Generator(params1, xform1)
    generator1.calc_frames(16)
    generator1.log_frames()
    image.mono_images(generator1)

    generator2 = generate.Generator(params2, xform2)
    generator2.calc_frames(16)
    generator2.log_frames()
    image.mono_images(generator2)

    generator3 = generate.Generator(params3, xform3)
    generator3.calc_frames(16)
    generator3.log_frames()
    image.mono_images(generator3)

    image.color_images(generator1, generator2, generator3)



if __name__ == '__main__':
    basic_example()
