import math
import time
from uuid import uuid4
import numpy as np

import image
import utils
import generate


def basic_example():
    '''Produces an example Green's fractal animation'''
    params1 = np.array([[1.0, 1.0, 1.0]]).T
    params2 = np.array([[1.0, 1.0, 1.0]]).T
    params3 = np.array([[1.0, 1.0, 1.0]]).T

    num_frames = 64
    theta_range = 2 * math.pi / 128
    d_theta = theta_range / num_frames

    xform1 = utils.rotate_xform(d_theta, 0, 0)
    xform2 = utils.rotate_xform(0, d_theta, 0)
    xform3 = utils.rotate_xform(0, 0, d_theta)

    generator1 = generate.Generator(params1, xform1)
    generator1.calc_frames(num_frames)

    generator2 = generate.Generator(params2, xform2)
    generator2.calc_frames(num_frames)

    generator3 = generate.Generator(params3, xform3)
    generator3.calc_frames(num_frames)

    image_id = uuid4()
    time_str = time.strftime("%Y%m%d%H%M%S")

    print(f"calc color {str(image_id)[:6]} ", end='', flush=True)

    for frame_num in range(num_frames):
        print(f"{frame_num + 1} ", end='', flush=True)

        out_img = image.frames2image(
            generator1.frames[frame_num], 
            generator2.frames[frame_num], 
            generator3.frames[frame_num]
        )

        name = f"{image_id}_{time_str}_frame_{frame_num:04}"

        out_img.save(f"./media/imgs/{name}.png")

    print()


if __name__ == '__main__':
    basic_example()
