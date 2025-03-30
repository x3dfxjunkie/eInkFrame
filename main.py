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


def check_sd_card_presence(mount_base=SD_MOUNT_BASE):
    """Returns the SD card path if present, else None."""
    try:
        items = os.listdir(mount_base)
        valid_dirs = [item for item in items if item != "rootfs" and os.path.isdir(os.path.join(mount_base, item))]
        if len(valid_dirs) == 1:
            return os.path.join(mount_base, valid_dirs[0])
    except Exception as e:
        print(f"Error accessing {mount_base}: {e}")
    return None


def wait_for_sd_card(mount_base=SD_MOUNT_BASE):
    """Wait until an SD card is mounted."""
    while True:
        sd_path = check_sd_card_presence(mount_base)
        if sd_path:
            print(f"SD card detected at: {sd_path}")
            return sd_path
        print("SD card not found. Please insert the SD card.")
        display_manager.display_message('no_sd_card.jpg')
        time.sleep(5)


def process_images():
    if os.path.exists(PIC_PATH):
        shutil.rmtree(PIC_PATH)
    os.makedirs(PIC_PATH)

    # Get the SD card path
    sd_path = wait_for_sd_card()
    print(sd_path)

    image_converter = ImageConverter(source_dir=sd_path, output_dir=PIC_PATH)
    print("image converter created")

    # Process images from the SD card
    display_manager.display_message('start.jpg')
    try:
        print("Processing images, please wait...")
        image_converter.process_images()
    except Exception as e:
        print(f"Error during image processing: {e}")

    # Start displaying images
    try:
        display_manager.display_images()
    except Exception as e:
        print(f"Error during image display: {e}")


def monitor_sd_card(mount_base=SD_MOUNT_BASE):
    """Continuously monitor SD card presence and trigger reprocessing if inserted."""
    global sd_card_present
    first_check = True  # Flag to avoid unnecessary reprocessing on first iteration

    while True:
        print("Monitoring SD card...")
        sd_path = check_sd_card_presence(mount_base)
        sd_inserted = sd_path is not None

        if sd_inserted and not sd_card_present.is_set():
            if first_check:  # Skip reprocessing on first loop iteration
                print("SD card already inserted at startup. Skipping reprocessing.")
                sd_card_present.set()
            else:
                print("SD card inserted. Reprocessing images...")
                sd_card_present.set()
                display_manager.stop_display = True
                process_images()  # Restart processing

        elif not sd_inserted and sd_card_present.is_set():
            print("SD card removed.")
            sd_card_present.clear()

        first_check = False  # Disable startup skipping after first iteration
        time.sleep(2)


def main():
    # Initialize `sd_card_present` correctly before starting the monitor thread
    if check_sd_card_presence():
        print("SD card detected at startup.")
        sd_card_present.set()
    
    # Start monitoring SD card in a separate thread
    threading.Thread(target=monitor_sd_card, daemon=True).start()

    # Only process images at startup if SD card was detected
    if sd_card_present.is_set():
        process_images()


if __name__ == "__main__":
    main()
