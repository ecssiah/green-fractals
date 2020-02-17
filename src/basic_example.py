import numpy as np
from uuid import uuid4
from PIL import Image
import generate


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

    return np.dot(yaw, np.dot(pitch, roll))


def mono_images(gen):
    '''Produce monocolor images for each frame'''
    print(f"{gen.id}:", end='', flush=True)

    for i, frame in enumerate(gen.frames):
        # TODO: use Image.fromarray
        img = Image.new(
            'RGB', (generate.FRAME_SIZE, generate.FRAME_SIZE), (0, 0, 0)
        )

        for x in range(generate.FRAME_SIZE):
            for y in range(generate.FRAME_SIZE):
                intensity = int(255 * frame.density_norm[x, y])
                img.putpixel((y, x), (intensity, intensity, intensity))

        img.save(f"./media/frames/{gen.id}-frame{i}.png")

        print(f" {i}", end='', flush=True)

    print()


def color_images(r_gen, g_gen, b_gen):
    '''Produce color images using the red, green, and blue frames'''
    assert len(r_gen.frames) == len(g_gen.frames) == len(b_gen.frames)

    image_id = uuid4()
    print(f"{image_id}:", end='', flush=True)

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

        img.save(f"./media/frames/{image_id}-frame{i}.png")

        print(f" {i}", end='')


def basic_example():
    '''Produces an example Green's fractal animation'''
    params1 = np.array([[1.0, 1.0, 0.0]]).T
    params2 = np.array([[0.0, 1.0, 1.0]]).T
    params3 = np.array([[1.0, 0.0, 1.0]]).T

    xform = rotate_xform(2 * np.pi / 8, 2 * np.pi / 8, 2 * np.pi / 8)

    generator1 = generate.Generator(params1, xform)
    generator1.calc_frames(4)

    generator2 = generate.Generator(params2, xform)
    generator2.calc_frames(4)

    generator3 = generate.Generator(params3, xform)
    generator3.calc_frames(4)

    mono_images(generator1)
    mono_images(generator2)
    mono_images(generator3)

    color_images(generator1, generator2, generator3)


if __name__ == '__main__':
    basic_example()
