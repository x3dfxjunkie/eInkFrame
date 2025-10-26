"""
Helper script to generate pre-built test images for the test suite.

This script creates test images with various:
- Sizes and aspect ratios
- Color modes
- EXIF orientations
- File formats

Run this script once to populate tests/test_images/ directory.
Usage: python tests/create_test_images.py
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os


def create_test_images_directory():
    """Create the test_images directory if it doesn't exist."""
    test_images_dir = Path(__file__).parent / 'test_images'
    test_images_dir.mkdir(exist_ok=True)
    return test_images_dir


def add_text_to_image(img, text):
    """Add descriptive text to an image."""
    draw = ImageDraw.Draw(img)
    try:
        # Try to use a basic font
        font = ImageFont.load_default()
    except:
        font = None

    # Draw text in upper left corner
    color = (0, 0, 0) if img.mode == 'RGB' else 0
    draw.text((10, 10), text, fill=color, font=font)
    return img


def create_aspect_ratio_images(test_images_dir):
    """Create images with various aspect ratios."""
    print("Creating aspect ratio test images...")

    # Square image (1:1)
    img = Image.new('RGB', (500, 500), color='blue')
    add_text_to_image(img, 'Square 1:1')
    img.save(test_images_dir / 'sample_square.png')
    print("  - sample_square.png (500x500)")

    # Wide image (16:9)
    img = Image.new('RGB', (1600, 900), color='green')
    add_text_to_image(img, 'Wide 16:9')
    img.save(test_images_dir / 'sample_wide.png')
    print("  - sample_wide.png (1600x900)")

    # Tall image (1:2)
    img = Image.new('RGB', (600, 1200), color='red')
    add_text_to_image(img, 'Tall 1:2')
    img.save(test_images_dir / 'sample_tall.png')
    print("  - sample_tall.png (600x1200)")

    # Small image (below target)
    img = Image.new('RGB', (100, 100), color='yellow')
    add_text_to_image(img, 'Small')
    img.save(test_images_dir / 'sample_small.png')
    print("  - sample_small.png (100x100)")

    # Large image (above target)
    img = Image.new('RGB', (4000, 3000), color='purple')
    add_text_to_image(img, 'Large')
    img.save(test_images_dir / 'sample_large.png')
    print("  - sample_large.png (4000x3000)")

    # Exact target size
    img = Image.new('RGB', (800, 480), color='cyan')
    add_text_to_image(img, 'Exact 800x480')
    img.save(test_images_dir / 'sample_exact.png')
    print("  - sample_exact.png (800x480)")


def create_color_mode_images(test_images_dir):
    """Create images with various color modes."""
    print("Creating color mode test images...")

    # RGB color
    img = Image.new('RGB', (800, 480), color='white')
    add_text_to_image(img, 'RGB Mode')
    img.save(test_images_dir / 'sample_rgb.png')
    print("  - sample_rgb.png (RGB mode)")

    # RGBA with transparency
    img = Image.new('RGBA', (800, 480), color=(255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([100, 100, 300, 300], fill=(255, 0, 0, 128))
    img.save(test_images_dir / 'sample_rgba.png')
    print("  - sample_rgba.png (RGBA mode)")

    # Grayscale
    img = Image.new('L', (800, 480), color=128)
    add_text_to_image(img, 'Gray')
    img.save(test_images_dir / 'sample_grayscale.png')
    print("  - sample_grayscale.png (Grayscale)")

    # Palette mode (GIF)
    img = Image.new('P', (800, 480))
    img.paste(100, (0, 0, 400, 240))
    img.paste(200, (400, 0, 800, 240))
    img.paste(150, (0, 240, 800, 480))
    img.save(test_images_dir / 'sample_palette.gif')
    print("  - sample_palette.gif (Palette mode)")


def create_format_images(test_images_dir):
    """Create test images in various formats."""
    print("Creating format test images...")

    base_img = Image.new('RGB', (800, 480), color='orange')
    add_text_to_image(base_img, 'Format Test')

    # JPEG
    base_img.save(test_images_dir / 'sample.jpg', 'JPEG')
    print("  - sample.jpg (JPEG format)")

    # PNG
    base_img.save(test_images_dir / 'sample.png', 'PNG')
    print("  - sample.png (PNG format)")

    # BMP
    base_img.save(test_images_dir / 'sample.bmp', 'BMP')
    print("  - sample.bmp (BMP format)")

    # GIF (converted to P mode for GIF)
    base_img.convert('P').save(test_images_dir / 'sample.gif', 'GIF')
    print("  - sample.gif (GIF format)")

    # TIFF
    base_img.save(test_images_dir / 'sample.tiff', 'TIFF')
    print("  - sample.tiff (TIFF format)")


def create_exif_orientation_images(test_images_dir):
    """Create images with various EXIF orientations."""
    print("Creating EXIF orientation test images...")

    # Note: EXIF orientation requires piexif library
    # For now, create basic images that represent different orientations

    # Portrait orientation
    img = Image.new('RGB', (480, 800), color='brown')
    draw = ImageDraw.Draw(img)
    draw.rectangle([50, 50, 430, 750], outline='white', width=2)
    img.save(test_images_dir / 'exif_portrait.jpg', 'JPEG')
    print("  - exif_portrait.jpg (simulated portrait orientation)")

    # Landscape orientation
    img = Image.new('RGB', (800, 480), color='teal')
    draw = ImageDraw.Draw(img)
    draw.rectangle([50, 50, 750, 430], outline='white', width=2)
    img.save(test_images_dir / 'exif_landscape.jpg', 'JPEG')
    print("  - exif_landscape.jpg (simulated landscape orientation)")

    # Upside-down simulation
    img = Image.new('RGB', (800, 480), color='olive')
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), 'UPSIDE DOWN', fill=(255, 255, 255))
    img = img.rotate(180, expand=False)
    img.save(test_images_dir / 'exif_upside_down.jpg', 'JPEG')
    print("  - exif_upside_down.jpg (simulated upside-down orientation)")


def create_corrupted_image(test_images_dir):
    """Create a corrupted/invalid image file."""
    print("Creating corrupted test image...")

    # Write invalid JPEG data
    corrupted_path = test_images_dir / 'corrupted.jpg'
    with open(corrupted_path, 'wb') as f:
        f.write(b'This is not a valid JPEG file content\x00\x00\x00')
    print("  - corrupted.jpg (invalid JPEG data)")


def create_special_filename_images(test_images_dir):
    """Create images with special characters in filenames."""
    print("Creating special filename test images...")

    base_img = Image.new('RGB', (800, 480), color='pink')

    # Filename with spaces
    base_img.save(test_images_dir / 'image with spaces.jpg')
    print("  - image with spaces.jpg")

    # Filename with hyphens and underscores
    base_img.save(test_images_dir / 'image-2024_final.jpg')
    print("  - image-2024_final.jpg")

    # Filename with numbers
    base_img.save(test_images_dir / 'photo123.jpg')
    print("  - photo123.jpg")


def create_unusual_aspect_ratios(test_images_dir):
    """Create images with unusual aspect ratios."""
    print("Creating unusual aspect ratio test images...")

    # Ultra-wide (21:9)
    img = Image.new('RGB', (2400, 900), color='magenta')
    add_text_to_image(img, 'Ultra Wide 21:9')
    img.save(test_images_dir / 'sample_ultrawide.png')
    print("  - sample_ultrawide.png (2400x900)")

    # Ultra-tall (9:21)
    img = Image.new('RGB', (600, 1600), color='lime')
    add_text_to_image(img, 'Ultra Tall')
    img.save(test_images_dir / 'sample_ultratall.png')
    print("  - sample_ultratall.png (600x1600)")


def main():
    """Generate all test images."""
    print("Generating test images for eInkFrame test suite...\n")

    test_images_dir = create_test_images_directory()
    print(f"Test images directory: {test_images_dir}\n")

    # Create all test image categories
    create_aspect_ratio_images(test_images_dir)
    create_color_mode_images(test_images_dir)
    create_format_images(test_images_dir)
    create_exif_orientation_images(test_images_dir)
    create_corrupted_image(test_images_dir)
    create_special_filename_images(test_images_dir)
    create_unusual_aspect_ratios(test_images_dir)

    print(f"\nTest images generated successfully in {test_images_dir}")
    print(f"Total files created: {len(list(test_images_dir.glob('*')))}")


if __name__ == '__main__':
    main()
