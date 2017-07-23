# Steganographic Image Processing

Just a simple python script for processing images containing
steganographically-embedded information in the least-significant digits of the
RGB values.

Written cuz I'm on vacation from work and I remembered that I actually like
coding lol. "What a time to be alive."

## Usage

`python processing.py --help` should get you started – keep in mind that you'll
need to install Pillow and pathlib (noted in `requirements.txt`).

Here's an example of how you could run the program:

```sh
python processing.py riskytxt.jpg --least_significant_digits=3 --save_processed_images
```

This will:

1. Process `riskytxt.jpg` for `0b11` and `0b111`.
1. Open the post-processed images.
1. Save the processed images to the current working directory from whence the
   script is running.
