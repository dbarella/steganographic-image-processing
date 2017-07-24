"""Script for processing steganographically-encoded images."""

import argparse
import pathlib
import os
import sys

from PIL import Image

# Specific to this package
import utilities

RGB_RANGE = 0b11111111


def argument_parser():
    # type: () -> argparse.ArgumentParser
    """Returns a configured argparser.ArgumentParser for this program."""
    parser = argparse.ArgumentParser(
        description='Process an image to figure out if it contains ~*SECRETS*~',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'image_name',
        type=str,
        help='The name of the image to process.')
    parser.add_argument(
        '--significant_digits_lower_bound',
        type=int,
        default=1,
        help='The lowest number of least significant digits to scan over.')
    parser.add_argument(
        '--significant_digits_upper_bound',
        type=int,
        default=1,
        help='The highest number of least significant digits to scan over.')
    parser.add_argument(
        '--display',
        action='store_true',
        default=False,
        help='Display the images processed by this script.')
    parser.add_argument(
        '--save_images',
        action='store_true',
        help='Save the images generated by this script.')
    parser.add_argument(
        '--output_dir',
        type=pathlib.Path,
        default='.',
        help=(
            'Save the images generated by this script to a specific location. '
            'If not specified, the current working directory will be used.'))

    return parser


def image_apply(image, function):
    # type: (PIL.Image, Callable[[int], int]) -> PIL.Image
    """Applies a function to an image, returning the result as a new image.

    Args:
        image: The image to process.
        function: A function :: int -> int that takes a value \in [0, 256) and
            returns a new value \in [0, 256).
    """
    return Image.merge(
        'RGB', [channel.point(function) for channel in image.split()])


def least_significant_digits(pixel_value, n_significant_digits):
    # type: int -> int
    """Returns the n least-significant-digits of pixel_value."""
    return pixel_value & utilities.bit_mask(n_significant_digits)


def normalize_to_rgb(value, n_significant_digits):
    # type: (int, int) -> int
    """Normalizes an int value \in [0, n_significant_digits) to RGB."""
    if n_significant_digits == 0:
        return value
    return value * int(float(RGB_RANGE) / n_significant_digits)


def apply_function_and_normalize_to_rgb(function, n_significant_digits):
    # type: (Callable[[int, int], int], int) -> Callable[int, int]
    """Composes a function which takes a pixel and applies function to it."""
    def inner(pixel_value):
        return normalize_to_rgb(
            function(pixel_value, n_significant_digits),
            n_significant_digits)
    return inner


def process(image, significant_digit_interval):
    # type: (str, Tuple[int, int]) -> Dict[int, PIL.Image]
    """Runs an image through some steganographic decodings.

    Args:
        image: The image to process.
        significant_digit_interval: An inverval of [int, int) over which
            to process the image.
    Returns:
        A map of least-significant-digit to post-processed image.
    """
    processed_images = {}
    for significant_digits in range(*significant_digit_interval):
        processed_images[significant_digits] = (
            image_apply(
                image,
                apply_function_and_normalize_to_rgb(
                    least_significant_digits,
                    utilities.bit_mask(significant_digits))))
    return processed_images


def save(images, output_dir):
    # type: (Dict[int, PIL.Image], pathlib.Path) -> None
    """Saves images with filenames showing the significant digit processed."""
    for significant_digits, image in images.items():
        filename = ('0b{0:b}.png'.format(
            utilities.bit_mask(significant_digits)))
        image.save(
            output_dir.joinpath(filename), format='png', quality=100)


def main():
    args = argument_parser().parse_args()

    # type: Dict[int, PIL.Image]
    lsd_to_images_map = process(
        Image.open(args.image_name),
        significant_digit_interval=(
            args.significant_digits_lower_bound,
            args.significant_digits_upper_bound + 1))

    # Display the processed images
    if args.display:
        for _, image in sorted(lsd_to_images_map.items()):
            image.show()

    # Save the images, if the user wants us to
    if args.save_images:
        user_response = (
            utilities.query_user(
                'GONNA SAVE {0:d} IMAGES to "{1:s}"; GAR, IS THAT K???'.format(
                    len(lsd_to_images_map), str(args.output_dir.absolute()))))
        if user_response:
            save(lsd_to_images_map, output_dir=args.output_dir)


if __name__ == '__main__':
    main()
