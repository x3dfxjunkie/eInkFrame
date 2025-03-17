from image_converter import ImageConverter
from display_manager import DisplayManager
import os
import shutil
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PIC_PATH = os.path.join(SCRIPT_DIR, 'pic')

def wait_for_sd_card(mount_base="/media/enriquepi"):
    """
    Wait until an SD card is mounted in the mount_base directory.
    Assumes the SD card is the only item under mount_base.
    """
    while True:
        try:
            items = os.listdir(mount_base)
            valid_dirs = [item for item in items
                          if item != "rootfs" and os.path.isdir(os.path.join(mount_base, item))]
            if len(valid_dirs) == 1:
                sd_path = os.path.join(mount_base, valid_dirs[0])
                if os.path.isdir(sd_path):
                    print(f"SD card detected at: {sd_path}")
                    return sd_path
            print("SD card not found. Please insert the SD card.")
        except Exception as e:
            print(f"Error accessing {mount_base}: {e}")
        time.sleep(5)


def main():
    if os.path.exists(PIC_PATH):
        shutil.rmtree(PIC_PATH)
    os.makedirs(PIC_PATH)

    # Wait for the SD card to be mounted.
    sd_path = wait_for_sd_card()
    print(sd_path)

    # Create instances of the classes using the SD card as the source.
    image_converter = ImageConverter(source_dir=sd_path, output_dir=PIC_PATH)
    display_manager = DisplayManager(image_folder=PIC_PATH)
    print("classes created")

    # Process images from the SD card.
    display_manager.processing_message()
    try:
        print("Processing images, please wait...")
        image_converter.process_images()
    except Exception as e:
        print(f"Error during image processing: {e}")

    # Display images
    try:
        display_manager.display_images()
    except KeyboardInterrupt:
        print("Exiting gracefully.")

if __name__ == "__main__":
    main()