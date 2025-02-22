import os
import sys
from PIL import Image, ImageEnhance, ImageOps
import numpy as np
script_dir = os.path.dirname(os.path.abspath(__file__))
pic_path = os.path.join(script_dir, 'pic')
bmp_path = os.path.join(script_dir, 'bmp')
sys.path.append(pic_path)
sys.path.append(bmp_path)

class ImageConverter:

    def __init__(self):
        self.input_directory = pic_path
        self.output_directory = bmp_path

        self.image_files = [file for file in os.listdir('pic') if 'modified' not in file]
    
    def process_image(self, file_name):
        img_path = os.path.join(self.input_directory, file_name)
        self.resize_image(img_path)
        self.to_bmp_seven_color(img_path)
            

    # Resize the image given by input_path and overwrite to the same path
    def resize_image(self, img_path):
        # Screen target size dims
        target_width = 600
        target_height = 448

        with Image.open(img_path) as img:
            img = ImageOps.exif_transpose(img)
            
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.3)
            
            # Original dimensions
            orig_width, orig_height = img.size

            original_aspect_ratio = orig_width / orig_height
            target_aspect_ratio = target_width / target_height

            # Fit height and crop sides
            if original_aspect_ratio > target_aspect_ratio:
                new_height = target_height
                new_width = int(new_height * original_aspect_ratio)
            # Fit width and crop top/bottom
            else:
                new_width = target_width
                new_height = int(new_width / original_aspect_ratio)

            # Resize the image while maintaining aspect ratio
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Calculate the cropping box to center the crop
            left = (new_width - target_width) // 2
            top = (new_height - target_height) // 2
            right = left + target_width
            bottom = top + target_height

            # Crop the image
            cropped_img = resized_img.crop((left, top, right, bottom))

            # Save the final image
            cropped_img.save(img_path)
    
    # Convert input image to bmp and save at the specified output path
    def to_bmp_seven_color(self, img_path):
        
        # Define the 7 colors in the palette (RGB values)
        palette_colors = [
            (0, 0, 0),  # Black: 0x0
            (255, 255, 255),  # White: 0x1
            (0, 255, 0),  # Green: 0x2
            (0, 0, 255),  # Blue: 0x3
            (255, 0, 0),  # Red: 0x4
            (255, 255, 0),  # Yellow: 0x5
            (255, 165, 0)  # Orange: 0x6
        ]

        # Create the flat palette by expanding each color tuple into individual RGB values
        flat_palette = []
        for color in palette_colors:
            flat_palette.extend(color)

        # Pad the palette with zeros to make it 256 colors (each with 3 channels: RGB)
        remaining_colors = 256 - len(palette_colors)
        flat_palette.extend([0] * remaining_colors * 3)

        # Create a palette image with the 7 colors
        palette_img = Image.new("P", (1, 1))
        palette_img.putpalette(flat_palette)

        # Open the image and convert it to RGB
        img = Image.open(img_path).convert("RGB")

        # Quantize the input image using the palette
        img_quantized = img.quantize(palette=palette_img)

        # Save the quantized image as BMP
        file_name = os.path.splitext(os.path.basename(img_path))[0]
        save_path = os.path.join(self.output_directory, f'{file_name}.bmp')
        img_quantized.save(save_path, format="BMP")
