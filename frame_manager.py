"""Main entry point for the e-ink frame application.

This module coordinates the image processing and display workflow for an e-ink frame.
It processes images from an SD card, converts them for display, and manages the
display rotation cycle.

Usage:
    python frame_manager.py <sd_path> <refresh_time>

Args:
    sd_path: Path to the SD card containing source images
    refresh_time: Time in seconds between image rotations
"""

import os
import shutil
import sys
from typing import NoReturn

from display_manager import DisplayManager
from image_converter import ImageConverter

# Directory paths for the application
SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))
PIC_PATH: str = os.path.join(SCRIPT_DIR, "pic")  # Local directory for processed images
SD_MOUNT_BASE: str = "/media/pi"  # Base path for SD card mounts


def main() -> NoReturn:
    """Main application entry point.

    Orchestrates the complete workflow: image processing from SD card,
    conversion for e-ink display, and continuous image rotation.

    Raises:
        SystemExit: If insufficient command line arguments provided
        Exception: For errors during image processing or display
    """
    # Validate command line arguments
    if len(sys.argv) < 3:
        print("Usage: python frame_manager.py <sd_path> <refresh_time>")
        sys.exit(1)

    # Parse command line arguments
    sd_path: str = sys.argv[1]
    refresh_time: int = int(sys.argv[2])
    print(f"Frame manager received SD path: {sd_path}")
    print(f"Frame manager received refresh time: {refresh_time} seconds")

    # Initialize display manager for the e-ink screen
    display_manager: DisplayManager = DisplayManager(image_folder=PIC_PATH, refresh_time=refresh_time)
    print("Display manager created")

    # Prepare local image directory (clean slate for new images)
    if os.path.exists(PIC_PATH):
        shutil.rmtree(PIC_PATH)  # Remove any existing processed images
    os.makedirs(PIC_PATH)  # Create fresh directory for new processed images

    # Initialize image converter for processing SD card images
    image_converter: ImageConverter = ImageConverter(source_dir=sd_path, output_dir=PIC_PATH)
    print("Image converter created")

    # Show startup message on display while processing
    display_manager.display_message("start.jpg")

    # Process all images from the SD card
    try:
        print("Processing images, please wait...")
        image_converter.process_images()
    except Exception as e:
        print(f"Error during image processing: {e}")
        # Continue execution even if some images fail to process

    # Begin continuous image display rotation
    try:
        display_manager.display_images()
    except Exception as e:
        print(f"Error during image display: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
