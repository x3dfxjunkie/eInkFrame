"""Display management for e-ink frame with automatic image rotation.

This module handles the display of processed images on an e-paper screen,
managing image rotation timing, random selection, and display lifecycle.
It interfaces with the Waveshare e-paper display library for hardware control.
"""

import atexit
import os
import random
import sys
import time
from typing import List, NoReturn, Optional

from PIL import Image

from lib.waveshare_epd import epd7in3f

# Path configuration for library access
SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))
LIB_PATH: str = os.path.join(SCRIPT_DIR, "lib")
sys.path.append(LIB_PATH)  # Add lib directory to Python path for e-paper library


class DisplayManager:
    """Manages e-paper display operations and image rotation lifecycle.

    This class handles all aspects of displaying images on the e-paper screen,
    including initialization, image selection, rotation timing, and cleanup.
    It provides automatic random image selection with duplicate prevention
    and configurable refresh intervals.

    Attributes:
        image_folder: Directory containing processed images for display
        refresh_time: Interval in seconds between image rotations
        rotation: Image rotation angle (0, 90, 180, or 270 degrees)
        epd: Waveshare e-paper display driver instance
        last_display_time: Timestamp of last image display
        last_selected_image: Name of previously displayed image (for deduplication)
        stop_display: Flag to halt the display loop
    """

    def __init__(self, image_folder: str, refresh_time: int) -> None:
        """Initialize the display manager with configuration and hardware setup.

        Sets up the e-paper display driver, configures timing parameters,
        and registers cleanup handlers for graceful shutdown.

        Args:
            image_folder: Path to directory containing processed images
            refresh_time: Interval in seconds between image rotations
        """
        # Display timing and state management
        self.last_display_time: float = time.time()
        self.last_selected_image: Optional[str] = None
        self.image_folder: str = image_folder
        self.refresh_time: int = refresh_time

        # Display configuration
        self.rotation: int = 0  # Image rotation angle in degrees
        self.stop_display: bool = False  # Flag to control display loop

        # Initialize e-paper display hardware
        self.epd: epd7in3f.EPD = epd7in3f.EPD()
        self.epd.init()  # Initialize display driver

        # Register cleanup function for graceful shutdown
        atexit.register(self.reset_frame)

    def reset_frame(self) -> None:
        """Clean up display resources and clear screen.

        Called automatically on program exit to ensure the e-paper display
        is properly cleared and put into sleep mode to prevent burn-in.
        """
        self.epd.Clear()  # Clear any displayed content
        self.epd.sleep()  # Put display into low-power sleep mode

    def fetch_image_files(self) -> List[str]:
        """Get list of all image files in the configured directory.

        Returns:
            List of image filenames available for display
        """
        # Return all files in the image directory (assumes they're all processed images)
        return [f for f in os.listdir(self.image_folder)]

    def select_random_image(self, images: List[str]) -> str:
        """Select a random image avoiding immediate repetition.

        Chooses a random image from the available list, ensuring that
        the same image isn't displayed consecutively when multiple
        images are available.

        Args:
            images: List of available image filenames

        Returns:
            Filename of the selected image
        """
        # Handle single image case
        if len(images) <= 1:
            return images[0]

        # Create list excluding previously displayed image to avoid repetition
        available_images: List[str] = [img for img in images if img != self.last_selected_image]

        # If all images were filtered out (shouldn't happen), use full list
        if not available_images:
            available_images = images

        # Select random image from available options
        random_image: str = random.choice(available_images)
        return random_image

    def display_images(self) -> NoReturn:
        """Start continuous image display rotation loop.

        Begins the main display loop that continuously rotates through
        available images at the configured refresh interval. This function
        runs indefinitely until the stop_display flag is set.

        The loop handles:
        - Initial image selection and display
        - Timed image rotation based on refresh_time
        - Random image selection with duplicate prevention
        - Error handling for missing images
        """
        # Reset display control flag
        self.stop_display = False

        # Get available images for display
        images: List[str] = self.fetch_image_files()

        # Handle case where no processed images are available
        if not images:
            print("No images found, displaying default message.")
            self.display_message("no_valid_images.jpg")
            return

        # Select and display initial image
        random_image: str = self.select_random_image(images)
        self.last_selected_image = random_image
        print(f"Displaying initial image: {random_image}")

        # Load, rotate, and display the selected image
        with Image.open(os.path.join(self.image_folder, random_image)) as pic:
            rotated_pic: Image.Image = pic.rotate(self.rotation)
            self.epd.display(self.epd.getbuffer(rotated_pic))
            self.last_display_time = time.time()

        # Main display rotation loop
        while not self.stop_display:
            current_time: float = time.time()
            elapsed_time: float = current_time - self.last_display_time

            # Check if it's time to rotate to next image
            if elapsed_time >= self.refresh_time:
                # Refresh image list (in case new images were added)
                images = self.fetch_image_files()
                random_image = self.select_random_image(images)
                self.last_selected_image = random_image

                # Load, rotate, and display the new image
                with Image.open(os.path.join(self.image_folder, random_image)) as pic:
                    print(f"Displaying new image: {random_image}")
                    rotated_pic: Image.Image = pic.rotate(self.rotation)
                    self.epd.display(self.epd.getbuffer(rotated_pic))
                    self.last_display_time = time.time()

            # Short sleep to prevent excessive CPU usage
            time.sleep(1)

    def display_message(self, message_file: str) -> None:
        """Display a predefined message image on the screen.

        Loads and displays a message image from the messages directory.
        Used for status messages like startup, error states, etc.

        Args:
            message_file: Filename of the message image to display
        """
        message_path: str = os.path.join(SCRIPT_DIR, f"messages/{message_file}")

        try:
            with Image.open(message_path) as img_start:
                rotated_img: Image.Image = img_start.rotate(self.rotation)
                self.epd.display(self.epd.getbuffer(rotated_img))
                print(f"Displayed message: {message_file}")
        except FileNotFoundError:
            print(f"Warning: Message file not found: {message_path}")
        except Exception as e:
            print(f"Error displaying message {message_file}: {e}")
