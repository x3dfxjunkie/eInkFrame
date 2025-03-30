from image_converter import ImageConverter
from display_manager import DisplayManager
import os
import shutil
import time
import threading

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PIC_PATH = os.path.join(SCRIPT_DIR, 'pic')
SD_MOUNT_BASE = "/media/enriquepi"  # Adjust this path as needed

display_manager = DisplayManager(image_folder=PIC_PATH)
print("display manager created")
sd_card_present = threading.Event()


def wait_for_sd_card(mount_base=SD_MOUNT_BASE):
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
            display_manager.display_message('no_sd_card.jpg')
        except Exception as e:
            print(f"Error accessing {mount_base}: {e}")
        time.sleep(5)


def monitor_sd_card(mount_base=SD_MOUNT_BASE):
    """Continuously monitor SD card presence and trigger reprocessing if inserted."""
    global sd_card_present
    while True:
        items = os.listdir(mount_base)
        valid_dirs = [item for item in items if os.path.isdir(os.path.join(mount_base, item))]
        sd_inserted = len(valid_dirs) >= 1

        if sd_inserted and not sd_card_present.is_set():
            print("SD card inserted. Reprocessing images...")
            sd_card_present.set()
            display_manager.stop_display = True
            process_images()  # Restart processing

        elif not sd_inserted and sd_card_present.is_set():
            print("SD card removed.")
            sd_card_present.clear()

        time.sleep(2)


def process_images():
    if os.path.exists(PIC_PATH):
        shutil.rmtree(PIC_PATH)
    os.makedirs(PIC_PATH)

    # Wait for the SD card to be mounted.
    sd_path = wait_for_sd_card()
    print(sd_path)

    image_converter = ImageConverter(source_dir=sd_path, output_dir=PIC_PATH)
    print("image converter created")

    # Process images from the SD card.
    display_manager.display_message('start.jpg')
    try:
        print("Processing images, please wait...")
        image_converter.process_images()
    except Exception as e:
        print(f"Error during image processing: {e}")

    # Display images
    try:
        display_manager.display_images()
    except Exception as e:
        print(f"Error during image processing: {e}")


def main():
    threading.Thread(target=monitor_sd_card, daemon=True).start()
    process_images()


if __name__ == "__main__":
    main()