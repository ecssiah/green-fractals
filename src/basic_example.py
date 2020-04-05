'''Script demonstrating some basic uses of the Green fractal classes'''
import math
import numpy as np

import image
import utils
import generate


def example_img():
    '''Produces a image of a Green fractal'''
    generator = generate.Generator(
        np.array([[1.0, 1.0, 1.0]]).T,
        utils.rotate_xform(0.01, 0.01, 0),
        4
    )


def example_color_img():
    '''Produces a three channel color image of a Green fractal'''
    params1 = np.array([[1.0, 1.0, 1.0]]).T
    params2 = np.array([[1.0, 1.0, 1.0]]).T
    params3 = np.array([[1.0, 1.0, 1.0]]).T

    num_frames = 64
    theta_range = 2 * math.pi / 512
    d_theta = theta_range / num_frames

    xform1 = utils.rotate_xform(d_theta, 0, 0)
    xform2 = utils.rotate_xform(0, d_theta, 0)
    xform3 = utils.rotate_xform(0, 0, d_theta)

    generator1 = generate.Generator(params1, xform1, num_frames)
    generator2 = generate.Generator(params2, xform2, num_frames)
    generator3 = generate.Generator(params3, xform3, num_frames)

    image.generate_color_image(generator1, generator2, generator3)


if __name__ == '__main__':
    example_img()
