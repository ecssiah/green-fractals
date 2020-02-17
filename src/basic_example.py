from generate import Generator


def basic_example():
    '''Produces an example Green's fractal animation'''
    generator = Generator()
    generator.next(4)


if __name__ == '__main__':
    basic_example()
