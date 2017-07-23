"""Script for encoding a payload into an image."""

from PIL import Image, ImageMath


def encode(host, payload):
    # type: (PIL.Image, PIL.Image) -> PIL.Image
    """Encode a payload into an image."""
    output_rgb_channels = []
    for host_channel, payload_channel in zip(host.split(), payload.split()):
        # Mask out all but the least significant byte, encoding payload there
        expression = "convert((host & (0xff - 0b11)) | (payload & 0x11), 'L')"
        output_rgb_channels.append(
            ImageMath.eval(
                expression,
                host=host_channel,
                payload=payload_channel))
    return Image.merge('RGB', output_rgb_channels)
