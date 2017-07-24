"""Convenience functions for running the process(encode) pipeline."""

import argparse
import pathlib

from PIL import Image

import encoding
import processing


def argument_parser():
    # type: () -> argparse.ArgumentParser
    """Returns a configured argparser.ArgumentParser for this program."""
    parser = argparse.ArgumentParser(
        description='Chain an image decode and encode!',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'host_image',
        type=pathlib.Path,
        help='The image that will hide the information.')
    parser.add_argument(
        'payload_image',
        type=pathlib.Path,
        help='The image that will be hidden within the host image.')
    parser.add_argument(
        '--encoding_significant_digits',
        type=int,
        default=1,
        help='The number of least significant digits with which to encode.')
    parser.add_argument(
        '--processing_least_significant_digits_lower_bound',
        type=int,
        default=1,
        help='The lowest number of least significant digits to scan over.')
    parser.add_argument(
        '--processing_least_significant_digits_upper_bound',
        type=int,
        default=1,
        help='The highest number of least significant digits to scan over.')

    return parser


def pipeline(
        host_image,
        payload_image,
        encoding_significant_digits,
        least_significant_digit_interval):
    # type: (PIL.Image, PIL.Image, int, Tuple[int, int]) -> Dict[int, PIL.Image]
    """Encodes an image using some params, returning a decoded-image dict."""
    encoded = encoding.encode(
        host_image, payload_image, encoding_significant_digits)

    return processing.process(
        image=encoding.encode(
            host_image,
            payload_image,
            encoding_significant_digits),
        least_significant_digit_interval=least_significant_digit_interval)


def main():
    args = argument_parser().parse_args()

    # type: Dict[int, PIL.Image]
    lsd_to_images_map = pipeline(
        host_image=Image.open(args.host_image),
        payload_image=Image.open(args.payload_image),
        encoding_significant_digits=args.encoding_significant_digits, 
        least_significant_digit_interval=(
            args.processing_least_significant_digits_lower_bound,
            args.processing_least_significant_digits_upper_bound + 1))

    # Display the processed images
    for _, image in lsd_to_images_map.items():
        image.show()


if __name__ == '__main__':
    main()
