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
    parser.add_argument(
        '--display_encoded_image',
        action='store_true',
        help="Show the encoded image, if you're curious")

    return parser


def pipeline(
        host_image,
        payload_image,
        encoding_significant_digits,
        least_significant_digit_interval):
    # type: (
    #    PIL.Image, PIL.Image, int, Tuple[int, int]
    # ) -> Tuple[PIL.Image, Dict[int, PIL.Image]]
    """Encodes an image using some params, returning encoded and decoded images.

    Args:
        host_image: Host image.
        payload_image: Payload image.
        (Yeah, I know, and I don't care. These values are documented elsewhere.)
        encoding_significant_digits: The significant digits to use in the
            encoding.
        least_significant_digits_interval: The significant digits to scan over
            when decoding the image.
    Returns:
        A 2-tuple; the first item is the encoded image, the second item is a
        dictionary mapping from significant_digit to decoded PIL.Image.
    """
    encoded = encoding.encode(
        host_image, payload_image, encoding_significant_digits)

    return (
        encoded,
        processing.process(
            image=encoding.encode(
                host_image,
                payload_image,
                encoding_significant_digits),
            least_significant_digit_interval=least_significant_digit_interval))


def main():
    args = argument_parser().parse_args()

    # type: Dict[int, PIL.Image]
    encoded, lsd_to_images_map = pipeline(
        host_image=Image.open(args.host_image),
        payload_image=Image.open(args.payload_image),
        encoding_significant_digits=args.encoding_significant_digits, 
        least_significant_digit_interval=(
            args.processing_least_significant_digits_lower_bound,
            args.processing_least_significant_digits_upper_bound + 1))

    # Display the processed images
    for _, image in lsd_to_images_map.items():
        image.show()


    if args.display_encoded_image:
        input('Hit enter to display the encoded image.')
        encoded.show()


if __name__ == '__main__':
    main()
