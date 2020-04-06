'''Imaging module for generators'''
from uuid import uuid4
from PIL import Image

import generate


def frame2image(frame):
    '''Produce a monocolor image from a frame'''

    img = Image.new(
        'RGB', (generate.FRAME_SIZE, generate.FRAME_SIZE), (0, 0, 0)
    )

    for x in range(generate.FRAME_SIZE):
        for y in range(generate.FRAME_SIZE):
            intensity = int(255 * frame.density_norm[x, y])
            img.putpixel((x, y), (intensity, intensity, intensity))

    return img


def frames2image(red_frame, green_frame, blue_frame):
    '''Produce a color image from three channel frames'''

    assert len(red_frame) == len(green_frame) == len(blue_frame)

    img = Image.new(
        'RGB', (generate.FRAME_SIZE, generate.FRAME_SIZE), (0, 0, 0)
    )

    for x in range(generate.FRAME_SIZE):
        for y in range(generate.FRAME_SIZE):
            red_intensity = int(255 * red_frame.density_norm[x, y])
            green_intensity = int(255 * green_frame.density_norm[x, y])
            blue_intensity = int(255 * blue_frame.density_norm[x, y])

            img.putpixel(
                (y, x),
                (red_intensity, green_intensity, blue_intensity)
            )

    return img


def generate_color_image(red_generator, green_generator, blue_generator):
    '''Produce a color image from three generators representing color channels'''

    assert (
        len(red_generator.frames) ==
        len(green_generator.frames) ==
        len(blue_generator.frames)
    )

    num_frames = len(red_generator.frames)
    image_id = str(uuid4())[:18]

    print(f"calc frame {str(image_id)[:6]} ", end='', flush=True)

    for frame_num in range(num_frames):
        print(f"{frame_num + 1} ", end='', flush=True)

        out_img = frames2image(
            red_generator.frames[frame_num],
            green_generator.frames[frame_num],
            blue_generator.frames[frame_num]
        )

        name = f"{image_id}_frame_{frame_num:04}"

        out_img.save(f"./media/imgs/{name}.png")

    print()
