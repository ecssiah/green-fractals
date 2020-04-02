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

    divs = 256
    num_frames = divs + 1
    angle = 2 * math.pi / divs

    xform1 = utils.rotate_xform(-angle, angle, angle)
    xform2 = utils.rotate_xform(angle, -angle, angle)
    xform3 = utils.rotate_xform(angle, angle, -angle)

    generator1 = generate.Generator(params1, xform1)
    generator1.calc_frames(num_frames)

    generator2 = generate.Generator(params2, xform2)
    generator2.calc_frames(num_frames)

    generator3 = generate.Generator(params3, xform3)
    generator3.calc_frames(num_frames)

    for frame_num in range(num_frames):
        out_img = image.frames2image(
            generator1.frames[frame_num], 
            generator2.frames[frame_num], 
            generator3.frames[frame_num]
        )

        image_id = uuid4()
        time_str = time.strftime("%Y%m%d%H%M%S")
        name = f"{image_id}_{time_str}_frame{frame_num:03}.png"

        out_img.save(f"./media/imgs/{name}.png")


if __name__ == '__main__':
    basic_example()
