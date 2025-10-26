"""Image processing module for e-ink display optimization.

This module handles the conversion of source images to e-ink display format,
including resizing, cropping, and color/contrast enhancement for optimal
display on e-paper screens.
"""

import os
from typing import Tuple

from PIL import Image, ImageEnhance, ImageOps


class ImageConverter:
    """Handles image processing and conversion for e-ink display optimization.

    This class processes images from a source directory, resizing and enhancing
    them for optimal display on e-paper screens. Images are resized to fit the
    target dimensions while maintaining aspect ratio, then cropped and enhanced
    for better visibility on e-ink displays.

    Attributes:
        source_dir: Directory containing source images to process
        output_dir: Directory where processed images will be saved
        target_width: Target width for processed images (800px)
        target_height: Target height for processed images (480px)
    """

    def __init__(self, source_dir: str, output_dir: str) -> None:
        """Initialize the ImageConverter with source and output directories.

        Args:
            source_dir: Path to directory containing source images
            output_dir: Path to directory where processed images will be saved
        """
        self.source_dir: str = source_dir
        self.output_dir: str = output_dir
        self.target_width: int = 800  # E-ink display width
        self.target_height: int = 480  # E-ink display height

    def process_images(self) -> None:
        """Process all valid image files in the source directory.

        Scans the source directory for supported image formats and processes
        each one for e-ink display. Skips hidden files and non-image files.

        Supported formats: .jpg, .jpeg, .png, .bmp, .gif, .tiff
        """
        # Define supported image file extensions
        valid_extensions: Tuple[str, ...] = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff")

        # Process each file in the source directory
        for img in os.listdir(self.source_dir):
            # Skip hidden files (starting with dot)
            if img.startswith("."):
                continue

            print(f"Found file: {img}")
            img_path: str = os.path.join(self.source_dir, img)

            # Process only valid image files
            if os.path.isfile(img_path) and img.lower().endswith(valid_extensions):
                print(f"Processing image: {img_path}")
                self.resize_image(img_path, img)

    def resize_image(self, img_path: str, file_name: str) -> None:
        """Resize and enhance an image for e-ink display.

        Processes a single image through the complete optimization pipeline:
        1. Loads and corrects image orientation using EXIF data
        2. Resizes while maintaining aspect ratio
        3. Crops to exact target dimensions (centered)
        4. Enhances color saturation and contrast for e-ink visibility
        5. Saves the processed image to the output directory

        Args:
            img_path: Full path to the source image file
            file_name: Name of the file for the output image
        """
        # Use class-defined target dimensions for consistency
        target_width: int = self.target_width
        target_height: int = self.target_height

        with Image.open(img_path) as img:
            # Correct image orientation based on EXIF data
            img = ImageOps.exif_transpose(img)

            # Calculate aspect ratios for resize strategy
            orig_width, orig_height = img.size
            original_aspect_ratio: float = orig_width / orig_height
            target_aspect_ratio: float = target_width / target_height

            # Determine resize dimensions to fill target area (may require cropping)
            if original_aspect_ratio > target_aspect_ratio:
                # Image is wider than target - fit height and crop sides
                new_height: int = target_height
                new_width: int = int(new_height * original_aspect_ratio)
            else:
                # Image is taller than target - fit width and crop top/bottom
                new_width: int = target_width
                new_height: int = int(new_width / original_aspect_ratio)

            print("Resizing image...")
            # Resize image using high-quality Lanczos resampling
            resized_img: Image.Image = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Calculate centered crop coordinates
            left: int = (new_width - target_width) // 2
            top: int = (new_height - target_height) // 2
            right: int = left + target_width
            bottom: int = top + target_height

            print("Cropping image...")
            # Crop to exact target dimensions with center alignment
            cropped_img: Image.Image = resized_img.crop((left, top, right, bottom))

            print("Enhancing image...")
            # Enhance color saturation for better e-ink visibility
            color_enhancer: ImageEnhance.Color = ImageEnhance.Color(cropped_img)
            cropped_img = color_enhancer.enhance(1.5)  # 50% more saturation

            # Enhance contrast for sharper e-ink display
            contrast_enhancer: ImageEnhance.Contrast = ImageEnhance.Contrast(cropped_img)
            cropped_img = contrast_enhancer.enhance(1.5)  # 50% more contrast

            print("Saving processed image...")
            # Save the final optimized image to output directory
            output_path: str = os.path.join(self.output_dir, file_name)
            cropped_img.save(output_path)
