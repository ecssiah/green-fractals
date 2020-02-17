import numpy as np
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


def generate_mono_images(frames):
    '''Produce monocolor images for each frame'''
    for i, frame in enumerate(frames):
        print(f"image {i}")

        # TODO: use Image.fromarray
        img = Image.new(
            'RGB', (generate.FRAME_SIZE, generate.FRAME_SIZE), (0, 0, 0)
        )

        for x in range(generate.FRAME_SIZE):
            for y in range(generate.FRAME_SIZE):
                intensity = int(255 * frame.density_norm[x, y])
                img.putpixel((y, x), (intensity, intensity, intensity))

        img.save(f"./media/frames/frame{i}.png")


def  generate_color_images(r_frames, g_frames, b_frames):
    '''Produce color images using the red, green, and blue frames'''

    assert len(r_frames) == len(g_frames) == len(b_frames)

    for i in range(len(r_frames)):
        print(f"image {i}")

        # TODO: use Image.fromarray
        img = Image.new(
            'RGB', (generate.FRAME_SIZE, generate.FRAME_SIZE), (0, 0, 0)
        )

        for x in range(generate.FRAME_SIZE):
            for y in range(generate.FRAME_SIZE):
                r = int(255 * r_frames[i].density_norm[x, y])
                g = int(255 * g_frames[i].density_norm[x, y])
                b = int(255 * b_frames[i].density_norm[x, y])

                img.putpixel((y, x), (r, g, b))

        img.save(f"./media/frames/frame{i}.png")






def basic_example():
    '''Produces an example Green's fractal animation'''
    params1 = np.array([[1.0, 0.0, 0.0]]).T
    params2 = np.array([[0.0, 1.0, 0.0]]).T
    params3 = np.array([[0.0, 0.0, 1.0]]).T

    xform = rotate_xform(2 * np.pi / 4, 2 * np.pi / 4, 0)

    generator1 = generate.Generator(params1, xform)
    generator1.calc_frames(2)

    generator2 = generate.Generator(params2, xform)
    generator2.calc_frames(2)

    generator3 = generate.Generator(params3, xform)
    generator3.calc_frames(2)

    generate_color_images(generator1.frames, generator2.frames, generator3.frames)


if __name__ == '__main__':
    basic_example()
