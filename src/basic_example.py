'''Script demonstrating some basic uses of the Green fractal classes'''
import math
import numpy as np

import image
import utils
import generate


def example_img():
    '''Produces a image of a Green fractal'''
    num_frames = 128
    theta_range = 2 * math.pi / 1
    d_theta = theta_range / num_frames

    params = np.array([[0.0, 1.0, 1.0]]).T

    xform = utils.rotate_xform(d_theta, d_theta, d_theta)

    generate.Generator(params, xform, num_frames)


def example_color_img():
    '''Produces a three channel color image of a Green fractal'''
    num_frames = 64
    theta_range = 2 * math.pi / 512
    d_theta = theta_range / num_frames

    params_r = np.array([[1.0, 1.0, 1.0]]).T
    params_g = np.array([[1.0, 1.0, 1.0]]).T
    params_b = np.array([[1.0, 1.0, 1.0]]).T

    xform_r = utils.rotate_xform(d_theta, 0, 0)
    xform_g = utils.rotate_xform(0, d_theta, 0)
    xform_b = utils.rotate_xform(0, 0, d_theta)

    generator_r = generate.Generator(params_r, xform_r, num_frames)
    generator_g = generate.Generator(params_g, xform_g, num_frames)
    generator_b = generate.Generator(params_b, xform_b, num_frames)

    image.generate_color_image(generator_r, generator_g, generator_b)


if __name__ == '__main__':
    example_img()
