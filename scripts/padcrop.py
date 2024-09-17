#!/usr/bin/env python3

"""
Add padding around cropped images.

This script processes images by removing existing padding and adding new
padding. It supports sequential and parallel processing of multiple images.
"""

import sys
from pathlib import Path

import concurrent.futures
import argparse

from PIL import Image, ImageOps

script_name = Path(sys.argv[0]).name


def _process_image(filename, padding):
    """
    Crop an image and add padding.

    Opens an image, removes existing padding, adds new padding, and saves
    the modified image with a new filename.

    Args:
        filename (str):
            Path to the image file.
        padding (int):
            Number of pixels for new padding.

    Returns:
        None
    """

    img = Image.open(filename)

    cropped = img.crop(bbox) if (bbox := img.getbbox()) else img

    # Add padding
    new_img = ImageOps.expand(
        cropped, border=padding, fill=(255, 255, 255)
    )  # Assuming white padding

    # Save new image
    path = Path(filename)
    new_path = path.with_stem(f"{path.stem} padding={padding}")
    new_img.save(new_path)

    print(f"{path.name}: {new_path.name}")


def process_image(padding, filename):
    """
    Process an image by cropping its padding and adding new padding.

    This function opens an image file, calculates the amount of padding to be
    removed, crops the image accordingly, and then adds a specified amount of
    new padding around it. The processed image is saved with a modified
    filename indicating the padding applied.

    Args:
        padding (int):
            Number of pixels to add as padding around the cropped image.
        filename (str):
            Path to the image file to be processed.

    Returns:
        None

    Raises:
        OSError:
            If there is an error opening or saving the image file.
        ValueError:
            If there is an issue with the image processing.
    """

    try:
        _process_image(filename, padding)
        return True
    except (OSError, ValueError) as e:
        print(f"Error processing {filename}: {str(e)}", file=sys.stderr)
        return False


def main(padding, filenames, use_parallel=True):
    """
    Run the image processing.

    This function takes a specified padding size, a list of filenames, and an
    optional flag to disable parallel processing. It processes each filename
    in parallel or sequentially based on the flag.

    Args:
        padding (int):
            Number of pixels to add as padding around the cropped image.
        filenames (list of str):
            A list of image filenames to be processed.
        use_parallel (bool, optional):
            Flag to disable parallel processing. Defaults to True.

    Returns:
        None
    """

    if use_parallel:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(
                executor.map(lambda f: process_image(padding, f), filenames)
            )
    else:
        results = list(map(lambda f: process_image(padding, f), filenames))

    # Log the number of successful and failed processes
    success_count = sum(results)
    failure_count = len(filenames) - success_count
    print(f"Processed {success_count} images successfully.")
    if failure_count:
        print(f"{failure_count} failures.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process images with padding."
    )
    parser.add_argument(
        "--use_parallel",
        action="store_true",
        help="Enable parallel processing",
    )
    parser.add_argument(
        "padding",
        type=int,
        help="Number of pixels for padding",
        choices=range(1000),
    )
    parser.add_argument(
        "filenames", nargs="+", help="List of image filenames to process"
    )

    args = parser.parse_args()

    main(args.padding, args.filenames, args.use_parallel)
