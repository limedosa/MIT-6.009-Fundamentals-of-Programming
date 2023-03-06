"""
6.1010 Spring '23 Lab 1: Image Processing 
LD
"""

#!/usr/bin/env python3

import math

from PIL import Image


def get_pixel(image, row, col):
    return image["pixels"][col * image["width"] + row]


def set_pixel(image, row, col, color):
    image["pixels"][col * image["width"] + row] = color


def apply_per_pixel(image, func):
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [0] * len(image["pixels"]),  # CHANGE THIS
    }

    for col in range(image["height"]):
        for row in range(image["width"]):
            color = get_pixel(image, row, col)
            newcolor = func(color)
            set_pixel(result, row, col, newcolor)
    return result


def inverted(image):
    # original function: return apply_per_pixel(image, lambda color: 256-color)
    return apply_per_pixel(image, lambda color: 255 - color)
    # original had  had the wrong number; changed from 256 to 255, also had to change apply)

    # This passes test cases too!!!!
    # inverted_pixels = [255 - pixel for pixel in image["pixels"]]
    # return {
    #     "height": image["height"],
    #     "width": image["width"],
    #     "pixels": inverted_pixels,
    # }


def updatedPixel(image, row, col, new):
    # make test cases for all (wrap, zero, extend,outof bounds)
    width = image["width"]
    height = image["height"]
    pixels = image["pixels"]
    if new == "extend":
        return get_pixel(
            image, (min(max(row, 0), width - 1)), (min(max(col, 0), height - 1))
        )
    if new == "wrap":
        return get_pixel(image, row % width, col % height)
    if new == "zero":
        return 0
    if width > row and row >= 0 and height > col and col >= 0:
        new = pixels[row + col * width]
        return new
    return None


def correlate(image, kernel, boundary_behavior):
    """
    Compute the result of correlating the given image with the given kernel.
    `boundary_behavior` will one of the strings "zero", "extend", or "wrap",
    and this function will treat out-of-bounds pixels as having the value zero,
    the value of the nearest edge, or the value wrapped around the other edge
    of the image, respectively.

    if boundary_behavior is not one of "zero", "extend", or "wrap", return
    None.

    Otherwise, the output of this function should have the same form as a 6.101
    image (a dictionary with "height", "width", and "pixels" keys), but its
    pixel values do not necessarily need to be in the range [0,255], nor do
    they need to be integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    Makes array of arrays, use nested loops
    """
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [0] * len(image["pixels"]),
    }
    imagewidth = image["width"]
    imageheight = image["height"]
    # pixels = image['pixels']
    height = len(kernel)
    width = len(kernel[0])
    halfw = len(kernel) // 2
    halfh = len(kernel) // 2

    for col in range(imageheight):
        for row in range(imagewidth):
            count = 0
            for rows in range(height):
                for columns in range(width):
                    newrows = rows + row - halfw
                    newcols = columns + col - halfh
                    newk = kernel[columns][rows]
                    count += newk * updatedPixel(
                        image, newrows, newcols, boundary_behavior
                    )
            set_pixel(result, row, col, count)
    return result


def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the "pixels" list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    for ipixel in range(len(image["pixels"])):
        pixel = round(image["pixels"][ipixel])
        pixel = min(max(pixel, 0), 255)
        image["pixels"][ipixel] = pixel
    return image


# FILTERS
def blurerhelp(n):
    """Helper function for blurred function
    Generates a 2D list"""
    return [[1 / n**2] * n] * n


def blurred(image, kernel_size):
    """
    Return a new image representing the result of applying a box blur (with
    kernel size n) to the given input image.
    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # first, create a representation for the appropriate n-by-n kernel (you may
    # wish to define another helper function for this)
    # then compute the correlation of the input image with that kernel using
    # the 'extend' behavior for out-of-bounds pixels
    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    newKernel = blurerhelp(kernel_size)
    return round_and_clip_image(correlate(image, newKernel, "extend"))


def edges(image):
    krow = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    kcol = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    corRow = correlate(image, krow, "extend")
    corCol = correlate(image, kcol, "extend")
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [0] * len(image["pixels"]),
    }
    for col in range(image["height"]):
        for row in range(image["width"]):
            both = math.sqrt(
                updatedPixel(corRow, row, col, "extend") ** 2
                + updatedPixel(corCol, row, col, "extend") ** 2
            )
            set_pixel(result, row, col, both)
    return round_and_clip_image(result)


def sharpened(image, n):
    blurred = [[-1 / n**2] * n for i in range(n)]
    blurred[n // 2][n // 2] += 2
    return round_and_clip_image(correlate(image, blurred, "extend"))


# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image("test_images/cat.png")
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [
                round(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) for p in img_data
            ]
        elif img.mode == "LA":
            pixels = [p[0] for p in img_data]
        elif img.mode == "L":
            pixels = list(img_data)
        else:
            raise ValueError(f"Unsupported image mode: {img.mode}")
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_greyscale_image(image, filename, mode="PNG"):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the "mode" parameter.
    """
    out = Image.new(mode="L", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    pass
    # invertedBlueGill = inverted(load_greyscale_image('test_images/bluegill.png'))
    # save_greyscale_image(invertedBlueGill, 'inverted_bluegill.png')
    # kernelpb = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    # pigbird_zero = correlate(load_greyscale_image('test_images/pigbird.png'), kernelpb, 'zero')
    # save_greyscale_image(pigbird_zero, 'pigbird_zero.png')

    # pigbirdExtend = correlate(load_greyscale_image('test_images/pigbird.png'), kernelpb, 'extend')
    # save_greyscale_image(pigbirdExtend, 'pigbirdExtended.png')

    # pigbirdWrap = correlate(load_greyscale_image('test_images/pigbird.png'), kernelpb, 'wrap')
    # save_greyscale_image(pigbirdWrap, 'pigbirdWrap.png')

    # catBlurred = blurred(load_greyscale_image('test_images/cat.png'), 13)
    # save_greyscale_image(catBlurred, 'catBlurred.png')
    # ##changed to zero
    # catBlurredZero = blurred(load_greyscale_image('test_images/cat.png'), 13)
    # save_greyscale_image(catBlurredZero, 'catBlurredZero.png')
    # ##changed to wrap
    # catBlurredWrap= blurred(load_greyscale_image('test_images/cat.png'), 13)
    # save_greyscale_image(catBlurredWrap, 'catBlurredWrap.png')

    # catBlurredZero = blurred(load_greyscale_image('test_images/cat.png'), 13)
    # save_greyscale_image(catBlurredZero, 'catBlurredZero.png')

    # catBlurredturn = correlate(load_greyscale_image('test_images/cat.png'), kernelpb, 'zero')
    # save_greyscale_image(catBlurredturn, 'catBlurredturn.png')
    # catBlurredZero = blurred(load_greyscale_image('catBlurredturn.png'), 13)
    # save_greyscale_image(catBlurredZero, 'catBlurredZero.png')

    # save_greyscale_image(catBlurredturnw, 'catBlurredturnw.png')
    # catBlurredWrap = blurred(load_greyscale_image('catBlurredturnw.png'), 13)
    # save_greyscale_image(catBlurredWrap, 'catBlurredWrap.png')

    # blurredCatZero = blurred(load_greyscale_image('test_images/cat.png'), 13)
    # save_greyscale_image(blurredCatZero, 'blurredCatZero.png')
    # blurredCatZeroFinal = correlate(load_greyscale_image('blurredCatZero.png'), kernelpb, 'wrap')

    # blurredCatWrap = blurred(load_greyscale_image('test_images/cat.png'), 13)
    # save_greyscale_image(blurredCatZero, 'blurredCatZero.png')

    # pythonShapened1 = sharpened(load_greyscale_image('test_images/python.png'),11)
    # save_greyscale_image(pythonShapened1, 'pythonShapened1.png')

    constructEdges = edges(load_greyscale_image("test_images/construct.png"))
    save_greyscale_image(constructEdges, "constructEdges.png")
