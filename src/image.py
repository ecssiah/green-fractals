'''Imaging module for generators'''
import time
import numpy as np
from uuid import uuid4
from PIL import Image

import utils
import generate


def mono_images(gen):
    '''Produce monocolor images for each frame'''
    print(f"imag {utils.trunc(str(gen.id))} ", end='', flush=True)

    time_str = time.strftime("%Y%m%d-%H%M%S")
    name = f"{gen.id}_{time_str}"

    for i, frame in enumerate(gen.frames):
        # TODO: use Image.fromarray
        img = Image.new(
            'RGB', (generate.FRAME_SIZE, generate.FRAME_SIZE), (0, 0, 0)
        )

        for x in range(generate.FRAME_SIZE):
            for y in range(generate.FRAME_SIZE):
                intensity = int(255 * frame.density_norm[x, y])
                img.putpixel((y, x), (intensity, intensity, intensity))

        img.save(f"./media/frames/{name}_frame{i}.png")

        print(f"{i} ", end='', flush=True)

    print()


def color_images(r_gen, g_gen, b_gen):
    '''Produce color images using the red, green, and blue frames'''
    image_id = uuid4()
    print(f"imag {utils.trunc(str(image_id))} ", end='', flush=True)

    assert len(r_gen.frames) == len(g_gen.frames) == len(b_gen.frames)

    time_str = time.strftime("%Y%m%d-%H%M%S")
    name = f"{image_id}_{time_str}"

    for i in range(len(r_gen.frames)):
        # TODO: use Image.fromarray
        img = Image.new(
            'RGB', (generate.FRAME_SIZE, generate.FRAME_SIZE), (0, 0, 0)
        )

        for x in range(generate.FRAME_SIZE):
            for y in range(generate.FRAME_SIZE):
                r = int(255 * r_gen.frames[i].density_norm[x, y])
                g = int(255 * g_gen.frames[i].density_norm[x, y])
                b = int(255 * b_gen.frames[i].density_norm[x, y])

                img.putpixel((y, x), (r, g, b))

        img.save(f"./media/frames/{name}_frame{i}.png")

        print(f"{i} ", end='', flush=True)

