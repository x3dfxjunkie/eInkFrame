from image_converter import ImageConverter
from display_manager import DisplayManager
import os
import shutil
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_PATH = os.path.join(SCRIPT_DIR, 'lib')
PIC_PATH = os.path.join(SCRIPT_DIR, 'pic')

def wait_for_sd_card(mount_base="/media/enriquepi"):
    """
    Wait until an SD card is mounted in the mount_base directory.
    Assumes the SD card is the only item under mount_base.
    """
    while True:
        try:
            items = os.listdir(mount_base)
            if len(items) == 1:
                sd_path = os.path.join(mount_base, items[0])
                if os.path.isdir(sd_path):
                    print(f"SD card detected at: {sd_path}")
                    return sd_path
            print("SD card not found. Please insert the SD card.")
        except Exception as e:
            print(f"Error accessing {mount_base}: {e}")
        time.sleep(5)


def main():
    if not os.path.exists(PIC_PATH):
        os.makedirs(PIC_PATH)
    shutil.rmtree(PIC_PATH)

    # Wait for the SD card to be mounted.
    sd_path = wait_for_sd_card()

    # Create instances of the classes using the SD card as the source.
    image_converter = ImageConverter(source_dir=sd_path, output_dir=PIC_PATH)
    display_manager = DisplayManager(image_folder=PIC_PATH)

    # Process images from the SD card.
    try:
        image_converter.process_all_images()
    except Exception as e:
        print(f"Error during image processing: {e}")

    # Main loop: display images and monitor SD card status.
    try:
        while True:
            # Check if the SD card is still mounted.
            if not os.path.exists(sd_path):
                print("SD card has been removed! Waiting for re-insertion...")
                sd_path = wait_for_sd_card()
                # Re-run image processing after the SD card is re-inserted.
                image_converter = ImageConverter(source_dir=sd_path, output_dir=PIC_PATH)
                try:
                    image_converter.process_all_images()
                except Exception as e:
                    print(f"Error during image processing: {e}")

            display_manager.show_next_image()
            time.sleep(display_manager.display_interval)
    except KeyboardInterrupt:
        print("Exiting gracefully.")

if __name__ == "__main__":
    main()